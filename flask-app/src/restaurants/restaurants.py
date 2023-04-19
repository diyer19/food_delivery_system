from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


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
    restaurant_name = req_data['restaurant_name']
    phone_number = req_data['restaurant_phone']
    street_address = req_data['restaurant_street']
    city = req_data['restaurant_city']
    state = req_data['restaurant_state']
    zicode = req_data['restaurant_zip']

    # constructing the query 

    insert_stmt = 'insert into Customer (restaurant_name, phone_number, street_address, city, state, zip) values ("'
    insert_stmt += restaurant_name + '", "'
    insert_stmt += phone_number + '", "'
    insert_stmt += street_address + '", "'
    insert_stmt += city + '", "'
    insert_stmt += state + '", "'
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

    delete_stmt = 'delete Customer (restaurant_name, phone_number, street_address, city, state, zip) values ("'
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