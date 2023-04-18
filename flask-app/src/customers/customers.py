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

# Get customer details for customer with a particular number
@customers.route('/customers/<phone_number>', methods=['GET'])
def get_customer_id(phone_number):
    cursor = db.get_db().cursor()
    #cursor.execute('select * from Customer where phone_number = "{0}"'.format(phone_number))
    
    select = "SELECT c.customer_id, c.first_name, c.last_name, c.email, c.phone_number, da.street_address AS delivery_street_address, "
    select += "da.zip AS delivery_zip, da.city AS delivery_city, da.state AS delivery_state, pi.payment_id, pi.cc, pi.expiration, "
    select += "pi.zip AS payment_zip, pi.cvv, ba.street_address AS billing_street_address, ba.zip AS billing_zip, ba.city AS billing_city, "
    select += "ba.state AS billing_state FROM Customer c JOIN Delivery_Address da ON c.customer_id = da.customer_id "
    select += "JOIN Payment_Info pi ON c.customer_id = pi.customer_id JOIN Billing_Address ba ON pi.payment_id = ba.payment_id AND  "
    select += 'pi.customer_id = ba.customer_id WHERE c.phone_number = "{0}"'.format(phone_number)
    

    cursor.execute(select)

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        print(row)
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Post Customer
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

    # Delivery Address 
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

    # Payment 
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

    # Billing Address 
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

# update customer's billing_address
@customers.route('/customers/<phone_number>/billing_address', methods=['PUT'])
def update_billing_address(phone_number):
    cursor = db.get_db().cursor()

    # getting update data
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extracting the variables 
    street = str(req_data['billing_street'])
    city = str(req_data['billing_city'])
    state = str(req_data['billing_state'])
    zipcode = str(req_data['billing_zip'])

    update = "UPDATE Billing_Address"
    update += " SET street_address = '" + street + "', city = '" + city + "', state = '" + state + "', zip = '" + zipcode + "'"
    update += " WHERE customer_id = (SELECT customer_id FROM Customer WHERE phone_number = '{0}'".format(phone_number)
    update += ")"

    # executing and commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(update)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()

    return "success"

# update customer's delivery_address
@customers.route('/customers/<phone_number>/delivery_address', methods=['PUT'])
def update_delivery_address(phone_number):
    cursor = db.get_db().cursor()

    # getting update data
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extracting the variables 
    street = str(req_data['delivery_street'])
    city = str(req_data['delivery_city'])
    state = str(req_data['delivery_state'])
    zipcode = str(req_data['delivery_zip'])

    update = "UPDATE Delivery_Address"
    update += " SET street_address = '" + street + "', city = '" + city + "', state = '" + state + "', zip = '" + zipcode + "'"
    update += " WHERE customer_id = (SELECT customer_id FROM Customer WHERE phone_number = '{0}'".format(phone_number)
    update += ")"

    # executing and commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(update)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()

    return "success"




# update customer's payment info
@customers.route('/customers/<phone_number>/payment_info', methods=['PUT'])
def update_payment_info(phone_number):
    cursor = db.get_db().cursor()

    # getting update data
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extracting the variables 
    cc = str(req_data['payment_number'])
    expiration = str(req_data['payment_expiration'])
    zipcode = str(req_data['payment_zip'])
    cvv = str(req_data['payment_cvv'])

    update = "UPDATE Payment_Info"
    update += " SET cc = '" + cc + "', expiration = '" + expiration + "', zip = '" + zipcode + "', cvv = '" + cvv + "'"
    update += " WHERE customer_id = (SELECT customer_id FROM Customer WHERE phone_number = '{0}'".format(phone_number)
    update += ")"

    # executing and commiting the insert stmt 
    cursor = db.get_db().cursor()
    cursor.execute(update)
    #can't commit the cursor, have to commit the db 
    db.get_db().commit()

    return "success"


## Get all Restaurants from the DB
@customers.route('/restaurants', methods=['GET'])
def get_restaurants():
    cursor = db.get_db().cursor()
    cursor.execute('select distinct restaurant_name as label, restaurant_name as value from Restaurant')

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


## Get all Menu Items from the DB
@customers.route('/restaurants/<restaurant_name>', methods=['GET'])
def get_menu_items(restaurant_name):
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

## Get all Menu Items from the DB
@customers.route('/total/<menu_item_id>', methods=['GET'])
def get_total(menu_item_id):
    cursor = db.get_db().cursor()
    insert_stmt = "SELECT concat('$', price) AS price_1 FROM Menu_Item WHERE menu_item_id = '" + menu_item_id + "'"
    
    cursor.execute(insert_stmt)

    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

## Place a New Order
@customers.route('/new_order', methods=['POST'])
def post_new_order():
    current_app.logger.info('Processing form data')

    req_data = request.get_json()

    current_app.logger.info(req_data)

    list1 = []
    
    # extracting the variables 
    # this needs to match the widget input box names in Appsmith 
    # ex: 'product_name', 'product_description', 'product_price', etc 
    menu_items = req_data['menu_items']

    # menu_items = json.loads(menu_items)
    
    # new_list = [element.replace('\\', "") for element in menu_items]

    # for each in new_list: 
    #     print(each)
    #     list1.append(each) 

    # constructing the query 

    # insert_stmt = 'insert into Order (first_name, last_name, phone_number, email) values ("'
    # insert_stmt += first_name + '", "'
    # insert_stmt += last_name + '", "'
    # insert_stmt += phone_number + '", "'
    # insert_stmt += email + '" )'


    # # executing anad commiting the insert stmt 
    # cursor = db.get_db().cursor()
    # cursor.execute(insert_stmt)
    # #can't commit the cursor, have to commit the db 
    # db.get_db().commit()

    return list1