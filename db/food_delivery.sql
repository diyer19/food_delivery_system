
show tables;

create database food_delivery;

use food_delivery;

CREATE TABLE Customer (
    customer_id int PRIMARY KEY,
    phone_number varchar(50) not null UNIQUE,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(100) not null UNIQUE
);

INSERT INTO Customer (customer_id, phone_number, first_name, last_name, email)
VALUES (1, '449-889-8080', 'John', 'Smith', 'john_smith@gmail.com'),
       (2, '567-889-7060', 'Jane', 'Doe', 'jane_doe@gmail.com'),
       (3, '404-222-6767', 'Mary', 'Smith', 'mary_smith@gmail.com');


CREATE TABLE Restaurant (
    restaurant_id int PRIMARY KEY,
    restaurant_name varchar(50) not null,
    phone_number varchar(50) not null UNIQUE,
    avg_delivery_time int not null,
    street_address varchar(100) not null,
    city varchar(50) not null,
    state varchar(50) not null,
    zip varchar(50) not null
);

INSERT INTO Restaurant (restaurant_id, restaurant_name, phone_number, avg_delivery_time, street_address, city, state, zip)
VALUES (1, 'Bgood', '343-898-4556', 25, '12 State St','Boston','MA','02115'),
       (2, 'Tatte', '399-606-9099', 20, '67 Milk St','Boston','MA','02116'),
       (3, 'Bgood', '503-888-6232', 25, '92 Water St','Boston','MA','02115');



CREATE TABLE Delivery_Person (
    driver_id int not null PRIMARY KEY,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    phone_number varchar(50) not null UNIQUE,
    email varchar(100) not null,
    street_address varchar(100) not null,
    city varchar(50) not null,
    state varchar(50) not null,
    zip varchar(50) not null,
    mode_transportation varchar(50) not null
);

INSERT INTO Delivery_Person (driver_id, first_name, last_name, phone_number, email, street_address, city, state, zip, mode_transportation)
  VALUES (1, 'Jim', 'Patterson', '414-362-4410', 'jim.patterson@hotmail.com', '5 Broadway Dr', 'Boston', 'MA', '02118', 'car'),
  (2, 'Linda', 'Brown', '343-342-9443', 'Linda.Brown@gmail.com', '46 West St', 'Boston', 'MA', '02110', 'car'),
  (3, 'Jillian', 'Smith', '342-643-5432', 'Jill.Smith@gmail.com', '10 Dusty St', 'Boston', 'MA', '02119', 'car');


CREATE TABLE Delivery_Rating (
    driver_id int,
    customer_id int,
    delivery_id int,
    review varchar(100),
    delivery_time datetime default current_timestamp not null,
    score float not null,
    PRIMARY KEY(driver_id,customer_id,delivery_id),
    FOREIGN KEY (driver_id) REFERENCES Delivery_Person(driver_id) on delete cascade on update cascade,
    FOREIGN KEY(customer_id) REFERENCES Customer(customer_id) on delete cascade on update cascade
);

INSERT INTO Delivery_Rating (driver_id, customer_id, delivery_id, review, score)
VALUES (1, 1, 1, 'Great! Delivered 5 mins early', 5),
       (2, 2, 2, 'Forgot the sauce, but on time.', 4),
       (3, 3, 3, 'Stole my food.', 1);

CREATE TABLE Screening (
    driver_id int,
    screening_id int,
    valid_gov_id boolean not null,
    convicted_felon boolean not null,
    above_18 boolean not null,
    SSN boolean not null,
    PRIMARY KEY(driver_id, screening_id),
    FOREIGN KEY (driver_id) REFERENCES Delivery_Person(driver_id) on delete cascade on update cascade
);

INSERT INTO Screening (driver_id, screening_id, valid_gov_id, convicted_felon, above_18, SSN)
VALUES (1, 100, True, False, True, True),
       (2, 101, True, False, True, True),
       (3, 102, True, False, False, True);

CREATE TABLE Delivery_Address (
    customer_id int,
    street_address varchar(100) not null,
    state varchar(50) not null,
    city varchar(50) not null,
    zip varchar(50) not null,
    PRIMARY KEY(customer_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) on delete cascade on update cascade
);

INSERT INTO Delivery_Address (customer_id, street_address, state, city, zip)
VALUES (1, '251 Huntington Avenue', 'MA', 'Boston', '02115'),
       (2, '1040 Tremont Street', 'MA', 'Roxbury', '02120'),
       (3, '241 Huntington Avenue', 'MA', 'Boston', '02115');

CREATE TABLE Payment_Info (
    customer_id int,
    payment_id int,
    cc varchar(100) not null,
    zip varchar(50) not null,
    expiration int not null,
    cvv int not null,
    PRIMARY KEY(customer_id, payment_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) on update cascade on delete cascade
);

INSERT INTO Payment_Info (customer_id, payment_id, cc, zip, expiration, cvv)
  VALUES (1, 1, '3432839293420137', '02118', 0426, 392),
  (2, 2, '9822983409372937', '02117', 1024, 342),
  (3, 3, '3432839293420137', '02112', 0927, 234);


CREATE TABLE Billing_Address (
    payment_id int,
    customer_id int,
    street_address varchar(100) not null,
    state varchar(50) not null,
    city varchar(50) not null,
    zip varchar(50) not null,
    PRIMARY KEY(customer_id, payment_id),
    FOREIGN KEY (customer_id, payment_id) REFERENCES Payment_Info(customer_id, payment_id)  on delete cascade on update cascade
);

INSERT INTO Billing_Address (payment_id, customer_id, street_address, state, city, zip)
VALUES (1, 1, '251 Huntington Avenue', 'MA', 'Boston', '02115'),
       (2, 2, '1040 Tremont Street', 'MA', 'Roxbury', '02120'),
       (3, 3, '241 Huntington Avenue', 'MA', 'Boston', '02115');

CREATE TABLE Order_Table (
    order_id int,
    customer_id int,
    restaurant_id int,
    driver_id int,
    order_total int not null,
    earnings float,
    time_placed datetime default current_timestamp not null,
    time_delivered datetime default current_timestamp,
    time_picked_up datetime default current_timestamp,
    PRIMARY KEY (order_id, customer_id, restaurant_id, driver_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) on update cascade on delete restrict ,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) on update cascade on delete restrict,
    FOREIGN KEY (driver_id) REFERENCES Delivery_Person(driver_id) on update cascade on delete restrict
);

INSERT INTO Order_Table (order_id, customer_id, restaurant_id, driver_id, order_total, earnings)
  VALUES (1, 1, 1, 1, 34, 54.2),
  (2, 2, 2, 2, 22, 44.7),
  (3, 2, 3, 3, 52, 33.2);

CREATE TABLE Menu_Item (
    restaurant_id int,
    menu_item_id int,
    item_name varchar(50) not null,
    descrip varchar(100),
    price float not null,
    order_id int,
    PRIMARY KEY(restaurant_id, menu_item_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) on delete cascade on update cascade
);

INSERT INTO Menu_Item (restaurant_id, menu_item_id, item_name, descrip, price, order_id)
  VALUES (1, 1,'Burger', 'Cheeseburger with fries', 10.99, 1),
  (1, 2,'Salad', 'Cobb Salad', 7.99, 1),
  (2, 4,'Coffee', 'with cream and sugar', 4.99, 2),
  (2, 5,'Egg and Toast', 'scrambled eggs', 10.99, 2),
  (3, 7,'Burger', 'Cheeseburger with fries', 10.99, 3),
  (3, 8,'Bottled Water', 'Dasani', 3, 3);

CREATE TABLE Common_Allergens(
    restaurant_id int,
    menu_item_id int,
    allergen varchar(100),
    PRIMARY KEY(restaurant_id, menu_item_id),
    FOREIGN KEY (restaurant_id, menu_item_id) REFERENCES Menu_Item(restaurant_id, menu_item_id) on delete cascade on update cascade
);

INSERT INTO Common_Allergens (restaurant_id, menu_item_id, allergen)
VALUES (1, 1, 'peanuts'),
       (1, 2, 'eggs'),
       (2, 4, 'tree nuts');

CREATE TABLE Restaurant_Review (
    customer_id int,
    restaurant_id int,
    review_id int,
    score float not null,
    review varchar(100),
    review_date datetime default current_timestamp not null,
    PRIMARY KEY(customer_id, restaurant_id, review_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) on delete cascade on update cascade,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) on delete cascade on update cascade

);

INSERT INTO Restaurant_Review (customer_id, restaurant_id, review_id, score, review)
VALUES (1, 1, 1, 5, 'Quick, fast, and great food!'),
       (2, 2, 2, 3, 'messed up my order, but compd meal'),
       (3, 3, 3, 1, 'Chicken was raw');


CREATE TABLE MenuItem_Order (
    restaurant_id int,
    menu_item_id int,
    customer_id int,
    driver_id int,
    order_id int,
    PRIMARY KEY(restaurant_id, menu_item_id, customer_id, driver_id, order_id),
    FOREIGN KEY(order_id, customer_id, restaurant_id, driver_id) REFERENCES Order_Table(order_id, customer_id, restaurant_id, driver_id) on update cascade on delete cascade,
    FOREIGN KEY(restaurant_id, menu_item_id) REFERENCES Menu_Item(restaurant_id, menu_item_id) on update cascade on delete cascade
);

INSERT INTO MenuItem_Order (restaurant_id, menu_item_id, customer_id, driver_id, order_id)
VALUES (1, 1, 1, 1, 1),
       (1, 2, 1, 1, 1),
       (2, 4, 2, 2, 2),
       (2, 5, 2, 2, 2),
       (3, 7, 2, 3, 3),
       (3, 8, 2, 3, 3);












