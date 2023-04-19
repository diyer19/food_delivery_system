from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import random


restaurants = Blueprint('restaurants', __name__)


# Post Restaurant
@restaurants.route('/new_restaurant', methods=['POST'])
def post_new_restaurant():
    current_app.logger.info('Processing form data')

    req_data = request.get_json()

    current_app.logger.info(req_data)


    # extracting the variables 
    # this needs to match the widget input box names in Appsmith 
    # ex: 'product_name', 'product_description', 'product_price', etc 
    avg_delivery = str(random.randint(1, 20))
    restaurant_name = req_data['restaurant_name']
    phone_number = req_data['restaurant_phone']
    street_address = req_data['restaurant_street']
    city = req_data['restaurant_city']
    state = req_data['restaurant_state']
    zicode = req_data['restaurant_zip']

    # constructing the query 

    insert_stmt = 'insert into Restaurant (restaurant_name, phone_number, street_address, city, state, avg_delivery_time, zip) values ("'
    insert_stmt += restaurant_name + '", "'
    insert_stmt += phone_number + '", "'
    insert_stmt += street_address + '", "'
    insert_stmt += city + '", "'
    insert_stmt += state + '", "'
    insert_stmt += avg_delivery + '", "'
    insert_stmt += zicode + '" )'


    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()

    return "Success"


# Delete Restaurant
@restaurants.route('/new_restaurant', methods=['DELETE'])
def delete_new_restaurant():
    current_app.logger.info('Processing form data')

    req_data = request.get_json()

    current_app.logger.info(req_data)


    # extracting the variables 
    # this needs to match the widget input box names in Appsmith 
    # ex: 'product_name', 'product_description', 'product_price', etc 
    restaurant_name = req_data['restaurant_name']
    phone_number = req_data['restaurant_phone']
    street_address = req_data['restaurant_street']
    city = req_data['restaurant_city']
    state = req_data['restaurant_state']
    zicode = req_data['restaurant_zip']

    # constructing the query 

    delete_stmt = 'delete Restaurant (restaurant_name, phone_number, street_address, city, state, zip) values ("'
    delete_stmt += restaurant_name + '", "'
    delete_stmt += phone_number + '", "'
    delete_stmt += street_address + '", "'
    delete_stmt += city + '", "'
    delete_stmt += state + '", "'
    delete_stmt += zicode + '" )'


    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(delete_stmt)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()

    return "Success"

## Create a new menu item
@restaurants.route('/new_menu_item/<phone_number>', methods=['POST'])
def post_new_menu_item(phone_number):
  current_app.logger.info('Processing form data')
  req_data = request.get_json()
  current_app.logger.info(req_data)


  # extracting the variables
  # this needs to match the widget input box names in Appsmith
  # ex: 'product_name', 'product_description', 'product_price', etc
  item_name = str(req_data['item_name'])
  descrip = str(req_data['item_description'])
  price = str(req_data['item_price'])


  # constructing the query
  insert_stmt = "insert into Menu_Item (menu_item_id, item_name, descrip, price, restaurant_id) VALUES (((select max(menu_item_id) from MenuItem_Order)+1),"
  insert_stmt += item_name + '", "'
  insert_stmt += descrip + '", "'
  insert_stmt += price + '", "'
  insert_stmt += "(SELECT distinct CONVERT((select restaurant_id from Restaurant"
  insert_stmt += "where phone_number='989-829-7577'), CHAR) from Restaurant));"
  
  # executing anad commiting the insert stmt
  cursor = db.get_db().cursor()
  cursor.execute(insert_stmt)
  #can't commit the cursor, have to commit the db
  db.get_db().commit()




## Get all Menu Items
@restaurants.route('/menu_items/<restaurant_name>', methods=['GET'])
def get_menu_items_rest(restaurant_name):
   cursor = db.get_db().cursor()
   insert_stmt = "select menu_item_id item_name from Menu_Item JOIN Restaurant R on Menu_Item.restaurant_id = R.restaurant_id where restaurant_name="
   insert_stmt += "'{0}'".format(restaurant_name)
   cursor.execute(insert_stmt)




   # grab the column headers from the returned data
   column_headers = [x[0] for x in cursor.description]


   # create an empty dictionary object to use in
   # putting column headers together with data
   json_data = []


   # fetch all the data from the cursor
   theData = cursor.fetchall()


   # for each of the rows, zip the data elements together with
   # the column headers.
   for row in theData:
       json_data.append(dict(zip(column_headers, row)))


   return jsonify(json_data)




## Delete Menu Item
@restaurants.route('/restaurant/<menu_item_id>', methods=['DELETE'])
def delete_menu_item(menu_item_id):
  cursor = db.get_db().cursor()
  cursor.execute('DELETE FROM Menu_Item where menu_item_id=”{0}”'.format(menu_item_id))
  db.get_db().commit()


  return "Success"


## Update MenuItem
@restaurants.route('/restaurant/<menu_item_id>', methods=['PUT'])
def update_menu_item(menu_item_id):
    cursor = db.get_db().cursor()

    # getting update data
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extracting the variables 
    name = str(req_data['menu_item_name'])
    descrip = str(req_data['menu_description'])
    price = str(req_data['menu_price'])

    update = "UPDATE Menu_Item"
    update += " SET item_name = '" + name + "', descrip = '" + descrip + "', price = '" + price + "'"
    update += " WHERE menu_item_id = '{0}'".format(menu_item_id)

    # executing and commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(update)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()

    return "success"