#!/usr/bin/python3
""" Create database for BusInfo """

from models.schedule import Schedule
from models.route import Route
from models.stop import BusStop
from models import storage
from datetime import time, timedelta


# Create Schedule instances and save them to the database
schedule1 = Schedule()


schedule2 = Schedule(
    first_departure=time(7, 0, 0),
    last_departure=time(22, 0, 0),
    duration=timedelta(hours=1),
    bus_frequency=timedelta(minutes=15)
)


schedule3 = Schedule(
    first_departure=time(6, 0, 0),
    last_departure=time(21, 0, 0),
    duration=timedelta(hours=1),
    bus_frequency=timedelta(minutes=20)
)

schedule4 = Schedule(
    first_departure=time(5, 0, 0),
    last_departure=time(20, 0, 0),
    duration=timedelta(hours=2),
    bus_frequency=timedelta(minutes=30)
)


schedule1.save()
schedule2.save()
schedule3.save()
schedule4.save()


schedule_idList = [schedule1.id, schedule2.id, schedule3.id]


# Create Route instances and save them to the database
urban_routes = [
    "01-Ain Sebaa-Gare de Train",
    "02-Ain Ariss-Bir Rami(El Hencha)",
    "03-Ain Sbaa-Place Moulay Youssef",
    "04-Hay Ouled Arfaa-Place Moulay Youssef",
    "05-Hay Ouled Arfaa-Hay Ouled Oujih",
    "06-Cité Saknina-Facultés",
    "07-Hay Lalla Meryem-Hay Oulad Mbarek",
    "08-Hay El Haouzia-Hay Lalla Meryem",
    "09-Place Lycée Mohammed V-Mehdiya Plage",
    "10-Place Lycée Mohammed V-Mehdiya Plage",
    "11-L'habita-Doha Alliance",
    "12-Bir Anzaren-Doha Alliance",
    "13-Bir Anzaren-Kasbat Mehdiya",
    "14-Facultés-Hay Oulad oujih",
    "15-Bassatine Haj Mansour-Salle Couverte Al Wahda",
    "16-Bassatine Haj Mansour-Hay Oulad oujih",
    "17-Facultés-Hay Nkhakhsa",
]

interurban_routes = [
    "30-Bir Anzaran-Sidi Taibi",
    "31-Bir Anzaran-Sidi Taibi",
    "32-Université Ibn Tofail-Oulad Bourahma",
    "33-Université Ibn Tofail-Douar Lahrayed",
    "34-Université Ibn Tofail-Sidi Allal Tazi",
]


# functions to Generate stops for routes
def createStops(line_number):
    """Generate a list of stop names for a route"""
    stops = []

    for i in range(1, 11):
        stops.append("Line {} Stop {}".format(line_number, i))
    return stops

# Create BusStop instances and save them to the database
def createStopInstances(route_id, stops):
    """Create BusStop instances and save them to the database"""    
    for stop in stops:
        is_terminus = False
        if stop == stops[0] or stop == stops[-1]:
            is_terminus = True
        stop_obj = BusStop(
            route_id=route_id,
            stop_number_in_route=stops.index(stop) + 1,
            stop_name=stop,
            is_terminus=is_terminus
        )
        stop_obj.save()

# Unique schedule for each 5 routes
def createRoutes(routes, urban=True, schedule_idList=schedule_idList):
    """Create Route instances and save them to the database"""
    count = 0
    
    if type(schedule_idList) == list:
        schedule_id = schedule_idList[0]
        price = 5
    else:
        schedule_id = schedule_idList
        price = 10
    for route in routes:
        route_data = route.split("-")
        if count % 5 == 0 and type(schedule_idList) == list and count // 5 < len(schedule_idList):
            schedule_id = schedule_idList[count // 5]
            price += count // 5
            
        route_obj = Route(
            schedule_id=schedule_id,
            line_number=int(route_data[0]),
            urban=urban,
            price=price,
            departure_terminus=route_data[1],
            arrival_terminus=route_data[2]
        )
        route_obj.save()
        # Generate stops for routes
        stops = createStops(route_data[0])
        createStopInstances(route_obj.id, stops)
        count += 1
	

createRoutes(urban_routes, schedule_idList=schedule_idList)
createRoutes(interurban_routes, False, schedule4.id)



print("All objects: {}".format(storage.count()))
print("Schedule objects: {}".format(storage.count(Schedule)))

first_state_id = list(storage.all(Schedule).values())[0].id
print("First Schedule: {}".format(storage.get(Schedule, first_state_id)))

print()

print("Route objects: {}".format(storage.count(Route)))

first_route_id = list(storage.all(Route).values())[0].id
print("First Route: {}".format(storage.get(Route, first_route_id)))

print()

print("BusStop objects: {}".format(storage.count(BusStop)))

first_stop_id = list(storage.all(BusStop).values())[0].id
print("First Stop: {}".format(storage.get(BusStop, first_stop_id)))



# Close the storage session after all tests
storage.close()


    