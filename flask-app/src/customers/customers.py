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


    # executing and commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()
    return "Success"

# Post Billing Address 
@customers.route('/new_billing_address', methods=['POST'])
def post_new_billing_address():
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    # extracting the variables 
    # this needs to match the widget input box names in Appsmith 
    # ex: 'product_name', 'product_description', 'product_price', etc 
    street = req_data['billing_street']
    city = req_data['billing_city']
    state = req_data['billing_state']
    zipcode = req_data['billing_zip']

    # Getting Max Values 
    cursor = db.get_db().cursor()
    cursor.execute("SELECT COALESCE(MAX(customer_id), 0) FROM Billing_Address")
    result = cursor.fetchone()
    max_customer_id = int(result[0]) + 1

    cursor = db.get_db().cursor()
    cursor.execute("SELECT COALESCE(MAX(payment_id), 0) FROM Billing_Address")
    result = cursor.fetchone()
    max_payment_id = int(result[0]) + 1

    # Constructing insert statement
    insert_stmt = 'INSERT INTO Billing_Address (payment_id, customer_id, street_address, state, city, zip) '
    insert_stmt += 'VALUES ('+ str(max_payment_id)+ ', '
    insert_stmt += str(max_customer_id)+ ', "'
    insert_stmt += street + '", "'
    insert_stmt += state + '", "'
    insert_stmt += city + '", '
    insert_stmt += zipcode + ')'

    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()
    return "Success"

# Post Payment Info 
@customers.route('/new_payment_info', methods=['POST'])
def post_new_payment_info():
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    # extracting the variables 
    cc = req_data['payment_number']
    expiration = req_data['payment_expiration']
    zipcode = req_data['payment_zip']
    cvv = req_data['payment_cvv']

    # Getting Max Values 
    cursor = db.get_db().cursor()
    cursor.execute("SELECT COALESCE(MAX(customer_id), 0) FROM Payment_Info")
    result = cursor.fetchone()
    max_customer_id = int(result[0]) + 1

    cursor = db.get_db().cursor()
    cursor.execute("SELECT COALESCE(MAX(payment_id), 0) FROM Payment_Info")
    result = cursor.fetchone()
    max_payment_id = int(result[0]) + 1

    # Constructing insert statement
    insert_stmt = 'INSERT INTO Payment_Info (payment_id, customer_id, cc, expiration, zip, cvv) '
    insert_stmt += 'VALUES (' + str(max_payment_id) + ', '
    insert_stmt += str(max_customer_id) + ', "'
    insert_stmt += cc + '", "'
    insert_stmt += expiration + '", '
    insert_stmt += zipcode + ', '
    insert_stmt += cvv + ')'

    # executing anad commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()
    return "Success"