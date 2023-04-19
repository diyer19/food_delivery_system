from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import random


restaurants = Blueprint('restaurants', __name__)


# 1. Create a new Restaurant (POST)
@restaurants.route('/new_restaurant', methods=['POST'])
def post_new_restaurant():
    current_app.logger.info('Processing form data')

    req_data = request.get_json()

    current_app.logger.info(req_data)

    # extract variables
    avg_delivery = str(random.randint(1, 20))
    restaurant_name = req_data['restaurant_name']
    phone_number = req_data['restaurant_phone']
    street_address = req_data['restaurant_street']
    city = req_data['restaurant_city']
    state = req_data['restaurant_state']
    zicode = str(req_data['restaurant_zip'])

    # query
    insert_stmt = 'insert into Restaurant (restaurant_name, phone_number, street_address, city, state, avg_delivery_time, zip) values ("'
    insert_stmt += restaurant_name + '", "'
    insert_stmt += phone_number + '", "'
    insert_stmt += street_address + '", "'
    insert_stmt += city + '", "'
    insert_stmt += state + '", "'
    insert_stmt += avg_delivery + '", "'
    insert_stmt += zicode + '" )'

    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    
    db.get_db().commit()

    return "Success"


## 2. Get all the Menu Items from a specific restaurant (GET)
@restaurants.route('/restaurants/<restaurant_name>', methods=['GET'])
def get_menu_items_restaurant(restaurant_name):
    cursor = db.get_db().cursor()

    #query
    insert_stmt = "select menu_item_id as value, item_name as label from Menu_Item JOIN Restaurant R on Menu_Item.restaurant_id = R.restaurant_id where restaurant_name="
    insert_stmt += "'{0}'".format(restaurant_name)
    cursor.execute(insert_stmt)


    column_headers = [x[0] for x in cursor.description]

    json_data = []

    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


## 3. Update a Restaurant's Menu Item (PUT)
@restaurants.route('/restaurant/<restaurant_name1>/<select_menu_item>', methods=['PUT'])
def update_menu_item(restaurant_name1, select_menu_item):
    cursor = db.get_db().cursor()

    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extract variables
    menu_item_id = str(req_data['select_menu_item'])
    item_name = str(req_data['item_name'])
    descrip = str(req_data['item_description'])
    price = str(req_data['item_price'])

    # query
    update = "UPDATE Menu_Item SET item_name = '"+item_name+"', descrip = '"+descrip+"',"
    update += "price = '"+price+"' WHERE menu_item_id = "+menu_item_id+";"

    cursor = db.get_db().cursor()
    cursor.execute(update)

    db.get_db().commit()

    return "success"

## 4. Delete a Restaurant (DELETE)
@restaurants.route('/delete_restaurant', methods=['DELETE'])
def delete_restaurant():
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)
    
    #extract data
    restaurant_cancel = str(req_data['restaurant_name2'])

    # query (delete orders of this restaurant)
    cancel_stmt = "DELETE FROM Order_Table WHERE restaurant_id IN (SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '"+restaurant_cancel+"');"

    cursor = db.get_db().cursor()
    cursor.execute(cancel_stmt)

    db.get_db().commit()

    # delete the restaurant
    cancel_stmt1 = "DELETE FROM Restaurant WHERE restaurant_name = '"+restaurant_cancel+"';"

    cursor = db.get_db().cursor()
    cursor.execute(cancel_stmt1)
    
    db.get_db().commit()

    return  "success"


## 5. Get all the orders of a restaurant (GET)
@restaurants.route('/orders/<restaurant_name>', methods=['GET'])
def get_restaurant_orders(restaurant_name):
   
   cursor = db.get_db().cursor()

    # query
   insert_stmt = "SELECT order_id, order_total, time_placed, time_delivered, time_picked_up FROM Order_Table WHERE restaurant_id = (SELECT restaurant_id FROM Restaurant WHERE restaurant_name = "
   insert_stmt += "'{0}'".format(restaurant_name) + ")"

   cursor.execute(insert_stmt)

   column_headers = [x[0] for x in cursor.description]

   json_data = []

   theData = cursor.fetchall()

   for row in theData:
       json_data.append(dict(zip(column_headers, row)))


   return jsonify(json_data)


## 6. Get all the reviews of a restaurant (GET)
@restaurants.route('/restaurant_reviews/<restaurant_name>', methods=['GET'])
def get_restaurant_reviews(restaurant_name):
   
   cursor = db.get_db().cursor()

    # query
   insert_stmt = "SELECT score, review, review date FROM Restaurant_Review WHERE restaurant_id = (SELECT restaurant_id FROM Restaurant WHERE restaurant_name ="
   insert_stmt += "'{0}'".format(restaurant_name) + ")"

   cursor.execute(insert_stmt)

   column_headers = [x[0] for x in cursor.description]

   json_data = []

   theData = cursor.fetchall()

   for row in theData:
       json_data.append(dict(zip(column_headers, row)))

   return jsonify(json_data)


# 7: Get the average review score of a restaurant (GET)
@restaurants.route('/avg_score/<restaurant_name>', methods=['GET'])
def get_avg_score(restaurant_name):

    cursor = db.get_db().cursor()

    #query
    insert_stmt = "select avg(score) from Restaurant_Review join Restaurant R on Restaurant_Review.restaurant_id = "
    insert_stmt += "R.restaurant_id where restaurant_name='"+restaurant_name+"';"

    cursor.execute(insert_stmt)

    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# 8: Get the total earnings of a restaurant (GET)
@restaurants.route('/restaurant_earnings/<restaurant_name>', methods=['GET'])
def get_total_earnings(restaurant_name):

    cursor = db.get_db().cursor()

    # query
    insert_stmt = "select sum(earnings) from Order_Table join Restaurant R on Order_Table.restaurant_id = R.restaurant_id where restaurant_name='" + restaurant_name + "'"
    
    cursor.execute(insert_stmt)

    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)