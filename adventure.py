"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: The ID number of player's current location.
        - inventory: A list of all Item objects the player has found/taken.
        - score: Total numerical score of the player depending on what items the player has picked up.

    Representation Invariants:
        - self.current_location_id >= 1
        - self.score >= 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    inventory: list[Item]
    score: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.inventory = []
        self.score = 0

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """
        Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects.
        """

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['read_description'],
                                    loc_data['item_description'], loc_data['available_commands'],
                                    loc_data['item_check'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        for loc_items in data['items']:
            item_obj = Item(loc_items['name'], loc_items['description'], loc_items['start_position'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """
        Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]




if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "read", "inventory", "score", "log", "quit"]  # Regular menu options available at each location
    choice = None
    step = 0
    dig_step = 0

    def display_items(game: AdventureGame) -> None:
        """
        Print a list of all items that the player currently has.
        """
        if game.inventory == []:
            print("Your inventory is empty.")
        else:
            print("Your inventory contains:")
            for item in game.inventory:
                print("Name: " + item)
                print("Item Points: " + str(item.target_points))

    def take_item(location: Location) -> None:
        """
        Update the location and player's inventory and score when picking up an item.
        """

        item = location.items[0]:
        game.inventory.append(item)
        if item == "Phone":
            pass
        elif (item == "Laptop Charger") or (item == "Lucky Mug") or (item == "USB Drive"):
            game.score += 100
        else:
            game.score += 50
        print("You have found and picked up:", item)
        location.item_check = True
    def dig_game(step: int, ch: str) -> int:
        """
        return an int that represents player's progress through the snow digging minigame.
        """
        directions = {0: "dig", 1: "up", 2: "left", 3: "right", 4: "down", 5: "up"}
        if directions[step] in ch:
            print("it's not here, but you feel like you're getting closer.")
            return step + 1
        else:
            print("it's not here, and you've lost track of where you were digging.")
            return 0
            
    def dig(location: Location) -> None:
        """
        play the digging minigame based on the player's input.
        """
        if "dig up" not in location.available_commands:
            location.available_commands["dig up"] = 0
            location.available_commands["dig down"] = 0
            location.available_commands["dig left"] = 0
            location.available_commands["dig right"] = 0
        if dig_step < 6:
            dig_step = dig_game(dig_step, choice)
        else:
            location.item_check = True
            take_item(location)
            location.available_commands.pop("dig up")
            location.available_commands.pop("dig down")
            location.available_commands.pop("dig left")
            location.available_commands.pop("dig right")
            location.available_commands.pop("dig")
            
    def act(location: Location) -> None:
        """
        print information to the player and update the game based on what item was picked up.
        """
        item = location.item[0]
        if item == "Powerbank":
            print("Your phone is now charging. You see a message from your friend, who found your mug and left it in the Robarts dining area for you.")
            game.get_location(3).item_check = True
        elif item == "Phone"
            print("Your phone ran out of battery. You might need a powerbank for it.")
            game.get_location(6).item_check = True
            

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        new_event = Event(location.id_num, location.long_description)
        game_log.add_event(new_event, choice)

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        if not location.visited:
            print(location.long_description)
            location.visited = True
        else:
            print(location.brief_description)
            
        if location.item_check:
            print(location.item_description)

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu and choice == "take":
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
        step += 1
        print("steps taken: " + f"{step}")

        if step > 60:
            print("The day is over and you haven't found all your items. Game over.")
            break
        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            if choice == "log":
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            elif choice == "look":
                print(location.long_description)
            elif choice == "read":
                print(location.read_description)
                if location.id_num == 3:
                    print(location.read_description)
                    location.item_check == True
            elif choice == "inventory":
                display_items(game)
            elif choice == "score":
                print(game.score)
            else:
                print("Thank you so much for playing!")
                break


        else:
            # Handle non-menu actions
            if "move" in choice:
                result = location.available_commands[choice]
                game.current_location_id = result
                
            elif "take" in choice:
                if not location.item_check:
                    print("There's no item here for you to take.")
                else:
                    take_item(location)
                    act(location)


            elif "dig" in choice:
                if any(x == "Gloves" for x in game.inventory):
                    dig()
                else:
                    print("The snow is too cold to touch with your bare hands.")
            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            


            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game
