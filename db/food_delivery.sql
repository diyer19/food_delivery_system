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

INSERT INTO Customer(customer_id,phone_number,first_name,last_name,email) VALUES
    (1,'583-299-8453','Doralia','Hyde','dhyde0@seattletimes.com')
    ,(2,'129-968-2446','Hi','Elvey','helvey1@samsung.com')
    ,(3,'765-914-7303','Waite','Markham','wmarkham2@nationalgeographic.com')
    ,(4,'810-327-8205','Lorette','Hughes','lhughes3@ft.com')
    ,(5,'598-744-1426','Rustie','Caffrey','rcaffrey4@feedburner.com')
    ,(6,'884-324-5088','Juieta','Bamber','jbamber5@phoca.cz')
    ,(7,'723-285-0144','Roddie','McVity','rmcvity6@bloglovin.com')
    ,(8,'504-286-7490','Patrice','Demangel','pdemangel7@jugem.jp')
    ,(9,'122-375-4286','Barbabas','Stratz','bstratz8@example.com')
    ,(10,'322-882-1288','Sheri','Norcop','snorcop9@flickr.com')
    ,(11,'497-609-4326','Brandie','Tatem','btatema@squidoo.com')
    ,(12,'899-522-6046','Camel','Franceschielli','cfranceschiellib@auda.org.au')
    ,(13,'129-408-6981','Berta','Taysbil','btaysbilc@wordpress.org')
    ,(14,'936-378-7972','Blaine','Seawell','bseawelld@tiny.cc')
    ,(15,'378-229-8461','Gussy','Gartell','ggartelle@uiuc.edu')
    ,(16,'729-444-5496','Austin','Baumaier','abaumaierf@php.net')
    ,(17,'169-672-3862','Alexi','Shotton','ashottong@multiply.com')
    ,(18,'125-117-9312','Cathrin','Bruneton','cbrunetonh@imdb.com')
    ,(19,'727-762-2904','Daisy','Jesper','djesperi@nymag.com')
    ,(20,'194-470-0836','Fidel','Bahl','fbahlj@g.co')
    ,(21,'442-282-2951','Gretta','Hammell','ghammellk@squidoo.com')
    ,(22,'268-259-8915','Mitchel','Quennell','mquennelll@plala.or.jp')
    ,(23,'364-899-2164','Joel','Cassin','jcassinm@woothemes.com')
    ,(24,'713-249-5136','Salvatore','Elgey','selgeyn@360.cn')
    ,(25,'655-263-6379','Manon','Dennitts','mdennittso@bluehost.com')
    ,(26,'519-357-3836','Janith','Cassells','jcassellsp@youtu.be')
    ,(27,'294-293-5305','Jarib','McCormick','jmccormickq@umn.edu')
    ,(28,'466-805-1777','Frederique','Walworth','fwalworthr@mapquest.com')
    ,(29,'847-152-1138','Vinny','Sigg','vsiggs@dmoz.org')
    ,(30,'606-538-6875','Kelsi','McConachie','kmcconachiet@digg.com')
    ,(31,'387-469-4403','Neale','Wiszniewski','nwiszniewskiu@hubpages.com')
    ,(32,'700-747-4991','Leopold','Riping','lripingv@google.it')
    ,(33,'311-671-5891','Juana','Rosina','jrosinaw@google.es')
    ,(34,'959-148-2479','Flinn','Allright','fallrightx@about.com')
    ,(35,'594-476-8097','Timothy','Belcham','tbelchamy@ycombinator.com')
    ,(36,'130-898-8374','Cindra','Balden','cbaldenz@zdnet.com')
    ,(37,'489-868-3870','Magdalena','Este','meste10@princeton.edu')
    ,(38,'482-243-5856','Nessi','Mabbutt','nmabbutt11@intel.com')
    ,(39,'767-943-0299','Vassili','Zorer','vzorer12@webeden.co.uk')
    ,(40,'534-321-0502','Garold','Hurdidge','ghurdidge13@stanford.edu')
    ,(41,'468-937-1032','Avis','Coward','acoward14@usgs.gov')
    ,(42,'295-365-8750','Andres','Carlisso','acarlisso15@yellowpages.com')
    ,(43,'229-907-9708','Quint','Ballinghall','qballinghall16@washington.edu')
    ,(44,'557-703-8247','Lorie','Kollatsch','lkollatsch17@cam.ac.uk')
    ,(45,'917-927-7134','Jacquelynn','Haberfield','jhaberfield18@unc.edu')
    ,(46,'626-874-1313','Trina','Sneezum','tsneezum19@amazon.com')
    ,(47,'857-599-0161','Cheryl','Pennings','cpennings1a@weebly.com')
    ,(48,'438-949-3751','Sterne','Drei','sdrei1b@deliciousdays.com')
    ,(49,'653-358-1983','Mylo','Braban','mbraban1c@soundcloud.com')
    ,(50,'356-368-5059','Irena','Massie','imassie1d@bigcartel.com')
    ,(51,'425-657-9560','Constantine','Ripley','cripley1e@engadget.com')
    ,(52,'953-513-7637','Karlen','Boorn','kboorn1f@networksolutions.com')
    ,(53,'254-794-9481','Joni','Molson','jmolson1g@independent.co.uk')
    ,(54,'798-570-9463','Clemence','Bonnor','cbonnor1h@washington.edu')
    ,(55,'483-837-1845','Ulick','Picton','upicton1i@histats.com')
    ,(56,'221-456-7216','Eddy','Toogood','etoogood1j@cocolog-nifty.com')
    ,(57,'513-682-9272','Boy','Lindenberg','blindenberg1k@admin.ch')
    ,(58,'274-699-7070','Millisent','Lethibridge','mlethibridge1l@dedecms.com')
    ,(59,'386-725-8429','Caresse','Tremlett','ctremlett1m@dot.gov')
    ,(60,'237-116-0572','Elayne','Kid','ekid1n@phpbb.com')
    ,(61,'930-825-1538','Des','Rivalland','drivalland1o@tinypic.com')
    ,(62,'549-431-3091','Keelby','Heinrich','kheinrich1p@sina.com.cn')
    ,(63,'683-893-0874','Ira','Abotson','iabotson1q@goo.ne.jp')
    ,(64,'806-581-7364','Christy','Darell','cdarell1r@spotify.com')
    ,(65,'511-381-7127','Drusy','Michel','dmichel1s@fema.gov')
    ,(66,'749-735-2704','Montgomery','Lilie','mlilie1t@symantec.com')
    ,(67,'224-666-3346','Kata','Ellerey','kellerey1u@mayoclinic.com')
    ,(68,'451-855-4156','Sue','Casarini','scasarini1v@google.ca')
    ,(69,'388-383-8584','Mercie','Moles','mmoles1w@buzzfeed.com')
    ,(70,'963-691-5232','Kittie','Korba','kkorba1x@usgs.gov')
    ,(71,'668-334-7253','Ramsey','Froude','rfroude1y@sciencedirect.com')
    ,(72,'291-626-5445','Nola','Dayley','ndayley1z@epa.gov')
    ,(73,'330-155-9001','Merv','Postlethwaite','mpostlethwaite20@scribd.com')
    ,(74,'194-801-8604','Ruddie','Kordas','rkordas21@discovery.com')
    ,(75,'114-885-3559','Ab','Brussell','abrussell22@edublogs.org')
    ,(76,'936-287-4248','Gavra','Bruinemann','gbruinemann23@reuters.com')
    ,(77,'470-410-6563','Perri','Stooke','pstooke24@xrea.com')
    ,(78,'252-627-8381','Padget','Leggs','pleggs25@vimeo.com')
    ,(79,'962-714-6268','Rosabella','Capon','rcapon26@cbsnews.com')
    ,(80,'232-261-2070','Ediva','Mcwhinney','emcwhinney27@cdbaby.com')
    ,(81,'185-545-3963','Jolynn','Martyns','jmartyns28@moonfruit.com')
    ,(82,'253-290-2371','Alano','Artingstall','aartingstall29@flickr.com')
    ,(83,'639-705-8880','Cam','Dunham','cdunham2a@cocolog-nifty.com')
    ,(84,'274-876-6967','Colene','Hamlet','chamlet2b@va.gov')
    ,(85,'263-771-4476','Ainslee','Creedland','acreedland2c@dedecms.com')
    ,(86,'838-339-8267','Pembroke','Kohrding','pkohrding2d@ovh.net')
    ,(87,'969-292-0804','Georgine','De Nisco','gdenisco2e@eventbrite.com')
    ,(88,'289-236-9774','Reinaldos','Kelleway','rkelleway2f@redcross.org')
    ,(89,'137-925-0842','Faina','Turfs','fturfs2g@google.co.uk')
    ,(90,'779-264-9966','Helenelizabeth','Collcutt','hcollcutt2h@usgs.gov')
    ,(91,'285-127-9182','Dix','Baudinet','dbaudinet2i@blog.com')
    ,(92,'284-868-0369','Chanda','Lewcock','clewcock2j@shareasale.com')
    ,(93,'390-121-8333','Eadie','Neligan','eneligan2k@squarespace.com')
    ,(94,'127-948-1778','Nerissa','Ayrs','nayrs2l@usatoday.com')
    ,(95,'642-359-8351','Hope','Forder','hforder2m@pen.io')
    ,(96,'838-954-6539','Correna','Loosemore','cloosemore2n@seesaa.net')
    ,(97,'573-402-0067','Trent','Barreau','tbarreau2o@fda.gov')
    ,(98,'609-630-8366','Vi','Pask','vpask2p@netlog.com')
    ,(99,'846-579-0881','Karoline','Hixley','khixley2q@over-blog.com')
    ,(100,'214-805-4859','Kamilah','Mincini','kmincini2r@ibm.com');


INSERT INTO Delivery_Person(driver_id,first_name,last_name,phone_number,email,street_address,city,state,zip,mode_transportation) VALUES
    (1,'Wilmette','Pearne','319-487-0641','wpearne0@nasa.gov','5 Hollow Ridge Circle','Waterloo','Iowa',50706,3)
    ,(2,'Chris','Prise','918-985-7561','cprise1@dyndns.org','4121 Autumn Leaf Hill','Tulsa','Oklahoma',74126,2)
    ,(3,'Patti','Badcock','720-308-6302','pbadcock2@nasa.gov','317 Westend Place','Littleton','Colorado',80161,3)
    ,(4,'Geraldine','Goulthorp','202-515-1601','ggoulthorp3@yahoo.co.jp','4 Golf Street','Washington','District of Columbia',20268,2)
    ,(5,'Janeva','Bailes','334-440-9605','jbailes4@globo.com','4409 Granby Road','Montgomery','Alabama',36104,2)
    ,(6,'Floyd','Moggan','218-535-0696','fmoggan5@biglobe.ne.jp','2 Texas Pass','Minneapolis','Minnesota',55423,1)
    ,(7,'Tessy','Copcott','916-767-2504','tcopcott6@youku.com','41 Ramsey Circle','Sacramento','California',94230,1)
    ,(8,'Holden','Brunelli','212-729-8616','hbrunelli7@google.nl','8699 Longview Point','New York City','New York',10131,1)
    ,(9,'Joya','O''Cullen','206-299-2857','jocullen8@cisco.com','9 Mariners Cove Pass','Seattle','Washington',98127,2)
    ,(10,'Willey','Hartgill','315-284-6982','whartgill9@illinois.edu','61169 Harper Parkway','Syracuse','New York',13224,2)
    ,(11,'Ragnar','Westcarr','404-757-3834','rwestcarra@blogs.com','8 Buell Parkway','Marietta','Georgia',30066,3)
    ,(12,'Greta','Cassy','918-141-0497','gcassyb@ovh.net','03 Washington Lane','Tulsa','Oklahoma',74156,1)
    ,(13,'Rock','Aldiss','404-709-8920','raldissc@tripadvisor.com','3749 Crownhardt Street','Atlanta','Georgia',30351,1)
    ,(14,'Lindi','Highnam','682-270-7696','lhighnamd@last.fm','0 Parkside Court','Fort Worth','Texas',76178,2)
    ,(15,'Brooks','Placido','804-894-3410','bplacidoe@gizmodo.com','17 Main Drive','Richmond','Virginia',23220,1)
    ,(16,'Vikki','Coen','304-223-9497','vcoenf@ed.gov','811 Lien Junction','Charleston','West Virginia',25362,1)
    ,(17,'Grace','Cooney','612-476-9246','gcooneyg@google.cn','0393 Moland Court','Saint Paul','Minnesota',55108,1)
    ,(18,'Julia','Reasce','702-328-6019','jreasceh@spiegel.de','1 Fairview Way','Las Vegas','Nevada',89115,1)
    ,(19,'Jaclin','Melesk','970-473-2911','jmeleski@simplemachines.org','8 Reindahl Plaza','Fort Collins','Colorado',80525,1)
    ,(20,'Bertine','Goundry','216-612-3452','bgoundryj@bluehost.com','28232 Calypso Terrace','Cleveland','Ohio',44105,1);


INSERT INTO Restaurant(restaurant_id,restaurant_name,phone_number,avg_delivery_time,street_address,city,state,zip) VALUES
    (1,'Photolist','727-699-6467',31,'727 Dayton Road','Saint Petersburg','FL',33737)
    ,(2,'Kwinu','415-679-8521',75,'5 Trailsway Avenue','San Francisco','CA',94169)
    ,(3,'Shufflebeat','971-900-1145',20,'2372 Spenser Place','Portland','OR',97255)
    ,(4,'Demivee','901-712-9628',63,'18619 Saint Paul Trail','Memphis','TN',38168)
    ,(5,'Vimbo','512-345-5424',59,'4 Ludington Terrace','Austin','TX',78789)
    ,(6,'Fliptune','213-736-7772',21,'868 Ohio Crossing','Los Angeles','CA',90025)
    ,(7,'Skyndu','608-414-4597',59,'220 Anniversary Park','Madison','WI',53705)
    ,(8,'Skyble','847-971-6576',75,'29 Hintze Lane','Evanston','IL',60208)
    ,(9,'Twimm','989-829-7577',71,'5482 Rigney Court','Midland','MI',48670)
    ,(10,'Pixoboo','718-245-2004',21,'37232 Spohn Pass','Bronx','NY',10469)
    ,(11,'Quimm','214-998-4503',41,'203 Manitowish Drive','Dallas','TX',75265)
    ,(12,'Gabspot','760-952-2511',37,'85 Pearson Drive','San Bernardino','CA',92415)
    ,(13,'Feedfire','718-900-5048',33,'466 Florence Alley','Brooklyn','NY',11220)
    ,(14,'Skalith','775-326-3747',72,'198 Messerschmidt Street','Reno','NV',89595)
    ,(15,'Camido','727-191-0332',34,'31919 Heffernan Drive','Saint Petersburg','FL',33705)
    ,(16,'Realmix','623-584-9485',61,'44 Hoffman Lane','Phoenix','AZ',85020)
    ,(17,'Flipopia','614-645-2360',51,'81 Welch Street','Columbus','OH',43215)
    ,(18,'Izio','361-730-1580',67,'896 Division Avenue','Corpus Christi','TX',78426)
    ,(19,'Yotz','682-865-9027',15,'596 Nova Alley','Fort Worth','TX',76115)
    ,(20,'Yakitri','202-868-6799',56,'0 Macpherson Court','Washington','DC',20397);

