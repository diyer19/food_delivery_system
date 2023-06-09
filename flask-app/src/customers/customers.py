from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
import random


customers = Blueprint('customers', __name__)

# 1. Get all Customers (GET)
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

# 2. Get details of a specific customer
@customers.route('/customers/<phone_number>', methods=['GET'])
def get_customer_id(phone_number):
    cursor = db.get_db().cursor()

    # query    
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

# 3. Create a new customer (POST)
@customers.route('/new_customer', methods=['POST'])
def post_new_customer():
    current_app.logger.info('Processing form data')

    req_data = request.get_json()

    current_app.logger.info(req_data)

    # extract variables (customer info)
    first_name = req_data['customer_firstname']
    last_name = req_data['customer_lastname']
    phone_number = req_data['customer_phone']
    email = req_data['customer_email']

    # query
    insert_stmt = 'insert into Customer (first_name, last_name, phone_number, email) values ("'
    insert_stmt += first_name + '", "'
    insert_stmt += last_name + '", "'
    insert_stmt += phone_number + '", "'
    insert_stmt += email + '" )'

    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)

    db.get_db().commit()

    # extract variables (delivery address)
    street = req_data['delivery_street']
    city = req_data['delivery_city']
    state = req_data['delivery_state']
    zipcode = req_data['delivery_zip']

    # query
    insert_stmt = 'insert into Delivery_Address (street_address, state, city, zip) values ("'
    insert_stmt += street + '", "'
    insert_stmt += state + '", "'
    insert_stmt += city + '", "'
    insert_stmt += str(zipcode) + '" )'

    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)

    db.get_db().commit()

    # extract variables (payment info) 
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

    # query
    insert_stmt = 'INSERT INTO Payment_Info (payment_id, customer_id, cc, expiration, zip, cvv) '
    insert_stmt += 'VALUES (' + str(max_payment_id) + ', '
    insert_stmt += str(max_customer_id) + ', "'
    insert_stmt += cc + '", "'
    insert_stmt += expiration + '", '
    insert_stmt += str(zipcode) + ', '
    insert_stmt += str(cvv) + ')'

    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    
    db.get_db().commit()

    # extract variables (billing address)
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

    # query
    insert_stmt = 'INSERT INTO Billing_Address (payment_id, customer_id, street_address, state, city, zip) '
    insert_stmt += 'VALUES ('+ str(max_payment_id)+ ', '
    insert_stmt += str(max_customer_id)+ ', "'
    insert_stmt += street + '", "'
    insert_stmt += state + '", "'
    insert_stmt += city + '", '
    insert_stmt += str(zipcode) + ')'

    
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    
    db.get_db().commit()

    return "Success"

# 4. Update a specific customer's billing address (PUT)
@customers.route('/customers/<phone_number>/billing_address', methods=['PUT'])
def update_billing_address(phone_number):
    cursor = db.get_db().cursor()

    
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extract variables
    street = str(req_data['billing_street'])
    city = str(req_data['billing_city'])
    state = str(req_data['billing_state'])
    zipcode = str(req_data['billing_zip'])

    # query
    update = "UPDATE Billing_Address"
    update += " SET street_address = '" + street + "', city = '" + city + "', state = '" + state + "', zip = '" + zipcode + "'"
    update += " WHERE customer_id = (SELECT customer_id FROM Customer WHERE phone_number = '{0}'".format(phone_number)
    update += ")"

    cursor = db.get_db().cursor()
    cursor.execute(update)

    db.get_db().commit()

    return "success"

# 5. Udate a specific customer's delivery address (PUT)
@customers.route('/customers/<phone_number>/delivery_address', methods=['PUT'])
def update_delivery_address(phone_number):
    cursor = db.get_db().cursor()

    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extract variables 
    street = str(req_data['delivery_street'])
    city = str(req_data['delivery_city'])
    state = str(req_data['delivery_state'])
    zipcode = str(req_data['delivery_zip'])

    # query
    update = "UPDATE Delivery_Address"
    update += " SET street_address = '" + street + "', city = '" + city + "', state = '" + state + "', zip = '" + zipcode + "'"
    update += " WHERE customer_id = (SELECT customer_id FROM Customer WHERE phone_number = '{0}'".format(phone_number)
    update += ")"

    cursor = db.get_db().cursor()
    cursor.execute(update)
    
    db.get_db().commit()

    return "success"




# 6. Update a specific customer's payment info (PUT)
@customers.route('/customers/<phone_number>/payment_info', methods=['PUT'])
def update_payment_info(phone_number):
    cursor = db.get_db().cursor()

    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)


    # extract variables 
    cc = str(req_data['payment_number'])
    expiration = str(req_data['payment_expiration'])
    zipcode = str(req_data['payment_zip'])
    cvv = str(req_data['payment_cvv'])

    # query
    update = "UPDATE Payment_Info"
    update += " SET cc = '" + cc + "', expiration = '" + expiration + "', zip = '" + zipcode + "', cvv = '" + cvv + "'"
    update += " WHERE customer_id = (SELECT customer_id FROM Customer WHERE phone_number = '{0}'".format(phone_number)
    update += ")"

    cursor = db.get_db().cursor()
    cursor.execute(update)
    
    db.get_db().commit()

    return "success"


## 7. Get all Restaurants (GET)
@customers.route('/restaurants', methods=['GET'])
def get_restaurants():
    cursor = db.get_db().cursor()

    # execute query
    cursor.execute('select distinct restaurant_name as label, restaurant_name as value from Restaurant')

    column_headers = [x[0] for x in cursor.description]

    json_data = []

    theData = cursor.fetchall()
    
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


## 8. Get all menu items from a specific restaurant (GET)
@customers.route('/restaurants/<restaurant_name>', methods=['GET'])
def get_menu_items(restaurant_name):
    cursor = db.get_db().cursor()

    # query
    insert_stmt = "select menu_item_id as value, item_name as label from Menu_Item JOIN Restaurant R on Menu_Item.restaurant_id = R.restaurant_id where restaurant_name="
    insert_stmt += "'{0}'".format(restaurant_name)

    cursor.execute(insert_stmt)

    column_headers = [x[0] for x in cursor.description]

    json_data = []

    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

## 9. Get all Menu Items (GET)
@customers.route('/total/<menu_item_id>', methods=['GET'])
def get_total(menu_item_id):
    cursor = db.get_db().cursor()

    # query
    insert_stmt = "SELECT concat('$', price) AS price_1 FROM Menu_Item WHERE menu_item_id = '" + menu_item_id + "'"
    
    cursor.execute(insert_stmt)

    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

## 10. Place a New Order (POST)
@customers.route('/new_order', methods=['POST'])
def post_new_order():
    current_app.logger.info('Processing form data')

    req_data = request.get_json()

    current_app.logger.info(req_data)
    
    # extract variables 
    restaurant_name = str(req_data['Order_restaurant'])
    menu_item = str(req_data['menu_items1'])
    phone_number = str(req_data['customer_phone'])
    order_total = str(req_data['Text7'])
    order_total = order_total.replace("$", "")

    # simulating choosing a driver 
    driver_id = str(random.randint(1, 20))
    earnings = str(random.randint(10, 50))
    
    # query 
    order_stmt = "INSERT INTO Order_Table (customer_id, restaurant_id, driver_id, order_total, earnings) VALUES "
    order_stmt += "((SELECT customer_id FROM Customer WHERE phone_number = '"+phone_number+"'), "
    order_stmt += "(SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '"+restaurant_name+"'), "
    order_stmt += driver_id + "," #driver_id, should be rand_int between 1-20 
    order_stmt += order_total 
    order_stmt += ", "+earnings+");" #should be rand int     

    cursor = db.get_db().cursor()
    cursor.execute(order_stmt)
    
    db.get_db().commit()

    # query (insert into MenuItem_Order)
    insert = "INSERT INTO MenuItem_Order (order_id, restaurant_id, menu_item_id, customer_id, driver_id) VALUES ("
    insert += "(SELECT MAX(order_id)  FROM Order_Table),"
    insert +="(SELECT restaurant_id FROM Restaurant WHERE restaurant_name = '"+restaurant_name+"'),"
    insert += menu_item+","
    insert += "(SELECT customer_id FROM Customer WHERE phone_number = '"+phone_number+"'), ("+driver_id+"));"

    cursor = db.get_db().cursor()
    cursor.execute(insert)
    
    db.get_db().commit()

    return  "success"

## 11. Get Orders for a specific customer (GET)
@customers.route('/orders/<phone_number>', methods=['GET'])
def get_orders(phone_number):
    cursor = db.get_db().cursor()

    # query
    select = "SELECT * FROM Order_Table JOIN Customer ON Order_Table.customer_id = Customer.customer_id"
    select += " WHERE Customer.phone_number = '" + phone_number + "';"

    cursor.execute(select)

    column_headers = [x[0] for x in cursor.description]

    json_data = []

    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

## 12. Get Orders for a specific customer (for dropdown for choosing items to order) (GET)
@customers.route('/order_id/<phone_number>', methods=['GET'])
def get_orders_id(phone_number):
    cursor = db.get_db().cursor()

    # query
    select = "SELECT order_id as label, order_id as value FROM Order_Table JOIN Customer ON Order_Table.customer_id = Customer.customer_id"
    select += " WHERE Customer.phone_number = '" + phone_number + "';"

    cursor.execute(select)

    column_headers = [x[0] for x in cursor.description]

    json_data = []

    theData = cursor.fetchall()

    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


## Cancel an Order (DELETE)
@customers.route('/cancel_order', methods=['DELETE'])
def delete_order():
    current_app.logger.info('Processing form data')

    req_data = request.get_json()

    current_app.logger.info(req_data)
    
    # extract variables
    order_cancel = str(req_data['menu_items1'])

    # query 
    cancel_stmt = "DELETE FROM Order_Table WHERE order_id = "+order_cancel

    cursor = db.get_db().cursor()
    cursor.execute(cancel_stmt)
    
    db.get_db().commit()

    return  "success"