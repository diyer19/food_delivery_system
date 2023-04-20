# The Delivery Guys

The Delivery Guys application seeks to provide an all inclusive end-to-end food ordering solution. The app’s specifications are tailored to two user personas: customers and restaurants. The use-case this app delivers for customers (generic users) is to allow them to explore an extensive array of dining establishments. Once a user browses the available restaurants and has identified the product they would like, they can place an order on the app. Restaurant owners are able to add their restaurant to the app for the customer to select. This app also allows restaurant owners to see all the orders placed as well as see the reviews given to the restaurant. The Delivery Guys aims to consolidate the gap between these two end-users and provide an optimized food delivery ecosystem.

In order to create our food delivery system, we created our database in mySQL and used the Flask frame work in Python to develop our web application. We utilized appsmith to host our work with a functional UI.

Attached is a demo of our project: <link>

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 




