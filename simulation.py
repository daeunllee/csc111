"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate
an entire playthrough of the game. Please consult the project handout for
instructions and details.

You can copy/paste your code from Assignment 1 into this file, and modify it as
needed to work with your game.

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
from event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """
        Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from the location at initial_location_id
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        event = Event(id_num=initial_location_id, description=self._game.get_location().long_description,
                      next_command=None)
        self._events.add_event(event)
        # Hint: self._game.get_location() gives you back the current location

        self.generate_events(commands, self._game.get_location())
        # Hint: Call self.generate_events with the appropriate arguments

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """
        Generate events in this simulation, based on current_location and commands, a valid list of commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from current_location
        """

        for command in commands:
            if command in current_location.available_commands:
                next_loc_id = current_location.available_commands[command]
            else:
                next_loc_id = current_location.id_num
            next_loc = self._game.get_location(next_loc_id)
            event = Event(id_num=next_loc.id_num,
                          description=next_loc.long_description, next_command=None)
            self._events.add_event(event, command)
            current_location = next_loc

        # Hint: current_location.available_commands[command] will return the next location ID resulting from executing
        # <command> while in <current_location_id>

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.
        """
        # Note: We have completed this method for you. Do NOT modify it for A1.

        return self._events.get_id_log()

    def run(self) -> None:
        """
        Run the game simulation and print location descriptions.
        """
        # Note: We have completed this method for you. Do NOT modify it for A1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    })

    win_walkthrough = ["take", "go south", "go west", "take", "go east", "take", "read", "go east", "dig", "dig up",
                       "dig left", "dig right", "dig down", "dig up", "take", "go west", "go north", "read", "go north",
                       "take", "go east", "read", "take", "go west", "go south", "go south", "go west", "inventory"]
    expected_log = [1, 1, 5, 6, 6, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 5, 1, 1, 2, 2, 3, 3, 3, 2, 1, 5, 6, 6]
    # Uncomment the line below to test your walkthrough
    sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough)
    assert expected_log == sim.get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = ["go north", "go south", "read", "look", "inventory", "go north", "go south", "read", "look",
                 "inventory", "go north", "go south", "read", "look", "inventory", "go north", "go south", "read",
                 "look", "inventory", "go north", "go south", "read", "look", "inventory", "go north", "go south",
                 "read", "look", "inventory", "go north", "go south", "read", "look", "inventory", "go north",
                 "go south", "read", "look", "inventory", "go north", "go south", "read", "look", "inventory",
                 "go north", "go south", "read", "look", "inventory", "go north", "go south", "read", "look",
                 "inventory", "go north", "go south", "read", "look", "inventory", "go north", "go south", "read",
                 "look", "inventory", "go north", "go south", "read", "look", "inventory", "go north", "go south",
                 "read", "look", "inventory", "go north", "go south", "read", "look", "inventory", "go north",
                 "go south", "read", "look", "inventory", "go north", "go south", "read", "look", "inventory",
                 "go north", "go south", "read", "look", "inventory", "go north", "go south", "read", "look",
                 "inventory"]
    expected_log = [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1,
                    1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1,
                    2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1,
                    1, 1]
    # Uncomment the line below to test your demo
    sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    assert expected_log == sim.get_id_log()

    inventory_demo = ["take", "inventory", "go north", "go east", "read", "take", "inventory"]
    expected_log = [1, 1, 1, 2, 3, 3, 3, 3]
    sim = AdventureGameSimulation('game_data.json', 1, inventory_demo)
    assert expected_log == sim.get_id_log()

    scores_demo = ["take", "score", "go south", "go west", "take", "score", "go east", "go north", "go north",
                   "take", "score"]
    expected_log = [1, 1, 1, 5, 6, 6, 6, 5, 1, 2, 2, 2]
    sim = AdventureGameSimulation('game_data.json', 1, scores_demo)
    assert expected_log == sim.get_id_log()

    read_demo = ["take", "read", "go north", "read", "go east", "read", "take"]
    expected_log = [1, 1, 1, 2, 2, 3, 3, 3]
    sim = AdventureGameSimulation('game_data.json', 1, read_demo)
    assert expected_log == sim.get_id_log()

    order_drink_demo = ["go north", "order a drink", "coffee", "venti", "hot"]
    expected_log = [1, 2, 2, 2, 2, 2]
    sim = AdventureGameSimulation('game_data.json', 1, order_drink_demo)
    assert expected_log == sim.get_id_log()

    dig_demo = ["go south", "take", "go east", "dig", "dig up", "dig left", "dig right", "dig down", "dig up", "take"]
    expected_log = [1, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4]
    sim = AdventureGameSimulation('game_data.json', 1, dig_demo)
    assert expected_log == sim.get_id_log()
    # Note: You can add more code below for your own testing purposes
