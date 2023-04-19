from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import random


restaurants = Blueprint('restaurants', __name__)


# 1. Post Restaurant
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
    zicode = str(req_data['restaurant_zip'])

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


# 2. Delete Restaurant
@restaurants.route('/remove_restaurant/<restaurant_id>', methods=['DELETE'])
def delete_restaurant():
  current_app.logger.info('Processing form data')

  req_data = request.get_json()

  current_app.logger.info(req_data)
  cursor = db.get_db().cursor()
  restaurant_id = str(req_data['restaurant_id'])
  delete_stmt = 'DELETE FROM Restaurant where restaurant_id='
  delete_stmt += restaurant_id + ")"
  cursor.execute(delete_stmt)
  db.get_db().commit()


  return "Success"

   
    # current_app.logger.info('Processing form data')

    # req_data = request.get_json()

    # current_app.logger.info(req_data)


    # # extracting the variables 
    # # this needs to match the widget input box names in Appsmith 
    # # ex: 'product_name', 'product_description', 'product_price', etc 
    # restaurant_name = req_data['restaurant_name']
    # phone_number = req_data['restaurant_phone']
    # street_address = req_data['restaurant_street']
    # city = req_data['restaurant_city']
    # state = req_data['restaurant_state']
    # zicode = req_data['restaurant_zip']

    # # constructing the query 

    # delete_stmt = 'delete Restaurant (restaurant_name, phone_number, street_address, city, state, zip) values ("'
    # delete_stmt += restaurant_name + '", "'
    # delete_stmt += phone_number + '", "'
    # delete_stmt += street_address + '", "'
    # delete_stmt += city + '", "'
    # delete_stmt += state + '", "'
    # delete_stmt += zicode + '" )'


    # # executing anad commiting the insert stmt 
    # cursor = db.get_db().cursor()
    # cursor.execute(delete_stmt)
    # #can't commit the cursor, have to commit the db 
    # db.get_db().commit()

    # return "Success"

## 3. Create a new menu item
@restaurants.route('/new_menu_item/', methods=['POST'])
def post_new_menu_item():
  current_app.logger.info('Processing form data')
  req_data = request.get_json()
  current_app.logger.info(req_data)


  # extracting the variables
  # this needs to match the widget input box names in Appsmith
  # ex: 'product_name', 'product_description', 'product_price', etc
  restaurant_id = str(req_data['restaurant_id'])
  item_id = str(req_data['item_id'])
  item_name = str(req_data['item_name'])
  descrip = str(req_data['item_description'])
  price = str(req_data['item_price'])

  insert_stmt = 'insert into Menu_Item (menu_item_id, restaurant_id, item_name, descrip, price) values ("'
  insert_stmt += item_id + '", "'
  insert_stmt += restaurant_id + '", "'
  insert_stmt += item_name + '", "'
  insert_stmt += descrip + '", "'
  insert_stmt += price + '" )'


  
  # executing anad commiting the insert stmt
  cursor = db.get_db().cursor()
  cursor.execute(insert_stmt)
  #can't commit the cursor, have to commit the db
  db.get_db().commit()

  return "Success"




## 4. Get all Menu Items
@restaurants.route('/restaurants/<restaurant_name>', methods=['GET'])
def get_menu_items_restaurant(restaurant_name):
    cursor = db.get_db().cursor()
    insert_stmt = "select menu_item_id as value, item_name as label from Menu_Item JOIN Restaurant R on Menu_Item.restaurant_id = R.restaurant_id where restaurant_name="
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


## 5. Delete Menu Item
@restaurants.route('/remove_menu_item/<menu_item_id>', methods=['DELETE'])
def delete_menu_item(menu_item_id):
  cursor = db.get_db().cursor()
  cursor.execute('DELETE FROM Menu_Item where menu_item_id={0}'.format(menu_item_id))
  db.get_db().commit()


  return "Success"


## 6. Update MenuItem
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


## 7. Get all Reviews for this Restaurant
@restaurants.route('/restaurant_reviews/<restaurant_name>', methods=['GET'])
def get_restaurant_reviews(restaurant_name):
   
   cursor = db.get_db().cursor()

   insert_stmt = "SELECT score, review, review date FROM Restaurant_Review WHERE restaurant_id = (SELECT restaurant_id FROM Restaurant WHERE restaurant_name ="
   insert_stmt += "'{0}'".format(restaurant_name) + ")"

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


# 8. get all orders for this restaurant
@restaurants.route('/orders/<restaurant_name>', methods=['GET'])
def get_restaurant_orders(restaurant_name):
   
   cursor = db.get_db().cursor()

   insert_stmt = "SELECT order_id, order_total, time_placed, time_delivered, time_picked_up FROM Order_Table WHERE restaurant_id = (SELECT restaurant_id FROM Restaurant WHERE restaurant_name = "
   insert_stmt += "'{0}'".format(restaurant_name) + ")"

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
   

## 9. Get Restaurant Info
@restaurants.route('/info/<restaurant_name>', methods=['GET'])
def get_restaurant_info(restaurant_name):
   
   cursor = db.get_db().cursor()

   insert_stmt = "SELECT * FROM Restaurant WHERE restaurant_id = (SELECT restaurant_id FROM Restaurant WHERE restaurant_name = "
   insert_stmt += "'{0}'".format(restaurant_name) + ")"

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

