import random

# Player class with its respective methods and properties
class Player:
    """
    A class to represent a Player.

    Attributes:
        name: The player name
        symbol: The player symbol
        has_initiative: Allows the player to play 2 rounds in a row
        initiative_count: Limits the number of rounds played to 2 at most.
        assigned_units: Dictionary following the structure {unit_type: [stack of Unit class objects]}
        bag: List following the structure: [list of Unit class objects]
        hand: List following the structure: [list of Unit class objects]
        discarded: List following the structure: [list of Unit class objects]
        control_tokens: The number of remaining control tokens the player has.
    """
    def __init__(self, name, symbol) -> None:
        # Player information
        self.name: str = name
        self.symbol: str = symbol
        self.has_initiative: bool = False
        self.initiative_count: int = 0
        # Player unit coins
        self.assigned_units: dict = {}
        self.bag: list = []
        self.hand: list = []
        self.discarded: list = []
        self.control_tokens: int = 3

    # Print the number of available recruitment pieces
    def get_recruitment_units(self) -> bool:
        """
        Shows the current status of the recruitment units for a player.

        Returns:
            False if there are no assigned and discarded units left, True in any other case.
        """
        # If there are no more units inside the assigned_units and the discarded pile, the player has lost 
        # (no more hands can be made and thus no more moves can be made)
        if len(self.assigned_units) == 0 and len(self.discarded) == 0:
            return False 
        
        print('Recruitment pieces: ', end='')
        for unit_type, units in self.assigned_units.items():
            # Skip the royal card since it can't be recruited
            if unit_type == 'Royal':
                continue
            print(f'{unit_type} = {len(units)}, ', end='')
        print()

    def print_hand(self) -> None:
        """
        Shows the current status of the player hand.
        """
        print('Hand: ', end='')
        for unit in self.hand:
            print(f'{unit.unit_type}, ', end='')
        print()

    # Get three random units from the bag to place inside the hand
    def get_hand(self) -> bool:
        """
        Shows the current status of the player hand, if no hands can be made that means that player has lost.

        Returns:
            False if no more hands can be made, True in any other case.
        """
        # If its not possible to get a hand by retrieving 3 coins from the bag, try to fill in the bag based
        # on the discarded unit coins (if there are any)
        while len(self.bag) < 3:
            # If we have no unit coins to get from the discarded pile we can just return False
            if len(self.discarded) == 0:
                return False
            
            retrieved_coins = 0
            # Get the unit coin and add it to the bag
            unit_coin = self.discarded[retrieved_coins]
            self.bag.append(unit_coin)

            # Remove it from the discarded pile
            print(f'Removed {unit_coin.unit_type} from the discarded pile and added it to the bag since there were less than 3 unit coins in the bag')
            del self.discarded[retrieved_coins]
            retrieved_coins += 1
        
        # Reset the hand in case it hasn't been emptied due to a user input error
        self.hand = []

        print('Hand: ', end='')
        # Get three coins from the bag to place inside the hand
        for _ in range(3):
            unit_no: int = random.randint(0, len(self.bag) - 1)
            unit = self.bag[unit_no]
            print(f'{unit.unit_type}, ', end='')
            # Add to our hand
            self.hand.append(unit)
            # Remove from the bag
            del self.bag[unit_no]
        print()
        return True

    # Print the discarded pile for the current player
    def print_discard_pile(self) -> None:
        """
        Shows the current status of the player discard pile.
        """
        print('Discard pile: ', end='')
        for unit in self.discarded:
            print(f'{unit.unit_type}, ', end='')
        print()

    def print_control_tokens(self) -> None:
        """
        Shows the remaning control tokens a player has.
        """
        print(f'\nControl tokens: {self.control_tokens}\n\n')

