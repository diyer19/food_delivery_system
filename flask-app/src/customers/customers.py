from flask import Blueprint, request, jsonify, make_response
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



# post a customer
@customers.route('/new_customer', methods=['POST'])
def post_new_customer():
    curr_app.logger.info('Processing form data')

    # capture the json data from the request object
    # rewuest is the object that gets automatically created whenever the flask
    # executes this code

    # collecting data from request object
    req_data = request.get_json()

    ## print out the data in the docker logs
    curr_app.logger.info(req_data)


    # extracting the variables 
    # this needs to match the widget input box names in Appsmith 
    # ex: 'product_name', 'product_description', 'product_price', etc 
    prod_name = req_data['product_name']
    prod_description = req_data['product_description']
    prod_price = req_data['product_price']
    category = req_data['product_category']

    # constructing the query 
    insert_stmt = 'INSERT INTO products (product_name, description, list_price) VALUES ("'
    insert_stmt += prod_name + '","' + prod_description + '", ' + str(prod_price) + '", '
    insert_stmt += category + ')'
    curr_app.logger.info(insert_stmt)

    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()
    return "Success"