# Health and Fitness Club Management System

This application acts as a management system for a health and fitness club. Users are able to register as a member for the club and members are able to log in and manage their profile by updating their personal and health information as well as their fitness goals. They are also able to view a dashboard with their information, schedule personal training sessions with trainers, and register for group fitness classess. Trainers of the fitness club are also able to log in and view and manage their availability as well as view profiles of members in the fitness club. Administrators are able to log in to the system and manage room bookings, view and perform maintenance on gym equipment, add new group fitness classes, generate bills for members, and process member payments.

## Video

Here is the link to the video demonstration for this application: https://youtu.be/Mc1ApSgrZSE 

## Running the Application

### Prerequisites
- Python (Can be downloaded from https://www.python.org/downloads/)
- PostgreSQL and pgAdmin (Can be installed from https://www.postgresql.org/download/)
- psycopg (Can be installed using pip install psycopg)

### Database Setup
- Launch pgAdmin 4
- Under the Object Explorer panel on the left, expand Servers
- Right click on Databases and choose Create -> Database
- In the pop-up window, enter Club as the Database name and click the Save button in the buttom right
- You should now see the Club database under Databases in the Object Explorer. Right click on the Club database and select Query Tool
- Click on the Open File icon in the toolbar and open the ddl.sql file that is under the SQL folder of this repository
- Click on the Run button to add the tables to the database
- Click on the Open File icon again and open the dml.sql file that is under the SQL folder of this repository
- Click on the Run button to insert the example records into the tables

### Connecting the Application to the Database
- The database connection occurs on line 35 of the main.py file in the src folder
- The current implementation has the fields filled out as: dbname="Club", user="postgres", password="postgres", host="localhost", port=5432
- Adjust the user, password, host, and port parameters to fit the PostgreSQL setup on your system
- If you named the database Club, there is no need to update the dbname parameter

### Running the Application
- In the command line, navigate to the src folder of this repository
- Run the command "py main.py"
- Interact with command line application using the menu options

### Testing the Application
- For testing the member functionality, it is recommended to login with the email marcus.smith@gmail.com and password Marcus123. You can also register a new member
- For testing the trainer functionality, you can login with the email jessica.norman@fitnessclub.com and password Jessica123
- For testing the administrator functionality, you can login with the email admin@fitnessclub.com and password admin