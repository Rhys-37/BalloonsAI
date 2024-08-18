import schedule
from screenshotter import Screenshotter
from game_info import GameInfo

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="easyocr")

def main():
    screenshotter = Screenshotter(use_gpu=True)  # Set to False to use CPU
    game_info = GameInfo()

    # Schedule the screenshot taking and game info updating process
    def update_game_info():
        # Extract values for cash, hearts, and round from the screenshot
        extracted_values = screenshotter.take_screenshot()
        
        # Update game_info with extracted values
        if 'cash' in extracted_values:
            game_info.cash = extracted_values['cash']
        if 'hearts' in extracted_values:
            game_info.hearts = extracted_values['hearts']
        if 'round' in extracted_values:
            game_info.round_num = extracted_values['round']
        
        # Display updated game info
        game_info.display_info()

    schedule.every(1).seconds.do(update_game_info)
    
    # Manually trigger the process for 5 iterations as an example
    for i in range(5):
        update_game_info()
        print(f"Cycle {i + 1} completed")

if __name__ == '__main__':
    main()
