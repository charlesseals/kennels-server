import sqlite3
import json
from models import Location


LOCATIONS = [
   {
       "id": 1,
       "name": "Nashville North",
       "address": "8422 Johnson Pike"
   },
   {
       "id": 2,
       "name": "Nashville South",
       "address": "209 Emory Drive"
   },
   {
       "id": 3,
       "name": "Nashville West",
       "address": "1007 West End Blvd"
   }
]


# def get_all_locations():
#     return LOCATIONS
def get_all_locations(query_params):
   with sqlite3.connect("./kennel.sqlite3") as conn:
       conn.row_factory = sqlite3.Row
       db_cursor = conn.cursor()


       if len(query_params) == 0:
          
           count_animals = " COUNT(*) AS animals"
           group_by_location = " GROUP BY a.location_id"
          
       sql_to_execute = f"""
       SELECT
           l.id,
           l.name,
           l.address,
           a.location_id,
           {count_animals}
       FROM location l
       JOIN Animal a
           ON a.location_id = l.id
       {group_by_location}       
       """


       db_cursor.execute(sql_to_execute)
       locations = []
       dataset = db_cursor.fetchall()
       for row in dataset:
           location = Location(row['id'], row['name'], row['address'])
           location.animals = row['animals']
           locations.append(location.__dict__)
   return locations




# def get_single_location(id):
#     requested_location = None
#     for location in LOCATIONS:
#         if location["id"] == id:
#             requested_location = location
#     return requested_location
def get_single_location(id):
   with sqlite3.connect("./kennel.sqlite3") as conn:
       conn.row_factory = sqlite3.Row
       db_cursor = conn.cursor()
       db_cursor.execute("""
       SELECT
           l.id,
           l.name,
           l.address
       FROM location l
       WHERE l.id = ?
       """, ( id, ))
       data = db_cursor.fetchone()
       location = Location(data['id'], data['name'], data['address'])
       return location.__dict__








def create_location(location):
   max_id = LOCATIONS[-1]["id"]
   new_id = max_id + 1
   location["id"] = new_id
   LOCATIONS.append(location)
   return location


def delete_location(id):
   location_index = -1
   for index, location in enumerate(LOCATIONS):
       if location["id"] == id:
           location_index = index
   if location_index >= 0:
       LOCATIONS.pop(location_index)


def update_location(id, new_location):
   for index, location in enumerate(LOCATIONS):
       if location["id"] == id:
           LOCATIONS[index] = new_location
           break

