from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import random


restaurants = Blueprint('restaurants', __name__)


# 1. Post Restaurant (WORKING)
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


## 2. Get all Menu Items (WORKING)
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


## 3. Update MenuItem (WORKING)
@restaurants.route('/restaurant/<restaurant_name1>/<select_menu_item>', methods=['PUT'])
def update_menu_item(restaurant_name1, select_menu_item):
    cursor = db.get_db().cursor()

    # getting update data
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extracting the variables 
    menu_item_id = str(req_data['select_menu_item'])
    item_name = str(req_data['item_name'])
    descrip = str(req_data['item_description'])
    price = str(req_data['item_price'])

    
    update = "UPDATE Menu_Item SET item_name = '"+item_name+"', descrip = '"+descrip+"',"
    update += "price = '"+price+"' WHERE menu_item_id = "+menu_item_id+";"

    # executing and commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(update)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()

    return "success"

## 4. delete restaurant
@restaurants.route('/delete_restaurant', methods=['DELETE'])
def delete_restaurant():
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)
    

    restaurant_cancel = str(req_data['restaurant_name2'])

    # constructing the query
    # 
    # DELETE FROM Order_Table WHERE restaurant_id IN (SELECT restaurant_id FROM Restaurant WHERE restaurant_name = 'Vimbo');

    # DELETE FROM Restaurant WHERE restaurant_name = 'Vimbo';

    cancel_stmt = "DELETE FROM Order_Table WHERE restaurant_id IN (SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '"+restaurant_cancel+"');"

    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(cancel_stmt)
    #can't commit the cursor, have to commit the db s
    db.get_db().commit()

    cancel_stmt1 = "DELETE FROM Restaurant WHERE restaurant_name = '"+restaurant_cancel+"';"

    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(cancel_stmt1)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()

    return  "success"


## 5. get restaurant orders
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


## 6. get restaurant reviews
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


# 7: get average restaurant score
@restaurants.route('/avg_score/<restaurant_name>', methods=['GET'])
def get_avg_score(restaurant_name):

    cursor = db.get_db().cursor()

    insert_stmt = "select avg(score) from Restaurant_Review join Restaurant R on Restaurant_Review.restaurant_id = R.restaurant_id where restaurant_name='" + restaurant_name + "'"
    
    cursor.execute(insert_stmt)

    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# 8: get a restaurant's total earnings
@restaurants.route('/restaurant_earnings/<restaurant_name>', methods=['GET'])
def get_avg_score(restaurant_name):

    cursor = db.get_db().cursor()

    insert_stmt = "select sum(earnings) from Order_Table join Restaurant R on Order_Table.restaurant_id = R.restaurant_id where restaurant_name='" + restaurant_name + "'"
    
    cursor.execute(insert_stmt)

    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)