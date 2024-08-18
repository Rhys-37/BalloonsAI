import cv2
import os
import pyscreenshot as ImageGrab
from PIL import Image, ImageOps
import numpy as np


class BoundingBox:

    def __init__(self, coordinates) -> None:
        self.coordinates = coordinates 


# Takes a screenshot of the monkey selection area 
def take_screenshot(coords, screenshot_dir):
    print("Taking screenshot!")
    screenshot_name = "bounding_box_screenshot.png"
    screenshot_file_path = os.path.join(screenshot_dir, screenshot_name)
    
    # Take and save screenshot
    screenshot = ImageGrab.grab(bbox=coords)
    screenshot.save(screenshot_file_path)

    return screenshot_file_path


def create_bounding_box(file_path, template_paths):
    image = cv2.imread(file_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    for template_path in template_paths:
        template = cv2.imread(template_path, 0)
        
        # Apply template matching
        result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)
        
        # Draw bounding boxes around detected areas
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)
    
    # Save the image with bounding boxes
    output_file_path = os.path.join(os.path.dirname(file_path), "bounding_box_output.png")
    cv2.imwrite(output_file_path, image)
    
    return output_file_path


# This block will only run if the script is executed directly, not if it's imported.
if __name__ == "__main__":

    monkey_selection_coordinates = (1655, 154, 1882, 943)
    screenshot_dir = "./BalloonsAI/Screenshots/"
    template_paths = [
        "./BalloonsAI/Screenshots/MonkeyCards/bomb_shooter.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/boomerang_monkey.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/dart_monkey.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/glue_gunner.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/heli_pilot.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/monkey_ace.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/monkey_buccaneer.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/monkey_sub.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/rosalia.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/sniper_monkey.png",  
        "./BalloonsAI/Screenshots/MonkeyCards/tack_shooter.png",  
    ]

    # screenshot_file_path = take_screenshot(monkey_selection_coordinates, screenshot_dir)
    screenshot_file_path = 'C:/Users/rhysf/OneDrive/Desktop/Coding Projects/Python Projects/BalloonsAI/Screenshots/bounding_box_screenshot.png'
    output_file_path = create_bounding_box(screenshot_file_path, template_paths)

    print(f"Bounding boxes drawn and saved to {output_file_path}")
