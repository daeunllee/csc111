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
        for loc_items in data['items']:
            item_obj = Item(loc_items['name'], loc_items['description'], loc_items['start_position'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """
        Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]

    def get_item(self, name: str) -> None | Item:
        """
        return Item object associated with the provided name.
        """
        for x in self._items:
            if x.name == name:
                return x
        return None


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
    drink_menu = ["order a drink", "coffee", "tea", "grande", "venti", "hot", "iced"]
    choice = None
    step = 0
    step_limit = 100
    dig_step = 0
    order_step = 0
    win_step = 500

    def display_items(g: AdventureGame) -> None:
        """
        Print a list of all items that the player currently has.
        """
        if not g.inventory:
            print("Your inventory is empty.")
        else:
            print("Your inventory contains:")
            for item in g.inventory:
                print("Name: " + item.name)


    def take_item(g: AdventureGame, loc: Location) -> None:
        """
        Update the location and player's inventory and score when picking up an item.
        """

        item = loc.items[0]
        g.inventory.append(g.get_item(item))

        if item in {"Laptop Charger", "Lucky Mug", "USB Drive"}:
            g.score += 100
        else:
            g.score += 50
        print("You have found and picked up:", item)
        loc.item_check = False


    def dig_helper(steps: int, ch: str) -> int:
        """
        return an int that represents player's progress through the snow digging minigame.
        """
        directions = {0: "dig", 1: "up", 2: "left", 3: "right", 4: "down", 5: "up"}
        if directions[steps] in ch:
            print("it's not here, but you feel like you're getting closer.")
            return steps + 1
        else:
            print("it's not here, and you've lost track of where you were digging.")
            return 0


    def dig_game(g: AdventureGame, steps: int, loc: Location) -> int:
        """
        play the digging minigame based on the player's input.
        """
        if "dig up" not in loc.available_commands:
            g.score += 50
            loc.available_commands["dig up"] = 0
            loc.available_commands["dig down"] = 0
            loc.available_commands["dig left"] = 0
            loc.available_commands["dig right"] = 0
        if steps < 5:
            return dig_helper(steps, choice)
        else:
            loc.item_check = True
            loc.available_commands.pop("dig up")
            loc.available_commands.pop("dig down")
            loc.available_commands.pop("dig left")
            loc.available_commands.pop("dig right")
            loc.available_commands.pop("dig")
            return -1


    def act(g: AdventureGame, loc: Location) -> None:
        """
        print information to the player and update the game based on what item was picked up.
        """
        item = loc.items[0]
        if item == "Powerbank":
            print(
                "Your phone is now charging. You see a message from your friend, who found your mug and left it in the "
                "Robarts dining area for you.")
            g.get_location(2).item_check = True
        elif item == "Phone":
            print("Your phone ran out of battery. You might need a powerbank for it.")
            g.get_location(6).item_check = True


    def order_drink(ch: str, steps: int) -> tuple[int, int]:
        """
        Order a personalized drink at starbucks with a list of commands. Increases the allowed amount of steps taken
        for this game.
        """
        order = {"order a drink": 0, "coffee": 10, "tea": 5, "grande": 5, "venti": 10, "iced": 5, "hot": 10}
        response = {1: "Coffee or tea?", 2: "Grande or venti?", 3: "Hot or iced?"}

        if ((steps == 0 and ch == "order a drink") or (steps == 1 and ch in {"coffee", "tea"}) or
                (steps == 2 and ch in {"grande", "venti"})):
            print(response[steps + 1])
            return order[ch], steps+1
        elif steps == 3 and (ch == "hot" or ch == "iced"):
            print("You got a nice drink and feel recharged. You're ready to put in more work.")
            return order[ch], -1
        elif steps == -1:
            print("You already got a drink today.")
            return 0, steps
        else:
            print("Not what they asked you.")
            print(response[steps])
            return 0, steps
            # Note: You may modify the code below as needed; the following starter code is just a suggestion


    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        new_event = Event(location.id_num, location.long_description)
        game_log.add_event(new_event, choice)

        if not location.visited:
            print(location.long_description)
            location.visited = True
        else:
            print(location.brief_description)

        if location.item_check:
            print(location.item_description)

        # Display possible actions at this location
        print("What to do? Choose from: look, read, inventory, score, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()

        valid_choices = set(location.available_commands) | set(menu) | set(drink_menu) | {"take"}
        while choice not in valid_choices:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)
        step += 1
        print("steps taken: " + f"{step}")

        if choice in menu:
            if choice == "log":
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            elif choice == "look":
                print(location.long_description)
            elif choice == "read":
                print(location.read_description)
                if location.id_num == 3:
                    location.item_check = True
            elif choice == "inventory":
                display_items(game)
            elif choice == "score":
                print(game.score)
            else:
                print("Thank you so much for playing!")
                break

        elif choice in drink_menu:
            if location.id_num != 2:
                print("This place doesn't take your starbucks order.")
            else:
                temp = order_drink(choice, order_step)
                step_limit += temp[0]
                order_step = temp[1]

        else:
            # Handle non-menu actions
            if "take" in choice:
                if not location.item_check:
                    print("There's no item here for you to take.")
                else:
                    take_item(game, location)
                    act(game, location)

            elif "dig" in choice:
                if any(x.name == "Gloves" for x in game.inventory):
                    dig_step = dig_game(game, dig_step, location)
                else:
                    print("The snow is too cold to touch with your bare hands.")

            elif choice in location.available_commands:
                result = location.available_commands[choice]
                game.current_location_id = result

        if step > step_limit:
            print("Your project is now overdue, but you still haven't found all the items. Game over.")
            break
        if game.score == win_step and location.id_num == 6:
            print("You found all your lost items and made it back to your dorm! Great job!")
            break
