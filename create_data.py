#!/usr/bin/python3
""" Create database for BusInfo """

from models.schedule import Schedule
from models.route import Route
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

# Unique schedule for each 5 routes
def createRoutes(routes, urban=True, schedule_idList=schedule_idList):
    """Create Route instances and save them to the database"""
    count = 0
    if type(schedule_idList) == list:
        schedule_id = schedule_idList[0]
    else:
        schedule_id = schedule_idList
    for route in routes:
        route_data = route.split("-")
        if count % 5 == 0 and type(schedule_idList) == list and count // 5 < len(schedule_idList):
            schedule_id = schedule_idList[count // 5]
            
        route_obj = Route(
            schedule_id=schedule_id,
            line_number=int(route_data[0]),
            urban=urban,
            departure_terminus=route_data[1],
            arrival_terminus=route_data[2]
        )
        route_obj.save()
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



# Close the storage session after all tests
storage.close()


    