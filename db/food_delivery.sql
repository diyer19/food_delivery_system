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




CREATE TABLE Restaurant (
    restaurant_id int PRIMARY KEY,
    restaurant_name varchar(50) not null,
    phone_number varchar(50) not null UNIQUE,
    avg_delivery_time int not null,
    street_address varchar(100) not null,
    city varchar(50) not null,
    state varchar(50) not null,
    zip int not null
);


CREATE TABLE Delivery_Person (
    driver_id int not null PRIMARY KEY,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    phone_number varchar(50) not null UNIQUE,
    email varchar(100) not null,
    street_address varchar(100) not null,
    city varchar(50) not null,
    state varchar(50) not null,
    zip int not null,
    mode_transportation varchar(50) not null
);


CREATE TABLE Delivery_Rating (
    driver_id int,
    customer_id int,
    delivery_id int,
    review text,
    delivery_time datetime default current_timestamp not null,
    score float not null,
    PRIMARY KEY(driver_id,customer_id,delivery_id),
    FOREIGN KEY (driver_id) REFERENCES Delivery_Person(driver_id) on delete cascade on update cascade,
    FOREIGN KEY(customer_id) REFERENCES Customer(customer_id) on delete cascade on update cascade
);


CREATE TABLE Screening (
    driver_id int,
    screening_id int,
    valid_gov_id boolean not null,
    convicted_felon boolean not null,
    above_18 boolean not null,
    SSN int not null,
    PRIMARY KEY(driver_id, screening_id),
    FOREIGN KEY (driver_id) REFERENCES Delivery_Person(driver_id) on delete cascade on update cascade
);




CREATE TABLE Delivery_Address (
    customer_id int,
    street_address varchar(100) not null,
    state varchar(50) not null,
    city varchar(50) not null,
    zip int not null,
    PRIMARY KEY(customer_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) on delete cascade on update cascade
);





CREATE TABLE Payment_Info (
    customer_id int,
    payment_id int,
    cc varchar(100) not null,
    zip varchar(50) not null,
    expiration int not null,
    cvv datetime not null,
    PRIMARY KEY(customer_id, payment_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) on update cascade on delete cascade
);


CREATE TABLE Billing_Address (
    payment_id int,
    customer_id int,
    street_address varchar(100) not null,
    state varchar(50) not null,
    city varchar(50) not null,
    zip int not null,
    PRIMARY KEY(customer_id, payment_id),
    FOREIGN KEY (customer_id, payment_id) REFERENCES Payment_Info(customer_id, payment_id)  on delete cascade on update cascade
);




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



CREATE TABLE Menu_Item (
    restaurant_id int,
    menu_item_id int,
    item_name varchar(50) not null,
    descrip text,
    price float not null,
    order_id int,
    PRIMARY KEY(restaurant_id, menu_item_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) on delete cascade on update cascade
);




CREATE TABLE Common_Allergens(
    restaurant_id int,
    menu_item_id int,
    allergen varchar(100),
    PRIMARY KEY(restaurant_id, menu_item_id),
    FOREIGN KEY (restaurant_id, menu_item_id) REFERENCES Menu_Item(restaurant_id, menu_item_id) on delete cascade on update cascade
);




CREATE TABLE Restaurant_Review (
    customer_id int,
    restaurant_id int,
    review_id int,
    score float not null,
    review text,
    review_date datetime default current_timestamp not null,
    PRIMARY KEY(customer_id, restaurant_id, review_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) on delete cascade on update cascade,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) on delete cascade on update cascade

);



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
