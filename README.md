# text-based-gardening-sim
Gardening simulator in python terminal.<br>

Usage:<br>
First user is prompted for the house file e.g. houses/house1.txt<br>
Then user enters a valid move.<br>
<br>
Valid moves:<br>
List information about plants and rooms: ```ls```<br>
Show information of a given plant: ```ls {room name} {position}```<br>
Move a plant from a room to another room: ```m {from room name} {from position} {to room name} {to position}```<br>
Plant a plant: ```p {plant name} {room name} {position}```<br>
Water a pot in a certain room: ```w {room name} {position}```<br>
Add an item to be applied to a position: ```a {room name} {position}```<br>
Swap two plants: ```s {from room name} {from position} {to room name} {to position}```<br>
Removes a plant: ```rm {room name} {position}```<br>
Progress to the next day: ```n```
