'''
File: game_info.py
'''
class GameInfo:
    def __init__(self, cash=0, hearts=0, round_num=0):
        self._cash = cash
        self._hearts = hearts
        self._round = round_num

    @property
    def cash(self):
        return self._cash
    
    @cash.setter
    def cash(self, value):
        self._cash = value

    @property
    def hearts(self):
        return self._hearts
    
    @hearts.setter
    def hearts(self, value):
        self._hearts = value

    @property
    def round_num(self):
        return self._round
    
    @round_num.setter
    def round_num(self, value):
        self._round = value

    def update_game_info(self, extracted_text):
        # Assume extracted_text contains numeric values related to cash, hearts, and round
        # Here, you would parse the extracted_text to update the game state
        # For now, we'll simulate that with placeholder values
        self.cash = 1000  # Replace with parsed value from extracted_text
        self.hearts = 5   # Replace with parsed value from extracted_text
        self.round_num = 10  # Replace with parsed value from extracted_text

    def display_info(self):
        print(f"Cash: {self.cash}, Hearts: {self.hearts}, Round: {self.round_num}")
