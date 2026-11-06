#!/usr/bin/env python
from rdflib import Graph, Namespace, URIRef, Literal
import rdflib
import json

RDF        = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS       = Namespace('http://www.w3.org/2000/01/rdf-schema#')
OWL        = Namespace('http://www.w3.org/2002/07/owl#')
BRICK      = Namespace('http://buildsys.org/ontologies/Brick#')
BRICKFRAME = Namespace('http://buildsys.org/ontologies/BrickFrame#')
BRICKTAG   = Namespace('http://buildsys.org/ontologies/BrickTag#')

# The occupant Brick namespace
NS         = Namespace('http://occupancy#')

# just a wrapping method for creating the graph and related stuff...
def model ():
    g = Graph()

    brickpath = lambda filename: 'var/'+filename
    g.parse(brickpath('Brick.ttl'), format='turtle')
    g.parse(brickpath('BrickFrame.ttl'), format='turtle')
    g.parse(brickpath('BrickTag.ttl'), format='turtle')

    g.bind('rdf'  , RDF)
    g.bind('rdfs' , RDFS)
    g.bind('owl'  , OWL)
    g.bind('brick', BRICK)
    g.bind('bf'   , BRICKFRAME)
    g.bind('btag' , BRICKTAG)
    g.bind('ns', NS)

    return g

# The actual brick model, as a graph
g = model()

# The Rooms
room_1 = NS['/rooms/1']
g.add((room_1, RDF.type, BRICK['Room']))

room_2 = NS['/rooms/2']
g.add((room_2, RDF.type, BRICK['Room']))

room_3 = NS['/rooms/3']
g.add((room_3, RDF.type, BRICK['Room']))

#The building
building = NS['/buildings/1']
g.add((building, RDF.type, BRICK['Building']))
g.add((building, BRICKFRAME['Contains'], room_1))
g.add((building, BRICKFRAME['Contains'], room_2))
g.add((building, BRICKFRAME['Contains'], room_3))

# The virtual occupant sensors
v_sensor = NS['/occ_sensors/1']
g.add((v_sensor, RDF.type, BRICK['Occupancy_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_1))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['occupant_count_room_1.csv']))

v_sensor = NS['/occ_sensors/2']
g.add((v_sensor, RDF.type, BRICK['Occupancy_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_2))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['occupant_count_room_2.csv']))

v_sensor = NS['/occ_sensors/3']
g.add((v_sensor, RDF.type, BRICK['Occupancy_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_3))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['occupant_count_room_3.csv']))

# The CO2 sensors
v_sensor = NS['/co2_sensors/1']
g.add((v_sensor, RDF.type, BRICK['CO2_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_1))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['co2_room_1.csv']))

v_sensor = NS['/co2_sensors/2']
g.add((v_sensor, RDF.type, BRICK['CO2_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_2))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['co2_room_2.csv']))

v_sensor = NS['/co2_sensors/3']
g.add((v_sensor, RDF.type, BRICK['CO2_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_3))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['co2_room_3.csv']))

# The humidity sensors
v_sensor = NS['/humidity_sensors/1']
g.add((v_sensor, RDF.type, BRICK['Humidity_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_1))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['humidity_room_1.csv']))

v_sensor = NS['/humidity_sensors/2']
g.add((v_sensor, RDF.type, BRICK['Humidity_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_2))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['humidity_room_2.csv']))

v_sensor = NS['/humidity_sensors/3']
g.add((v_sensor, RDF.type, BRICK['Humidity_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_3))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['humidity_room_3.csv']))

# The Illuminance sensors
v_sensor = NS['/illuminate_sensors/1']
g.add((v_sensor, RDF.type, BRICK['Illuminance_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_1))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['illuminance_room_1.csv']))

v_sensor = NS['/illuminate_sensors/2']
g.add((v_sensor, RDF.type, BRICK['Illuminance_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_2))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['illuminance_room_2.csv']))

v_sensor = NS['/illuminate_sensors/3']
g.add((v_sensor, RDF.type, BRICK['Illuminance_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_3))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['illuminance_room_3.csv']))

# The Temperature sensors
v_sensor = NS['/temperature_sensors/1']
g.add((v_sensor, RDF.type, BRICK['Temperature_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_1))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['temperature_room_1.csv']))

v_sensor = NS['/temperature_sensors/2']
g.add((v_sensor, RDF.type, BRICK['Temperature_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_2))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['temperature_room_2.csv']))

v_sensor = NS['/temperature_sensors/3']
g.add((v_sensor, RDF.type, BRICK['Temperature_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_3))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['temperature_room_3.csv']))

# The VAVs
vav_1 = NS['/vavs/1']
g.add((vav_1, RDF.type, BRICK['VAV']))
g.add((vav_1, BRICKFRAME['Feeds'], room_1))

v_sensor = NS['/damper_sensors/1']
g.add((v_sensor, RDF.type, BRICK['VAV_Damper_Position_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_1))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['vav_room_1.csv']))
g.add((v_sensor, BRICKFRAME['isPartOf'], vav_1))

vav_2 = NS['/vavs/2']
g.add((vav_2, RDF.type, BRICK['VAV']))
g.add((vav_2, BRICKFRAME['Feeds'], room_2))

v_sensor = NS['/damper_sensors/2']
g.add((v_sensor, RDF.type, BRICK['VAV_Damper_Position_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_2))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['vav_room_2.csv']))
g.add((v_sensor, BRICKFRAME['isPartOf'], vav_2))

vav_3 = NS['/vavs/3']
g.add((vav_3, RDF.type, BRICK['VAV']))
g.add((vav_3, BRICKFRAME['Feeds'], room_3))

v_sensor = NS['/damper_sensors/3']
g.add((v_sensor, RDF.type, BRICK['VAV_Damper_Position_Sensor']))
g.add((v_sensor, BRICKFRAME['isPointOf'], room_3))
g.add((v_sensor, BRICKFRAME['hasMeasurement'], NS['vav_room_3.csv']))
g.add((v_sensor, BRICKFRAME['isPartOf'], vav_3))

# The AHU
ahu_1 = NS['/ahus/1']
g.add((ahu_1, RDF.type, BRICK['AHU']))
g.add((ahu_1, BRICKFRAME['Feeds'], vav_1))
g.add((ahu_1, BRICKFRAME['Feeds'], vav_2))
g.add((ahu_1, BRICKFRAME['Feeds'], vav_3))

# Query the graph
query = '''
SELECT *
WHERE{
    ?sensor bf:hasMeasurement ?filename .
    ?sensor bf:isPointOf ?room .
}
'''

# Format result from graph and print
s = list(map(lambda row: list(map(lambda element: str(element), row)), g.query(query)))
result = json.dumps(s, sort_keys=True, indent=4, separators=(',', ' '))+'\r\n'
print(result)

# Export as complete turtle file
g.serialize(destination='brick_graph.ttl', format='turtle')
