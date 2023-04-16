from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select company, last_name,\
        first_name, job_title, business_phone from customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from customers where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# Post  Customer
@customers.route('/new_customer', methods=['POST'])
def post_new_customer():
    current_app.logger.info('Processing form data')

    req_data = request.get_json()

    current_app.logger.info(req_data)


    # extracting the variables 
    # this needs to match the widget input box names in Appsmith 
    # ex: 'product_name', 'product_description', 'product_price', etc 
    first_name = req_data['customer_firstname']
    last_name = req_data['customer_lastname']
    phone_number = req_data['customer_phone']
    email = req_data['customer_email']

    # constructing the query 

    insert_stmt = 'insert into Customer (first_name, last_name, phone_number, email) values ("'
    insert_stmt += first_name + '", "'
    insert_stmt += last_name + '", "'
    insert_stmt += phone_number + '", "'
    insert_stmt += email + '" )'


    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()
    return "Success"

# Post Delivery Address 
@customers.route('/new_delivery_address', methods=['POST'])
def post_new_delivery_address():
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    # extracting the variables 
    # this needs to match the widget input box names in Appsmith 
    # ex: 'product_name', 'product_description', 'product_price', etc 
    street = req_data['delivery_street']
    city = req_data['delivery_city']
    state = req_data['delivery_state']
    zipcode = req_data['delivery_zip']

    # constructing the query 

    insert_stmt = 'insert into Delivery_Address (street_address, state, city, zip) values ("'
    insert_stmt += street + '", "'
    insert_stmt += state + '", "'
    insert_stmt += city + '", "'
    insert_stmt += zipcode + '" )'


    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()
    return "Success"