from random import randint
from typing import Optional

from constants import *

def dice_roll() -> bool:
    """ (bool): Return True 15% of the time. False otherwise. """
    return randint(0, 100) > 85

def invalid_message(move: str) -> str:
    return f'move not found: {move}'

class View:
    def __init__(self):
        pass
    def draw(
        self,
        rooms: list['Room'],
    ) -> None:
        """ Draw the current game state.
        
        Parameters:
            rooms: a list of rooms
        """
        all_rooms = []
        all_plants = []

        for room in rooms:
            all_rooms.append(ROOM_LAYOUTS[room.get_name()].get('layout'))
            plants = {}
            for plant_number in room.get_plants():
                plant = room.get_plants()[plant_number]
                if plant is not None:
                    if plant.get_age() < 3:
                        plant_name = plant.get_name()[0].lower()
                    else:
                        plant_name = plant.get_name()[0].upper()
                    room_layout = ROOM_LAYOUTS.get(room.get_name())
                    plant_position = room_layout.get('positions')[plant_number]
                    plants[plant_position] = plant_name
            all_plants.append(plants)
        
        self._draw_house(all_rooms, all_plants)

    def _draw_house(
        self,
        rooms: list[dict[tuple[int, int], str]],
        all_plants: list[dict[tuple[int, int], str]],
    ) -> None:
        """ Draw the house with all rooms.
        
        Parameters:
            rooms: a list of rooms
            all_plants: All plants that needs to be displayed
        """
        for i in range(ROOM_ROW):
            row_text = ''
            for room_index, room in enumerate(rooms):
                row_text += ' '.join(self._draw_room(room, 
                    all_plants[room_index])[i]) + f' {SEPARATOR} '
            print(row_text)

    def _draw_room(self, room: dict[tuple[int, int], str], 
        plants: dict[tuple[int, int], str]):
        room_list = []
        """ Draw a room.
        
        Parameters:
            room: the room to be drawn
            plants: All plants that needs to be displayed within the room
        """
        for row in range(ROOM_ROW):
            row_list = []
            for col in range(ROOM_COL):
                if plants.get((row, col)) is not None:
                    row_list.append(plants.get((row, col)))
                elif room.get((row, col)) is not None:
                    row_list.append(room.get((row, col)))
                else:
                    # row_list.append()
                    row_list.append(EMPTY)
                
            room_list.append(row_list)
        return room_list

    def _display_plants(self, plants: dict[int, 'Plant']):
        """ Create the message to provide information all plants.
        
        Parameters:
            plants: All plants that needs to be displayed
        """
        for plant in plants:
            if plants[plant] is not None:
                health = plants[plant].get_health()
                age = plants[plant].get_age()
                name = plants[plant].get_name()
                if plants[plant].is_dead():
                    print(f'{plant}: {name} has died and is {age} days old')
                else:
                    output = f'{plant}: {name} has {health} '
                    output += f'health and is {age} days old'
                    print(output)
            else:
                print(f'{plant}: None')

    def display_rooms(self, rooms: dict[str, 'Room']):
        """ Display information of all the rooms.
        
        Parameters:
            rooms: All the rooms to be drawn
        """
        print('Rooms:')
        for room_name in rooms:
            print(room_name)
            self._display_plants(rooms[room_name].get_plants())

    def display_inventory(self, entities: dict[str, list], entity_type: str):
        """ Display information of inventory
        
        Parameters:
            entities: Entities to be displayed.
            entity_type: 'Plant' or 'Item' depending on what needs to be 
                displayed.
        """
        print(f'Inventory {entity_type}:')
        for entity in entities:
            if len(entities[entity]) > 0:
                print(entities[entity])

    def display_room_position_information(self, room: 'Room', position: int, 
        plant: Optional['Plant']):
        """ Display information of a specific position of a specific room.
            This includes plant information if a plant is at that position.
        
        Parameters:
            room: the room that the information needs to be displayed.
            position: the position where the information is needed.
            plant: plant to be displayed, if None then only room information
                will be displayed.
        """
        room_name = room.get_name()
        pot = room.get_pot(position)
        pot_sun_level = pot.get_sun_range()
        pot_evaporation = pot.get_evaporation()
        output = ''
        output += f'The pot at {room_name} position {position} experiences: '
        output += f'\n    sun levels of {pot_sun_level} and evaporation '
        output += f'of {pot_evaporation}.'
        if plant is not None:
            plant_name = plant.get_name()
            plant_age = plant.get_age()
            plant_water = plant.get_water()
            plant_sun_level = plant.get_sun_levels()
            if plant.has_repellent():
                plant_repellent = 'has repellent'
            else: 
                plant_repellent = 'does not have repellent'
            
            if plant.is_dead():
                output += f'\n{plant_name} died here'
                output += f'\n    {plant_age} days old'
            else:
                output += f'\n{plant_name} lives here, requires sun levels of '
                output += f'{plant_sun_level}'
                output += f'\n    {plant_age} days old and water levels '
                output += f'{round(plant_water, 3)} and {plant_repellent}'
            print(output)
        else:
            print(f'No plant lives in {room_name} position {position}')