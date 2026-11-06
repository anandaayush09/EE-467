Time period 2018-03-01 00:00:00 - 2019-04-30 23:59:00

Labels of the data files:
Year: The year.
Mouth: The mouth.
Time: Time of day, in UTC time.
DayID: random generated identifier.
Time: Time of day, in UTC time.
Workday: Workday number 1 if workday and 0 if not.

Two versions of the data, original and upsampled, can be found marked with original and filleddata respectively.

File:                                | Description:
=====================================|============================================================
roominfo.txt                         | Room information
co2_room_x.csv                       | Room CO2 [ppm] for room X
humidity_room_x.csv                  | Room relative humidity [%] for room X
illuminance_room_x.csv               | Room level illuminance[lux] for room X
occupant_data_room_x.csv     	     | Camera-based occupancy [persons] for room X
occupant_count_cam1_BW_room_x.csv    | Camera-based occupancy leaving the room using entrance 1  [persons] for room X
occupant_count_cam1_FW_room_x.csv    | Camera-based occupancy entering the room using entrance 1 [persons] for room X
occupant_count_cam2_BW_room_x.csv    | Camera-based occupancy leaving the room using entrance 2  [persons] for room X
occupant_count_cam2_FW_room_x.csv    | Camera-based occupancy entering the room using entrance 2 [persons] for room X
temperature_room_x.csv      	     | Room temperature [C] for room X
vav_data_room_x.csv                  | Damper openness [%] for room X
brick_generator.py                   | Script for generating brick graph
brick_graph.ttl                      | Generated brick graph represented in the turtle format