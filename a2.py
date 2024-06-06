from a2_support import *
from typing import Optional

# author = Hamza Khurram
# email_address = h.khurram@uqconnect.edu.au
# due_date = 23/09/2022

class Entity:
    """
    Provides base functionality for Plant and Item.
    """
    def get_class_name(self) -> str:
        """
        str: Returns string of the name of the class
        """
        return str(type(self).__name__)
    
    def get_id(self) -> str:
        """
        Returns the ID of the class from constants.py

        Returns:
            str: string of the ID of corresponding class.
        """
        with open("constants.py", "r") as id_file:
            for line in id_file:
                line = line.replace("_", "")
                if self.get_class_name().upper() in line:
                    line_wout_n = line.strip()
                    _, id_self = line_wout_n.split(" = ")
                    return str(id_self.strip("'"))
    
    def __str__(self) -> str:
        """
        str: Returns string representation of class
        """
        return str(self.get_id())
    
    def __repr__(self) -> str:
        """
        str: Returns representation of class
        """
        return f"{self.get_class_name()}()"


class Plant(Entity):
    """
    A subclass of Entity.
    It provides the plant's functionality.
    It contains the plant's statistics and state.
    """

    def __init__(self, name: str) -> None:
        """
        Initialises the plant's base private variables from PLANTS_DATA.
        
        Sets up the plants sun range, drink rate, health, water level, and age.

        Parameters:
            name (str): name of plant from PLANTS_DATA(constants.py)
        """
        self._name = name
        self._plant_data = PLANTS_DATA[name]

        self._drink_rate = self._plant_data['drink rate']
        self._sun_lower = self._plant_data['sun-lower']
        self._sun_upper = self._plant_data['sun-upper']

        self._water_lvl = 10.0
        self._health_lvl = 10
        self._age = 0
        self._repellent = False

    def get_name(self) -> str:
        """
        str: Return name of plant.
        """
        return self._name

    def get_health(self) -> int:
        """
        int: Returns health of plant.
        """
        return self._health_lvl

    def get_water(self) -> float:
        """
        float: Returns water level of plant.
        """
        return self._water_lvl

    def water_plant(self) -> None:
        """
        Adds 1 to the water level.
        """
        self._water_lvl += 1

    def get_drink_rate(self) -> float:	
        """
        float: Returns drink rate of plant.
        """
        return self._drink_rate

    def get_sun_levels(self) -> tuple[int, int]:	
        """
        Returns the plant's sun range.

        Returns:
            tuple[int, int]: lower and upper range of plant.
        """
        return (self._sun_lower, self._sun_upper)

    def decrease_water(self, amount: float) -> None:
        """
        Decreases water level of plant by specified amount.

        Parameters:
            amount (float): amount to decrease water level by.
        """
        self._water_lvl -= amount

    def drink_water(self) -> None:
        """
        Decreases water level by the drink rate and
        reduces health if water level is less than 0.
        """
        if self._water_lvl <= 0:
            self._health_lvl -= 1
        else:
            self._water_lvl -= self._drink_rate


    def add_health(self, amount: int) -> None:
        """
        Adds health to plant by specified amount.

        Parameters:
            amount (int): amount of health to increase by.
        """
        self._health_lvl += amount

    def decrease_health(self, amount: int = 1):
        """
        Decreases health by 1 by default, 
        otherwise it decreases health by specified amount.

        Parameters:
            amount (int, optional): specify amount of health, defaults to 1.
        """
        self._health_lvl -= amount

    def set_repellent(self, applied: bool) -> None:
        """
        Sets whether the plant has repellent.

        Parameters:
            applied (bool): True to set repellent or False to remove it.
        """
        self._repellent = applied

    def has_repellent(self) -> bool:
        """
        bool: Returns True if plant has repellent, False if no repellent.
        """
        return self._repellent

    def get_age(self) -> int:
        """
        int: Returns age of plant.
        """
        return self._age

    def increase_age(self) -> None:
        """
        Increases plant's age by 1.
        """
        self._age += 1

    def is_dead(self) -> bool:
        """
        bool: Returns True if plant's health level is less than 0,
            but False if health level is greater than 0.
        """
        if self._health_lvl <= 0:
            return True
        else:
            return False

    # The __str__ method is inherited from Entity.

    def __repr__(self) -> str:
        """
        str: Returns representation of an instance of plant.
        """
        return f"Plant('{self._name}')"


class Item(Entity):
    """
    Subclass of Entity.
    It provides an interface for Item's subclasses.
    Each subclass of Item applies an effect to the specified plant.
    """

    def apply(self, plant: 'Plant') -> None:
        """
        Applies an Item to the specifed instance of Plant.

        Parameters:
            plant (Plant): an instance of Plant to apply item to.

        Raises:
            NotImplementedError: Item cannot be applied.
                Its subclass can only be applied to Plant.
        """
        raise NotImplementedError


class Water(Item):
    """
    Subclass of Item.
    It creates an instance of water, and applies it to a plant.
    """
    def apply(self, plant: 'Plant') -> None:
        """
        Waters the specified instance of plant.
        Increases the plant's water level by 1.0.

        Parameters:
            plant (Plant): an instance of Plant to water.
        """
        plant.water_plant()


class Fertiliser(Item):
    """
    Subclass of Item.
    It creates an instance of fertiliser, and applies it to a plant.
    """
    def apply(self, plant: 'Plant') -> None:
        """
        Applies fertiliser to specified instance of Plant.
        Increases plant's health level by 1.

        Parameters:
            plant (Plant): an instance of Plant to apply fertiliser.
        """
        plant.add_health(1)


class PossumRepellent(Item):
    """
    Subclass of Item.
    It creates an instance of repellent, and applies it to a plant.
    """

    def apply(self, plant: 'Plant') -> None:
        """
        Applies repellent to specified instance of Plant.

        Parameters:
            plant (Plant): an instance of Plant to apply fertiliser.
        """
        plant.set_repellent(True)


class Inventory:
    """
    Class for base functionality of the inventory.
    It contains lists and dictionaries for the player's items and plants.
    """
    def __init__(self, initial_items: Optional[list[Item]] = None, 
        initial_plants: Optional[list[Plant]] = None) -> None:
        """
        Sets up the inventory for items and plants.
        Dictionaries are created for items and plants.

        Parameters:
            initial_items (Optional[list[Item]], optional): 
                A list of the instances of subclasses of Item.
                Defaults to None if nothing is input.
            
            initial_plants (Optional[list[Plant]], optional):
                A list of the instances of Plant.
                Defaults to None if nothing is input.
        """
        # If there is no input to Inventory, the initial lists and dictionaries
        # are empty.
        self._initial_items = []
        self._initial_plants = []
        self._items_inv = {}
        self._plants_inv = {}

        # If there are inputs to Inventory, the following code is executed.
        if initial_items != None and initial_items != []:
            # If there is input for initial_items but not initial_plants, 
            # then initial_items must be checked if it has items or plants.
            if type(initial_items[0]) == Plant:
                self._initial_plants = initial_items
            else:
                # If both inputs exist, then they are assigned to private
                # variables accordingly.
                self._initial_items = initial_items
                self._initial_plants = initial_plants
                # inital_plants can be None if there is no input for it.


        # A dictionary for items and a dictionary for plants are then 
        # initialised using the corresponding lists.

        if self._initial_items != None:
            for item in self._initial_items:
                # This adds each item to self._items_inv.
                self.add_item(item)
        
        if self._initial_plants != None:
            for plant in self._initial_plants:
                # This adds each plant to self._plants_inv.
                self.add_plant(plant)
        else:
            self._initial_plants = []

    def add_item(self, item: Item) -> None:
        """
        Adds an item to the items dictionary (self._items_inv) by creating
        a new key or appending to the existing key's list.

        Parameters:
            item (Item): an instance of a subclass of Item.
        """
        if item.get_id() not in self._items_inv:
            self._items_inv[item.get_id()] = [item]
        else:
            self._items_inv.get(item.get_id()).append(item)

    def add_plant(self, plant: Plant) -> None:
        """
        Adds an plant to the plants dictionary (self._plants_inv) by creating
        a new key or appending to the existing key's list.

        Parameters:
            plant (Plant): an instance of Plant.
        """
        if plant.get_name() not in self._plants_inv:
            self._plants_inv[plant.get_name()] = [plant]
        else:
            self._plants_inv.get(plant.get_name()).append(plant)

    def add_entity(self, entity: Item | Plant) -> None:
        """
        Adds an item or plant to their corresponding lists and dictionaries.

        Parameters:
            entity (Item | Plant): an instance of Plant or subclass of Item.
        """
        # The inbuilt issubclass() checks the class or inheretence of entity.

        if issubclass(type(entity), Item):
            self.add_item(entity)
            self._initial_items.append(entity)

        if issubclass(type(entity), Plant):
            self.add_plant(entity)
            self._initial_plants.append(entity)

    def get_entities(self, entity_type: str) -> dict[str, list[Item | Plant]]:
        """
        Gets the specified dictionary of either items or plants.

        Parameters:
            entity_type (str): 'Item' for the items dictionary or,
                'Plant' for the plants dictionary.

        Returns:
            dict[str, list[Item | Plant]]: The dictionary of items or plants.
        """
        if entity_type == 'Item':
            return self._items_inv
        elif entity_type == 'Plant':
            return self._plants_inv

    def remove_entity(self, entity_name: str) -> Optional[Item | Plant]:
        """
        Removes an instance of item or plant from their corresponding
        dictionaries and lists.

        Parameters:
            entity_name (str): To remove an item, input the item's ID.
                To remove a plant, input the plant's name.

        Returns:
            Optional[Item | Plant]: If an instance of entity was removed,
                that entity is returned. Otherwise, None is returned.
        """
        if entity_name in self._items_inv:
            temp_inv = self._items_inv
            temp_entities = self._initial_items
            pass
        elif entity_name in self._plants_inv:
            temp_inv = self._plants_inv
            temp_entities = self._initial_plants
            pass
        else:
            return None

        entity = temp_inv.get(entity_name).pop(0)
        temp_entities.pop(temp_entities.index(entity))

        if temp_inv.get(entity_name) == []:
            temp_inv.pop(entity_name)
        
        return entity

    def __str__(self) -> str:
        """
        str: Returns the string representation of Inventory.
            It returns each item's ID and plant's name and
            the number of instances for each.
        """
        # The double 'for' loop iterates through each item and each plant,
        # and adds each entity and its amount to quantities.
        plants_items = [self._items_inv, self._plants_inv]
        quantities = ""
        for entity in plants_items:
            for item in entity:
                quantities += f"{item}: {len(entity[item])}\n"
        return quantities.strip()
    
    def __repr__(self) -> str:
        """
        str: Returns the representation of Inventory.
        """
        return f"Inventory(initial_items={self._initial_items}, " \
            f"initial_plants={self._initial_plants})"


class Pot(Entity):
    """
    Subclass of Entity.
    Pot contains one instance of a plant. 
    It sets the conditions that the plant will live in, and it affects
    the plant accordingly.
    """

    def __init__(self) -> None:
        """
        Initialises an empty pot.
        Initialises its state: sun_range and evaporation rate.
        """
        self._pot = []
        self._sun_range = []
        self._evaporation_rate = None

    def set_sun_range(self, sun_range: tuple[int, int]) -> None:
        """
        Sets the sun range of the pot.

        Parameters:
            sun_range (tuple[int, int]): lowest value of sun range,
                and highest value of sun range.
        """
        self._sun_range = [sun_range[0], sun_range[1]]

    def get_sun_range(self) -> tuple[int, int]:
        """
        tuple[int, int]: Returns the sun range of the pot.
        """
        if len(self._sun_range) == 0:
            return
        else:
            return tuple(self._sun_range)

    def set_evaporation(self, evaporation: float) -> None:
        """
        Sets the evaporation rate of the pot.

        Parameters:
            evaporation (float): rate of evaporation per day.
        """
        self._evaporation_rate = evaporation

    def get_evaporation(self) -> float:
        """
        float: Returns the evaporation rate of the pot.
        """
        return self._evaporation_rate

    def put_plant(self, plant: Plant) -> None:
        """
        Puts a plant in an empty pot.
        Appends to empty pot.

        Parameters:
            plant (Plant): an instance of Plant.
        """
        if len(self._pot) == 1:
            return
        else:
            self._pot.append(plant)

    def look_at_plant(self) -> Optional[Plant]:
        """
        Optional[Plant]: Returns the instance of plant in the pot.
        """
        if len(self._pot) == 0:
            return None
        else:
            return self._pot[0]

    def remove_plant(self) -> Optional[Plant]:
        """
        Removes the plant from the pot.

        Returns:
            Optional[Plant]: returns the instance of Plant that was removed,
                but returns None of the pot was empty.
        """
        if len(self._pot) != 0:
            return self._pot.pop(0)

    def progress(self) -> None:
        """
        Progresses the state of the plant.

        Checks if the pot's conditions are suitable for the plant.
        Water level of plant is decreased based on evaporation rate,
        and drink rate.
        Health of plant is decreased if unsuitable sun range and below
        zero water level.
        Plant's age is also increased.
        """
        if self.look_at_plant() == None:
            return

        if self.look_at_plant().is_dead():
            print(f"{self.look_at_plant().get_name()} is dead")
            return
        
        # Check sun range.

        lower_sun_pot = self.get_sun_range()[0]
        upper_sun_pot = self.get_sun_range()[1]
        lower_sun_plant = self.look_at_plant().get_sun_levels()[0]
        upper_sun_plant = self.look_at_plant().get_sun_levels()[1]
        
        # At least one value of the plant's sun range must be in the
        # pot's sun range to avoid losing health.

        sun_lvl = 0
        for num in range(lower_sun_pot, upper_sun_pot+1):
            if num in range(lower_sun_plant, upper_sun_plant+1):
                sun_lvl += 1
        
        if sun_lvl < 1:
            self.look_at_plant().decrease_health()
            print(f"Poor {self.look_at_plant().get_name()} "
                "dislikes the sun levels.")

        # Decrease water level.
        # Plant.drink_water() decreases health if water level less than 0.
        # Otherwise, the plant drinks water.

        self.look_at_plant().decrease_water(self.get_evaporation())
        self.look_at_plant().drink_water()

        self.look_at_plant().increase_age()


    def animal_attack(self) -> None:
        """
        Applies effects of an animal attack to the plant.

        Decreases plant's health by 5 points if it does not have repellent.
        Otherwise, plant is not affected.
        """

        if self.look_at_plant() == None or self.look_at_plant().is_dead():
            return
        elif self.look_at_plant().has_repellent():
            print("There has been an animal attack! But luckily "
                f"the {self.look_at_plant().get_name()} has repellent.")
        else:
            self.look_at_plant().decrease_health(ANIMAL_ATTACK_DAMAGE)

            if not self.look_at_plant().is_dead():
                print(f"There has been an animal attack! "
                    f"Poor {self.look_at_plant().get_name()}.")
            else:
                print(f"There has been an animal attack! "
                    f"{self.look_at_plant().get_name()} is dead.")


    def __str__(self) -> str:
        """
        str: Returns string representation of Pot: 'U'
        """
        return self.get_class_name()
    
    # The Pot Class inherits __repr__ from Entity.


class Room:
    """
    Provides functionality for a room.

    It contains a room's layout (from constants.py).
    A room contains 4 pots.
    """
    def __init__(self, name: str) -> None:
        """
        Initialises a room with its layout and pots with positions.

        Parameters:
            name (str): name of the Room
        """
        self._room_name = name
        self._room_layout = ROOM_LAYOUTS[self._room_name]
        self._plants_position = {0: None, 1: None, 2: None, 3: None}
        self._pots_position = {0: None, 1: None, 2: None, 3: None}


    def get_plants(self) -> dict[int, Plant | None]:
        """
        Gets instances of all plants from all pots in the room.

        Returns:
            dict[int, Plant | None]: a dictionary of all plants in the room.
        """

        # Iterates through each pot and adds its plant to self._plants_position.
        for pot in self._pots_position:
            if self._pots_position[pot] != None:
                self._plants_position[pot] = \
                    self._pots_position[pot].look_at_plant()
        
        return self._plants_position
        
    def get_number_of_plants(self) -> int:
        """
        Gets the number of plant in the room.

        Returns:
            int: total number of instances of plants in the room.
        """
        num_plants = 0
        for position in self.get_plants():
            if self.get_plants().get(position) != None:
                num_plants += 1
        return num_plants

    def add_pots(self, pots: dict[int, Pot]) -> None:
        """
        Adds pots to the room (to self._pots_position).

        Parameters:
            pots (dict[int, Pot]): a dictionary of pots with positions 0 to 3.
        """
        for position in pots:
            self._pots_position[position] = pots[position]

    def get_pots(self) -> dict[int, Pot]:	
        """
        dict[int, Pot]: Returns a dictionary of pots with positions 0 to 3.
        """
        return self._pots_position

    def get_pot(self, position: int) -> Pot:
        """
        Gets the Pot at the specified position.

        Parameters:
            position (int): a position between 0 and 3.

        Returns:
            Pot: the instance of pot.
        """
        return self._pots_position.get(position)

    def add_plant(self, position: int, plant: Plant) -> None:
        """
        Adds the specified instance of Plant to the Pot 
        at the specified position if empty.

        Parameters:
            position (int): a position between 0 and 3.
            plant (Plant): the instance of Plant.
        """
        if self.get_pot(position).look_at_plant() == None:
            self.get_pot(position).put_plant(plant)
        
    def get_name(self) -> str:
        """
        str: Returns the name of the room.
        """
        return self._room_name
        
    def remove_plant(self, position: int) -> Plant | None:
        """
        Removes the instance of Plant from the Pot at the specified position.

        Parameters:
            position (int): a position between 0 and 3.

        Returns:
            Plant | None: the instance of Plant that was removed,
                otherwise returns None if no plant in the pot.
        """
        return self.get_pot(position).remove_plant()
        
    def progress_plant(self, pot: Pot) -> bool:
        """
        Progresses the plant in the pot at the specified position.

        Parameters:
            pot (Pot): a pot from positions 0 to 3.

        Returns:
            bool: True if there is a plant in the pot, but False if no plant.
        """
        if pot.look_at_plant() != None:
            pot.progress()
        return pot.look_at_plant() != None
        
    def progress_plants(self) -> None:
        """
        Progresses all plants in all pots in the room.
        """
        for pot in self.get_pots():
            if self.get_pot(pot) != None:
                self.progress_plant(self.get_pot(pot))
        
    def __str__(self) -> str:
        """
        Returns the string representation of the room.

        Returns:
            str: the name of the room.
        """
        return self.get_name()
        
    def __repr__(self) -> str:
        """
        Returns the representation of the room.

        Returns:
            str: Room({name of the room})
        """
        return f"Room('{self.get_name()}')"


class OutDoor(Room):
    """
    Subclass of room.
    Provides functionality for outdoor rooms.
    It accounts for the risk of an animal attack on the plant.
    """
    def progress_plant(self, pot: Pot) -> bool:
        """
        Progresses the plant in the pot at the specified position
        with the risk of an animal attack.

        There is a 15% chance of an animal attack on the plant.
        The plant loses 5 health points if attacked.

        Parameters:
            pot (Pot): a pot from positions 0 to 3.

        Returns:
            bool: True (and progresses plant) if there is a plant in the pot,
                but False if pot is empty.
        """
        if pot.look_at_plant() != None:
            super().progress_plant(pot)
            if dice_roll():
                pot.animal_attack()
        
        return pot.look_at_plant() != None
    
    def __repr__(self) -> str:
        """
        Returns the representation of an Outdoor Room.

        Returns:
            str: Outdoor({name of room})
        """
        return f"OutDoor('{self.get_name()}')"


def load_house(filename: str) -> tuple[list[tuple[Room, str]], dict[str, int]]:
    """ Reads a file and creates a dictionary of all the Rooms.
    
    Parameters:
        filename: The path to the file
    
    Return:
        A tuple containing 
            - a list of all Room instances amd their room name,
            - and a dictionary containing plant names and number of plants
    """
    rooms = []
    plants = {}
    items = {}
    room_count = {}

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Room'):
                _, _, room = line.partition(' - ')
                name, room_number = room.split(' ')
                room_number = int(room_number)
                if room_count.get(name) is None:
                    room_count[name] = 0
                room_count[name] += 1
                if ROOM_LAYOUTS.get(name).get('room_type') == 'Room':
                    room = Room(name)
                elif ROOM_LAYOUTS.get(name).get('room_type') == 'OutDoor':
                    room = OutDoor(name)
                rooms.append((room, name[:3] + str(room_count[name])))
                row_index = 0

            elif line.startswith('Plants'):
                _, _, plant_names = line.partition(' - ')
                plant_names = plant_names.split(',')
                for plant in plant_names:
                    plant = plant.split(' ')
                    plants[plant[0]] = int(plant[1])

            elif line.startswith('Items'):
                _, _, item_names = line.partition(' - ')
                item_names = item_names.split(',')
                for item in item_names:
                    item = item.split(' ')
                    items[item[0]] = int(item[1])

            elif len(line) > 0 and len(rooms) > 0:
                pots = line.split(',')
                positions = {}
                for index, pot in enumerate(pots):
                    sun_range, evaporation_rate, plant_name = pot.split('_')
                    pot = Pot()
                    if plant_name != 'None':
                        pot.put_plant(Plant(plant_name))
                    sun_lower, sun_upper = sun_range.split('.')
                    pot.set_evaporation(float(evaporation_rate))
                    pot.set_sun_range((int(sun_lower), int(sun_upper)))
                    positions[index] = pot
                rooms[-1][0].add_pots(positions)
                row_index += 1

    return rooms, plants, items


class Model:
    """
    Provides an interface for GardenSim to use to play the game.
    It contains an inventory and a series of rooms.
    """
    def __init__(self, house_file: str) -> None:
        """
        Initialises a model with multiple rooms and an inventory.

        load_house() initialises the rooms, pots with plants, and
        the inital items and plants for the inventory.

        Parameters:
            house_file (str): directory of the file with the house/model.
        """
        self._house_file = house_file
        self._house = load_house(house_file)
        self._rooms, self._plants, self._items = self._house
        self._n_day = 0


        # self._plants is a dictionary of plant names and quantities.
        # Thus, the loops iterates through the dictionary, and appends
        # to self._initial_plants as many times as each plant's quantity.

        self._initial_plants = []
        for plant in self._plants:
            n = 0
            while n < self._plants[plant]:
                self._initial_plants.append(Plant(plant))
                n += 1


        # self._items is a dictionary of item IDs and quantities.
        # Each item ID is compared to the IDs in all_items and it appends
        # to self._initial_items based on the quantities.

        all_items = [Water(), Fertiliser(), PossumRepellent()]
        self._initial_items = []
        for item in self._items:
            n = 0
            while n < self._items[item]:
                for a_item in all_items:
                    if item == a_item.get_id():
                        self._initial_items.append(a_item)
                n += 1

        # This initialises initial items and initial plants for the inventory.


        # The initial number of plants in each room is added and
        # recorded in self._total_plants.

        self._total_plants = 0
        for room in self.get_all_rooms():
            self._total_plants += room.get_number_of_plants()

    def get_rooms(self) -> dict[str, Room]:
        """
        Gets a dictionary of each room's key with its instance as its value.

        Returns:
            dict[str, Room]: a dictionary of all rooms.
        """
        rooms = {}
        for room in self._rooms:
            rooms[room[1]] = room[0]
        return rooms
        
    def get_all_rooms(self) -> list[Room]:
        """
        Gets all instances of room from self.get_rooms()

        Returns:
            list[Room]: a list of all of room's instances.
        """
        all_rooms = []
        for room in self.get_rooms():
            all_rooms.append(self.get_rooms().get(room))
        return all_rooms

    def get_inventory(self) -> Inventory:
        """
        Inventory: Returns user's inventory based on self._initial items and
            self._initial_plants
        """
        return Inventory(self._initial_items, self._initial_plants)

        
    def get_days_past(self) -> int:
        """
        int: Returns the number of days that have passed.
        """
        return self._n_day + 1

    def next(self, applied_items: list[tuple[str, int, Item]]) -> None:
        """
        Progresses state of the game to the next day and
        applies specified items.

        Increases the day by 1.
        Applies each specified item to each plant.
        Adds an instance of fertiliser and repellent every 3 days.
        Progresses all plants in all rooms.

        Parameters:
            applied_items (list[tuple[str, int, Item]]): a list of tuples
                with room names, positions, and ID of items to be applied.
        """
        self._n_day += 1


        # The loop iterates through each tuple and applies the item if there
        # is a plant at the specified room and position.

        for effect in applied_items:
            room_id, position, item = effect
            plant = self.get_rooms().get(room_id).get_pot(position)\
                .look_at_plant()
            if plant != None and not plant.is_dead():
                item.apply(plant)


        # A fertiliser and repellent are added every 3 days until
        # 15 days have passed.
        
        if self._n_day in range(0, 15, 3):
            self.get_inventory().add_entity(Fertiliser())
            self.get_inventory().add_entity(PossumRepellent())


        for room in self.get_all_rooms():
            room.progress_plants()


    def move_plant(self, from_room_name: str, from_position: int, 
        to_room_name: str, to_position: int) -> None: 
        """
        Moves the instance of plant from the specified position to
        the other specified position.

        Parameters:
            from_room_name (str): Room ID to move plant from.
            from_position (int): Position between 0 to 3.
            to_room_name (str): Room ID to move plant to.
            to_position (int): Position between 0 to 3.
        """
        initial_position = self.get_rooms().get(from_room_name)\
            .get_pot(from_position)

        final_position = self.get_rooms().get(to_room_name)\
            .get_pot(to_position)

        # Check if there is plant at initial and final position
        # before moving plant.

        if initial_position.look_at_plant() != None \
            and final_position.look_at_plant() == None:
            plant = initial_position.remove_plant()
            final_position.put_plant(plant)


    def plant_plant(self, plant_name: str, room_name: str, 
        position: int) -> None:
        """
        Plants the specified instance of plant in the specified position
        and room.

        Parameters:
            plant_name (str): name of plant
            room_name (str): ID of specified Room
            position (int): Position between 0 and 3.
        """
        self.get_rooms().get(room_name).add_plant(position, Plant(plant_name))


    def swap_plant(self, from_room_name: str, from_position: int, 
        to_room_name: str, to_position: int) -> None:
        """
        Swaps plants at between the specified rooms and positions.

        Parameters:
            from_room_name (str): Room ID to swap from.
            from_position (int): Position between 0 and 3.
            to_room_name (str): Room ID to swap to.
            to_position (int): Position between 0 and 3.
        """

        if [from_room_name, from_position] == [to_room_name, to_position]:
            return
        
        position_one = self.get_rooms().get(from_room_name)\
            .get_pot(from_position)
        
        position_two = self.get_rooms().get(to_room_name).get_pot(to_position)

        # Swaps plants if there is are plants at
        # both specified positions and rooms.

        if position_one.look_at_plant() != None \
            and position_two.look_at_plant() != None:
            plant_one = position_one.remove_plant()
            plant_two = position_two.remove_plant()
            position_one.put_plant(plant_two)
            position_two.put_plant(plant_one)


    def get_number_of_plants_alive(self) -> int:
        """
        Gets the current number of plants alive.

        Returns:
            int: number of alive plants.
        """
        # This double 'for' loop iterates through each room and position and
        # checks if a plant exists at each position and if that plant is alive.

        alive_plants = 0
        for room in self.get_all_rooms():
            for plant in room.get_plants():
                if room.get_plants().get(plant) != None \
                    and not room.get_plants().get(plant).is_dead():
                        alive_plants += 1
        return alive_plants

    def has_won(self) -> bool:
        """
        Returns True if player has won, but False if not.

        A player has won if the number of alive plants is more than 50% of the
        initial total number of plants after 15 days.

        Returns:
            bool: True if won, but False if player has not won.
        """
        if self.get_days_past() >= 15:
            return self.get_number_of_plants_alive() > (self._total_plants/2)
        else:
            return False

    def has_lost(self) -> bool:
        """
        Returns True if player has lost, but True if not.

        A player has lost if the number of alive plants is less than or equal
        to 50% of the inital total number of plants at any point.

        Returns:
            bool: True if lost, but False if player has not lost.
        """
        if self.get_days_past() > 1:
            return self.get_number_of_plants_alive() <= (self._total_plants/2)
    
    # Since __str__ is not implemented, __repr__ automatically
    # acts as a replacement for __str__.

    def __repr__(self) -> str:
        """
        Returns representation of the instance of Model.

        Returns:
            str: Model({house's file directory})
        """
        return f"Model('{self._house_file}')"


class GardenSim:
    """
    Provides the gameplay for the game.
    Utilises Model coordinate gameplay.
    Utilises View to draw the game and display the game's information.
    """
    def __init__(self, game_file: str, view: View) -> None:
        """
        Initialises the model and visual aspects of the game.

        It also initialises a list for applied_items to be applied when
        'n' is input.

        Parameters:
            game_file (str): file directory of the house (.txt)
            view (View): instance of View() from a2_support.py
                to display the house and other game information.
        """
        self._house = Model(game_file)
        self._view = view
        self._rooms = self._house.get_all_rooms()
        self._applied_items = []
    
    def input_user(self) -> str:
        """
        Asks the player to input their move.

        Possible moves:
            ls: lists all information about plants and inventory.

            n: progresses to the next, and applies items.
            
            ls {room ID} {position}: lists information about plant at the
                specified position.
            
            w {room ID} {position}: water a plant at a specified position.
            
            rm {room ID} {position}: removes the plant at the specified
                position.
            
            p {plant name} {room ID} {position}: plants a plant, from the
                inventory, to the specified position.
            
            a {room ID} {position} {item ID}: applies the specified item to
                the plant at the specified position, and removes the item
                from the inventory.
            
            m {from room ID} {from position} {to room ID} {to position}:
                moves a plant from one position in a room to the specified
                position and room.
            
            s {from room ID} {from position} {to room ID} {to position}:
                swaps a plant from one position in a room with another 
                plant in the specified position and room.

        Returns:
            str: player's input move
        """
        return input("Enter a move: ")
    
    def input_for_move(self, user_input: str) -> list:
        """
        Splits the player's input into a list.

        This is done to categorize the input to a certain method: one_input(),
        three_input(), four_input(), and five_input().

        Parameters:
            user_input (str): player's input from input_user()

        Returns:
            list: a list of inputs from the player's input
        """
        return user_input.split()
    
    def invalid_message(self, user_input: str) -> None:
        """
        Prints the INVALID_MOVE message with the player's input.

        Parameters:
            user_input (str): player's input from input_user()
        """
        print(INVALID_MOVE + user_input)


    def one_input(self, user_input: str) -> None:
        """
        Executes actions of a move with one input, specifically 'ls' or 'n'.

        Parameters:
            user_input (str): player's input from input_user()
        """
        move = self.input_for_move(user_input)[0]

        # Displays the state of each position and plant in each room.
        # Then it displays the inventory for plants and items.
        if move == "ls":
            self._view.display_rooms(self._house.get_rooms())
            for entity in ["Plant", "Item"]:
                self._view.display_inventory(
                    self._house.get_inventory().get_entities(entity), entity)

        # Progresses the state of all plants and applies items to the specified
        # plants. The applied items must also be cleared from the inventory.
        elif move == "n":
            self._house.next(self._applied_items)
            for effect in self._applied_items:
                _, _, item = effect
                self._house.get_inventory().remove_entity(item.get_id())
            self._applied_items.clear()

        else:
            self.invalid_message(user_input)


    def three_input(self, user_input: str) -> None:
        """
        Executes actions for moves with three inputs.

        Inputs include:
            ls {room ID} {position}
            w {room ID} {position}
            rm {room ID} {position}

        Parameters:
            user_input (str): player's input from input_user()
        """
        move, room_key, position = self.input_for_move(user_input)

        # Checks if the inputted positions are digits.
        if position.isdigit():
            position = int(position)
        else:
            self.invalid_message(user_input)
            return

        # Checks if the inputted room key and position are valid.
        if self._house.get_rooms().get(room_key) == None \
            or self._house.get_rooms().get(room_key).get_pot(position) == None:
            self.invalid_message(user_input)
            return
        

        # Displays information of specified pot.
        if move == "ls":
            plant = self._house.get_rooms().get(room_key)\
                .get_pot(position).look_at_plant()
            self._view.display_room_position_information(
                self._house.get_rooms().get(room_key), position, plant)
            
        # Adds an instance of water with the specified position to
        # applied_items for the 'n' input.
        elif move == "w":
            self._applied_items.append((room_key, position, Water()))
            
        # Removes the plant at the specified position.
        elif move == "rm": # removes plant
            plant = self._house.get_rooms().get(room_key).remove_plant(position)
            if plant != None:
                print(f"{plant.get_name()} has been removed.")
            
        else:
            self.invalid_message(user_input)


    def four_input(self, user_input: str) -> None:
        """
        Executes actions for moves with four inputs.

        Inputs include:
            p {plant name} {room ID} {position}
            a {room ID} {position} {item ID}

        Parameters:
            user_input (str): player's input from input_user()
        """
        move, input_one, input_two, input_three \
            = self.input_for_move(user_input)

        rooms = self._house.get_rooms()

        # Checks if the input meets the conditions for the 'a' move.
        # input_one must be a Room's ID.
        # input_two must be a valid position.
        # input_three must be a valid item ID.
        if rooms.get(input_one) != None \
            and input_two.isdigit() \
                and rooms.get(input_one).get_pot(int(input_two)) != None:
            position = int(input_two)
            item_id = input_three
            room_id = input_one

        # Checks if the input meets the conditions for the 'p' move.
        # input_one must be a valid plant name.
        # input_two must be a Room's ID.
        # input_three must be a valid position.
        elif rooms.get(input_two) != None \
            and input_three.isdigit() \
                and rooms.get(input_two).get_pot(int(input_three)) != None \
                    and input_one in PLANT_NAMES:
                position = int(input_three)
                plant_name = input_one
                room_id = input_two

        # Prints an invalid message if one of the inputs are invalid.
        else:
            self.invalid_message(user_input)
            return

        inv = self._house.get_inventory()

        # Appends the specified item to applied_items for the 'n'
        # input if it is in the inventory.
        if move == 'a':
            if item_id in inv.get_entities('Item'):
                item = inv.get_entities('Item').get(item_id)[0]
                self._applied_items.append((room_id, position, item))
            
        # Plants the specified plant if it is in the inventory.
        elif move == 'p':
            if plant_name in inv.get_entities('Plant') \
                and rooms.get(room_id).get_plants().get(position) == None:
                inv.remove_entity(plant_name)
                self._house.plant_plant(plant_name, room_id, position)
            pass
        else:
            self.invalid_message(user_input)


    def five_input(self, user_input: list) -> None:
        """
        Executes actions for moves with five inputs.

        Inputs include:
            m {from room ID} {from position} {to room ID} {to position}
            s {from room ID} {from position} {to room ID} {to position}

        Parameters:
            user_input (list): player's input from input_user()
        """
        move, from_room, from_position, to_room, to_position \
            = self.input_for_move(user_input)
        
        # Checks if the inputted positions are digits.
        if from_position.isdigit() and to_position.isdigit():
            from_position = int(from_position)
            to_position = int(to_position)
        else:
            self.invalid_message(user_input)
            return

        rooms = self._house.get_rooms()

        # Checks if the inputted room IDs and positions are valid.
        if rooms.get(from_room) == None \
            or rooms.get(from_room).get_pot(from_position) == None \
                or rooms.get(to_room) == None \
                    or rooms.get(to_room).get_pot(to_position) == None:
                    self.invalid_message(user_input)
                    return

        # Move a plants from one room to another.
        if move == "m":
            self._house\
                .move_plant(from_room, from_position, to_room, to_position)

        # Swaps two plants between their specified positions and rooms.
        elif move == "s":
            self._house\
                .swap_plant(from_room, from_position, to_room, to_position)
            
        else:
            self.invalid_message(user_input)


    def play(self):
        """Executes the entire game until a win or loss occurs."""

        while True:
            if self._house.has_lost() or self._house.has_won():
                break
            
            # Displays the room in a user-friendly format.
            self._view.draw(self._rooms)
            print("")

            # Asks player to input their move.
            user_input = self.input_user()

            # Converts player's input to a list.
            move_input = self.input_for_move(user_input)

            # Based on the number of inputs, the corresponding
            # method is called and the specified move is executed.

            if len(move_input) == 1:
                self.one_input(user_input)

            if len(move_input) == 3:
                self.three_input(user_input)

            if len(move_input) == 4:
                self.four_input(user_input)

            if len(move_input) == 5:
                self.five_input(user_input)
            
            if len(move_input) == 2 or len(move_input) > 5:
                self.invalid_message(user_input)
        
        if self._house.has_won():
            print(WIN_MESSAGE)
        elif self._house.has_lost():
            print(LOSS_MESSAGE)

def main():
    """ Entry-point to gameplay """
    view = View()
    house_file = input('Enter house file: ')
    garden_gnome = GardenSim(house_file, view)
    garden_gnome.play()


if __name__ == '__main__':
    main()