import os
import cv2
import easyocr
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import pyscreenshot as ImageGrab
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="easyocr")

class Screenshotter:
    def __init__(self, use_gpu=True):
        self.screenshot_dir = "./BalloonsAI/Screenshots/"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # Preload the OCR model only once
        self.reader = easyocr.Reader(['en'], gpu=use_gpu)

    def take_screenshot(self):
        print("Taking screenshot!")
        screenshot_name = "screenshot.png"
        screenshot_file_path = os.path.join(self.screenshot_dir, screenshot_name)
        
        # Take and save screenshot
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_file_path)
        
        # Perform OCR on the specific regions of the screenshot
        extracted_df = self.clean_screenshot(screenshot_file_path)
        
        # Initialize a dictionary to hold the extracted values
        extracted_values = {}
        
        # Process the DataFrame to extract values for each region
        for region in ["cash", "hearts", "round"]:
            # Filter DataFrame for the specific region
            region_df = extracted_df[extracted_df["Region"] == region]
            
            # Combine text from all entries for this region
            region_text = " ".join(region_df["Text"].tolist())
                
            # Remove commas from the text if it is for cash
            if region == "cash":
                region_text = region_text.replace(",", "")
                
            # Try to convert the combined text to an integer
            try:
                extracted_values[region] = int(region_text)
            except ValueError:
                extracted_values[region] = 0  # Default to 0 if conversion fails
        
        return extracted_values  # Return the values for all regions


    @staticmethod
    def crop_image(image, coords):
        left, top, right, bottom = coords
        return image.crop((left, top, right, bottom))

    def clean_screenshot(self, file_path):
        # Load image using PIL
        image = Image.open(file_path)

        # Optionally invert image if needed
        inverted_image = ImageOps.invert(image.convert('RGB'))  # Uncomment if you need to invert
        
        # Define regions of interest
        regions = {
            "cash": (365, 14, 522, 65),
            "hearts": (139, 14, 222, 65),
            "round": (1415, 32, 1485, 71)
        }

        # Initialize a list to store results
        all_results = []

        for label, coords in regions.items():
            # Crop the image to focus on the specific region
            cropped_image = self.crop_image(inverted_image, coords)

            # Convert PIL Image to OpenCV format
            cropped_image_cv = np.array(cropped_image)
            cropped_image_cv = cv2.cvtColor(cropped_image_cv, cv2.COLOR_RGB2BGR)

            # Save cropped image for debugging
            cv2.imwrite(os.path.join(self.screenshot_dir, f'{label}_image.jpg'), cropped_image_cv)

            # Use EasyOCR to extract text (preloaded model)
            results = self.reader.readtext(cropped_image_cv)

            # Append the results with an additional column for the region label
            for result in results:
                result_with_label = (result[0], result[1], result[2], label)
                all_results.append(result_with_label)
        
        # Create a DataFrame from all collected results
        result_df = pd.DataFrame(all_results, columns=["Coordinates", "Text", "Confidence", "Region"])
        
        return result_df
