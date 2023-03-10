import random 

from board import Board
from player import Player
from cell import Archer, Knight, Mercenary, Berserker, Unit, Royal
from high_scores import high_scores

def main():
    """
    Main entry point of the app, gives the user the option to start the game.
    """
    start_game = str(input('Start game? (y/n): '))
    if start_game == 'y':
        # Start the game
        play_game()
    else:
        print('\nYou exited the game.\n')

def generate_unit_coin(unit: str, player: Player) -> Player:
    """
    Generates a subclass of the Unit class objects depending on how it matches to the selected unit.

    Args:
        unit: The type of unit for which to create its relevant class.
        player: The player class object defining the current player.
    
    Returns:
        The relevant subclass of the Unit class.
    """
    match unit:
        case 'Archer':
            return Archer(player)
        case 'Knight':
            return Knight(player)
        case 'Mercenary':
            return Mercenary(player)
        case 'Berserker':
            return Berserker(player)

def initialize_player(player: Player, units: list[Unit]) -> Player:
    """
    Initializes a Player class object along with its relevant attributes: bag, assigned units etc.

    Args:
        player: The player class object defining the current player.
        units: A list of Unit class objects containing the units which are used to assign a certain number to the player.

    Returns:
        The Player class object with its initialized properties. 
    """
    # Repeat until we have assigned two units to the player
    for _ in range(2):
        # Generate the random number
        random_no: int = random.randint(0, len(units) - 1)
        # Get the unit and no_of_units assigned to it
        unit, no_of_units = units[random_no][0], units[random_no][1]
        # Create two unit coins
        unit_coin_one, unit_coin_two = generate_unit_coin(unit, player), generate_unit_coin(unit, player)

        # The assigned units dictionary follows the structure '{ unit_type: [stack of class Units] }'
        player.assigned_units[unit] = []
        # Create the stack of unit coins (remembering to remove two units we inserted in the player bag)
        for _ in range(no_of_units - 2):
            player.assigned_units[unit].append(generate_unit_coin(unit, player))

        # Place the two units in the bag
        player.bag.append(unit_coin_one)
        player.bag.append(unit_coin_two)
        # Remove them from the pool of available units
        del units[random_no]
    
    # Add the royal card (one available to each player)
    royal_unit: Royal = Royal()
    player.bag.append(royal_unit)
    return player

def show_player_information(player: Player) -> bool:
    """
    Shows the current player playing, as well as the status of its recruitment units, discard pile and control tokens.

    Args:
        player: The player class object defining the current player.
    
    Returns:
        True if the game can continue, False if it has ended due to the inability to make more hands.
    """
    print(f'  ==== {player.name} ({player.symbol}) ====')
    # Other player has won if the current player can't create a new hand
    if not player.get_hand():
        return False
    player.get_recruitment_units()
    player.print_discard_pile()
    player.print_control_tokens()
    
    return True

def prompt_player_actions(board: Board, player: Player) -> bool:
    """
    Defines the logic of how the game is played, involving the relevant actions until the player hand is empty.

    Args:
        board: The Board class object, containing the grid with the unit coins.
        player: The Player class object defining the current player.

    Returns:
        True if the user has forfeited, False if it is not the case and so the game can go on.
    """
    # Prompt the user to choose three actions
    for _ in range(3):
        forfeit = board.choose_action(player)
        if forfeit:
            return True
        
    return False
        
def swap_turns(curr_player: Player, player1: Player, player2: Player) -> Player:
    """
    Returns the current player by swapping turns based on the previous current player.

    Args:
        curr_player: The current Player class object.
        player1: Player 1 class object.
        player2: Player 2 class object.

    Returns:
        The current player after doing the relevant logic.
    """
    # Make sure that a player can only play at most two rounds in row
    if curr_player.has_initiative:
        curr_player.initiative_count += 1
        if curr_player.initiative_count >= 2:
            curr_player.has_initiative = False
            curr_player.initiative_count = 0
            curr_player = player1 if curr_player == player2 else player2
    else:
        curr_player = player1 if curr_player == player2 else player2
    
    return curr_player

def get_high_scores() -> None:
    """
    Prints the high scores obtained from the database, ordered by the most recent first.
    """
    results: list = high_scores()
    
    # Print the results
    print("High scores:")
    for row in results:
        print(f"{row[0]} - {row[1]} victories on {row[2]}")


def play_game() -> None:
    """
    Contains the logic which initializes the units, players, board and allows the players to keep playing until there
    is a winner.
    """
    # Show high scores
    get_high_scores()

    # Initialize the list of units where the tuple represents (type of unit, the no. of units corresponding to it)
    units: list[tuple]= [('Archer', 4), ('Knight', 5), ('Mercenary', 5), ('Berserker', 4)]
    # Initialize players
    crow: Player = initialize_player(Player('CROW', 's'), units)
    wolf: Player = initialize_player(Player('WOLF', 'v'), units)
    # Initialize board
    board: Board = Board(crow, wolf)
    # Set random starting player
    curr_player: Player = crow if random.randint(0, 1) == 0 else wolf

    # Stop the game when there is a winning condition
    game_ended: bool = False
    
    while not game_ended:
        # Show board
        board.print_board()

        # Decide player turn
        curr_player = swap_turns(curr_player, crow, wolf)

        # Show player information (hand, recruitment pieces, discard pile & control tokens)
        # If the method returns False that means the curr_player couldn't create a hand
        # or the player forfeited, therefore ending the game
        if not show_player_information(curr_player) or prompt_player_actions(board, curr_player):
            # Swap the curr_player to the previous player since that is the winner
            curr_player = wolf if curr_player == crow else crow
            break

        # If the player control tokens have reached 0, we have a winner
        if curr_player.control_tokens == 0:
            game_ended = True


    print(f'\nThe winner of the game is {curr_player.name}!\n')


if __name__ == "__main__":
    """
    Standard python boilerplate.
    """
    # This is executed when run from the command line
    main()
