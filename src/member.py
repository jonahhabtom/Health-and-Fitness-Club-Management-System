import psycopg
from datetime import datetime

# This file contains all of the functions related to member actions including user registration, profile management, dashboard display, and schedule management

# Displays the menu for a member
def memberMenu(conn, memberId, firstName):
    while True:
        print("\nMember Menu:")
        print("1. Display dashboard")
        print("2. Update personal information")
        print("3. Update health metrics")
        print("4. Manage fitness goals")
        print("5. Schedule personal training session")
        print("6. Reschedule personal training session")
        print("7. Cancel personal training session")
        print("8. Register for a group fitness class")
        print("9. Cancel a group fitness class registration")
        print("10. Add an exercise routine")
        print("11. Remove an exercise routine")
        print("12. Logout")
        choice = input("Select an option: ")

        # Call the relevant function depending on the selection
        if choice == "1":
            displayDashboard(conn, memberId)
        elif choice == "2":
            updatePersonalInfo(conn, memberId)
        elif choice == "3":
            updateHealthStats(conn, memberId)
        elif choice == "4":
            manageGoals(conn, memberId)
        elif choice == "5":
            schedulePersonalSession(conn, memberId)
        elif choice == "6":
            reschedulePersonalSession(conn, memberId)
        elif choice == "7":
            cancelPersonalSession(conn, memberId)
        elif choice == "8":
            registerGroupClass(conn, memberId)
        elif choice == "9":
            cancelGroupClass(conn, memberId)
        elif choice == "10":
            addExerciseRoutine(conn, memberId)
        elif choice == "11":
            removeExerciseRoutine(conn, memberId)
        elif choice == "12":
            print("Bye", firstName + "!")
            break
        else:
            print("Please select a valid option")

# Handles logging in a member
def memberLogin(conn):
    with conn.cursor() as cursor:
        # Prompt for email and password
        email = input("Member's email: ")
        password = input("Password: ")

        try:
            # Get a member with the email and password
            cursor.execute("SELECT member_id, first_name FROM members WHERE lower(email) = lower(%s) AND password = %s;", (email, password))
            member = cursor.fetchone()
            
            # If a member was found with that email and password, log them in
            if member:
                print(f"Welcome {member[1]}!")
                memberMenu(conn, member[0], member[1])
            else:
                print("No member with that email and password")
        except psycopg.Error as e:
            print(f"Error logging in member: {e}")

# Handles registering a member by adding them to the members table in the database    
def registerMember(conn):
    with conn.cursor() as cursor:
        firstName = input("Enter first name: ")
        lastName = input("Enter last name: ")
        email = input("Enter email: ")
        
        # Check to make sure that email does not already exist in the database
        try:
            cursor.execute("SELECT email FROM members WHERE email = %s;", (email,))
            if cursor.fetchone():
                print("Member with that email already exists")
                return
        except psycopg.Error as e:
            print(f"Error checking duplicate email during registration: {e}")
            return

        password = input("Enter password: ")
        gender = input("Gender (Male/Female/Other): ")
        
        # Get input for height, weight, body fat percentage and calculate bmi
        try:
            height = float(input("Height (cm): "))
            weight = float(input("Weight (lbs): "))
            bmi = float((weight / 2.205) / ((height / 100) ** 2))
            bodyFat = float(input("Body Fat Percentage (%): "))
        except ValueError:
            print("Please input a valid height, weight, or body fat percentage")
            return

        # Register the member by inserting them into the members table in the database
        try:
            cursor.execute("INSERT INTO members (first_name, last_name, email, password, gender, height, weight, bmi, body_fat_percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (firstName, lastName, email, password, gender, height, weight, bmi, bodyFat))
            print("Member registered")
        except psycopg.Error as e:
            print(f"Error registering member: {e}")

# Displays the dashboard to show personal info, health stats, group fitness classes, personal training sessions, fitness achievements, goals, and exercise routines
def displayDashboard(conn, memberId):
    with conn.cursor() as cursor:
        try:
            # Get the members personal info and health stats
            cursor.execute("SELECT first_name, last_name, join_date, gender, height, weight, bmi, body_fat_percentage FROM members WHERE member_id = %s;", (memberId,))
            info = cursor.fetchone()
            height, weight, bmi, bodyFat = info[4], info[5], info[6], info[7]
            
            # Print personal info
            print("\nMy Personal Dashboard")
            print(f"First Name: {info[0]}")
            print(f"Last Name: {info[1]}")
            print(f"Gender: {info[3]}")
            print(f"Club Join Date: {info[2]}")
            
            # Print health stats
            print("\nHealth Statistics:")
            print(f"Height: {height} cm")
            print(f"Weight: {weight} lbs")
            print(f"BMI: {bmi}")
            print(f"Body Fat Percentage: {str(bodyFat)}%")
            
            # Print scheduled personal training sessions
            print("\nMy Personal Training Sessions:")
            cursor.execute("SELECT p.title, p.start_time, p.end_time, t.first_name, t.last_name FROM personal_sessions p JOIN trainers t ON p.trainer_id = t.trainer_id WHERE p.member_id = %s ORDER BY p.start_time;", (memberId,))
            sessions = cursor.fetchall()
            if sessions:
                for session in sessions:
                    print(f"{session[0]} on {session[1].strftime('%Y-%m-%d')} from {session[1].strftime('%H:%M')} to {session[2].strftime('%H:%M')} with {session[3]} {session[4]}")
            else:
                print("No personal training sessions scheduled")

            # Print scheduled group fitness classes
            print("\nMy Group Fitness Classes:")
            cursor.execute("SELECT g.title, g.start_time, g.end_time, t.first_name, t.last_name FROM group_classes g JOIN trainers t ON g.trainer_id = t.trainer_id JOIN class_registrations c ON g.class_id = c.class_id WHERE c.member_id = %s ORDER BY g.start_time;", (memberId,))
            sessions = cursor.fetchall()
            if sessions:
                for session in sessions:
                    print(f"{session[0]} on {session[1].strftime('%Y-%m-%d')} from {session[1].strftime('%H:%M')} to {session[2].strftime('%H:%M')} with {session[3]} {session[4]}")
            else:
                print("No group fitness classes scheduled")
            
            # Print exercise routines
            print("\nMy Exercise Routines:")
            cursor.execute("SELECT movement, amount FROM exercise_routines WHERE member_id = %s;", (memberId,))
            routines = cursor.fetchall()
            if routines:
                for routine in routines:
                    print(f"Exercise: {routine[0]}, Repetitions/Time/Distance: {routine[1]}")
            else:
                print("No exercise routines set")
            
            # Print goals
            print("\nMy Goals:")
            cursor.execute("SELECT name, target_value, target_date FROM goals WHERE member_id = %s;", (memberId,))
            goals = cursor.fetchall()
            if goals:
                for goal in goals:
                    print(f"Goal: {goal[0]}, Target Value: {goal[1]}, Target Date: {goal[2]}")
            else:
                print("No fitness goals established")
            
            # Print fitness achievements
            print("\nMy Fitness Achievements:")
            cursor.execute("SELECT name, achieved_date FROM fitness_achievements WHERE member_id = %s ORDER BY achieved_date;", (memberId,))
            achievements = cursor.fetchall()
            if achievements:
                for achievement in achievements:
                    print(f"{achievement[0]}: Achieved on {achievement[1]}")
            else:
                print("No fitness achievements")
                    
        except psycopg.Error as e:
            print(f"Error occurred displaying dashboard: {e}")
    
# Updates personal information including name, email, password, gender      
def updatePersonalInfo(conn, memberId):
    with conn.cursor() as cursor:
        # Lists to hold parameters and their values depending on what information is being updated
        fields, values = [], []
        try:
            firstName = input("Enter new first name (Hit Enter to keep the same name): ")
            # If a first name was entered, add the field and value to the lists
            if firstName:
                fields.append("first_name = %s")
                values.append(firstName)
           
            lastName = input("Enter new last name (Hit Enter to keep the same name): ")
            # If a last name was entered, add the field and value to the lists
            if lastName:
                fields.append("last_name = %s")
                values.append(lastName)
            
            email = input("Enter new email (Hit Enter to keep the same email): ")
            # If an email was entered, add the field and value to the lists if that email does not exist already in the members table
            if email:
                cursor.execute("SELECT email FROM members WHERE email = %s;", (email,))
                if cursor.fetchone():
                    print("Member with that email already exists (Email will not be updated)")
                else:
                    fields.append("email = %s")
                    values.append(email)
            
            password = input("Enter new password (Hit Enter to keep the same password): ")
            # If a password was entered, add the field and value to the lists
            if password:
                fields.append("password = %s")
                values.append(password)
            
            gender = input("Enter new gender (Male/Female/Other or Hit Enter to keep the same gender): ")
            # If a gender was entered, add the field and value to the lists
            if gender:
                fields.append("gender = %s")
                values.append(gender)

            # If Enter was hit for every input, no updates need to be made
            if not fields:
                print("No updates made to personal information")
                return

            values.append(memberId)
            
            # Update the member record
            cursor.execute("UPDATE members SET " + ", ".join(fields) + " WHERE member_id = %s;", values)
            if cursor.rowcount > 0:
                print("Personal information updated")
            else:
                print("Personal information was not updated")
            
        except psycopg.Error as e:
            print(f"Error updating personal information: {e}")

# Function to update the member's health statistics   
def updateHealthStats(conn, memberId):
    with conn.cursor() as cursor:
        # Lists to hold parameters and their values depending on what information is being updated
        fields, values = [], []
        try:
            height = input("Enter new height in cm (Hit Enter to keep the same height): ")
            # If a height was entered, add the field and value to the lists
            if height:
                fields.append("height = %s")
                values.append(float(height))
            
            weight = input("Enter new weight in lbs (Hit Enter to keep the same weight): ")
            # If a weight was entered, add the field and value to the lists
            if weight:
                fields.append("weight = %s")
                values.append(float(weight))
            
            bodyFat = input("Enter new body fat percentage (Hit Enter to keep the same body fat percentage): ")
            # If a body fat percentage was entered, add the field and value to the lists
            if bodyFat:
                fields.append("body_fat_percentage = %s")
                values.append(float(bodyFat))

            # If the height or weight is update, recalculate the bmi
            if height or weight:
                bmi = float((float(weight) / 2.205) / ((float(height) / 100) ** 2))
                fields.append("bmi = %s")
                values.append(bmi)

            if not fields:
                print("No updates made to health statistics")
                return

            values.append(memberId)
            
            # Update the members record
            cursor.execute("UPDATE members SET " + ", ".join(fields) + " WHERE member_id = %s;", values)
            if cursor.rowcount > 0:
                print("Health statistics updated")
            else:
                print("Health statistics was not updated")
            
        except Exception as e:
            print(f"Error occured while updating health statistics: {e}")

# Displays the menu for goal management
def manageGoals(conn, memberId):
    while True:
        print("\nGoals Menu:")
        print("1. Add a new goal")
        print("2. Remove a goal")
        print("3. Go back")
        choice = input("Select an option: ")

        if choice == "1":
            addGoal(conn, memberId)
        elif choice == "2":
            removeGoal(conn, memberId)
        elif choice == "3":
            break
        else:
            print("Please select a valid option")

# Adds a goal to the goals table
def addGoal(conn, memberId):
    with conn.cursor() as cursor:
        name = input("Enter a name for the goal: ")
        target_value = input("Enter a target value for the goal: ")
        target_date = input("Enter a date by which you want to achieve the goal (Use the form yyyy-mm-dd): ")
        
        # Insert the goal into the goals table
        try:
            cursor.execute("INSERT INTO goals (member_id, name, target_value, target_date) VALUES (%s, %s, %s, %s);", (memberId, name, target_value, target_date))
            print("Goal was added")
        except psycopg.Error as e:
            print(f"Error when adding goal: {e}")

# Remove a goal from the goals table    
def removeGoal(conn, memberId):
    with conn.cursor() as cursor:
        try:
            # Get all the goals in for the member to display them for the user to choose which to remove
            cursor.execute("SELECT goal_id, name, target_value, target_date FROM goals WHERE member_id = %s;", (memberId,))
            goals = cursor.fetchall()
            
            if not goals:
                print("You do not have any goals to remove")
                return
            
            print("\nGoals:")
            for goal in goals:
                print(f"Goal Id: {goal[0]}, Goal: {goal[1]}, Target Value: {goal[2]}, Target Date: {goal[3]}")

            goalId = input("Enter the id of the goal to remove: ")
            
            # Remove the goal from the goals table
            cursor.execute("DELETE FROM goals WHERE goal_id = %s;", (goalId,))

            if cursor.rowcount > 0:
                print("Goal removed")
            else:
                print("No goal exists with that id")
                
        except psycopg.Error as e:
            print(f"Failed to remove goal: {e}")

# Helper function to check a trainer's availability        
def checkTrainerAvail(cursor, trainerId, startTime, endTime, sessionId = None, classId = None):
    # First check if trainer is available at the time
    cursor.execute("SELECT COUNT(*) FROM trainer_availability WHERE trainer_id = %s AND day = %s AND start_time <= %s AND end_time >= %s;", (trainerId, startTime.strftime("%A"), startTime.time(), endTime.time()))
    if cursor.fetchone()[0] == 0:
        return False
    
    # Check if the trainer is teaching a group fitness class. If a classId is given, do not include that class in the search (for updating class times)
    if classId:
        cursor.execute("SELECT COUNT(*) FROM group_classes WHERE trainer_id = %s AND NOT (end_time <= %s OR start_time >= %s) AND class_id != %s;", (trainerId, startTime, endTime, classId))
    else:
        cursor.execute("SELECT COUNT(*) FROM group_classes WHERE trainer_id = %s AND NOT (end_time <= %s OR start_time >= %s);", (trainerId, startTime, endTime))
    
    # If the count is more than 0, that means the trainer teaches a class during that time
    if cursor.fetchone()[0] > 0:
        return False
    
    # Check if trainer is teaching a personal training session. If a session Id is given, do not include that session in the search (for updating session times)
    if sessionId: 
        cursor.execute("SELECT COUNT(*) FROM personal_sessions WHERE trainer_id = %s AND NOT (end_time <= %s OR start_time >= %s) AND session_id != %s;", (trainerId, startTime, endTime, sessionId))
    else:
        cursor.execute("SELECT COUNT(*) FROM personal_sessions WHERE trainer_id = %s AND NOT (end_time <= %s OR start_time >= %s);", (trainerId, startTime, endTime))

    # If the count is more than 0, that means the trainer teaches a session during that time
    if cursor.fetchone()[0] > 0:
        return False
        
    return True

# Function for members to schedule a personal training session with a trainer
def schedulePersonalSession(conn, memberId):
    with conn.cursor() as cursor:
        # Provides the member a list of trainers to book with
        print("\nTrainers to schedule with:")
        cursor.execute("SELECT trainer_id, first_name, last_name FROM trainers;")
        for trainer in cursor.fetchall():
            print(f"Trainer Id: {trainer[0]}, Name: {trainer[1]} {trainer[2]}")
        
        trainerId = input("Enter the id of the trainer you want to schedule with: ")
        name = input("Enter a name for the session: ")
        date = input("Enter the date for the session (Use the form yyyy-mm-dd): ")
        startTimeInp = input("Enter the session start time (Use the form hh:mm): ")
        endTimeInp = input("Enter the session end time (Use the form hh:mm): ")
        
        # Convert date and time into datetime objects
        try:
            startTime = datetime.strptime(f"{date} {startTimeInp}", "%Y-%m-%d %H:%M")
            endTime = datetime.strptime(f"{date} {endTimeInp}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Incorrect format used for date or time")
            return

        # If the trainer is available, schedule the session
        if checkTrainerAvail(cursor, trainerId, startTime, endTime):
            try:
                cursor.execute("INSERT INTO personal_sessions (title, member_id, trainer_id, start_time, end_time) VALUES (%s, %s, %s, %s, %s);", (name, memberId, trainerId, startTime, endTime))
                print("Personal training session scheduled")
            except psycopg.Error as e:
                print(f"Error when scheduling personal training session: {e}")
        else:
            print("The trainer is not available at the requested time")

# Function for members to reschedule a personal training session
def reschedulePersonalSession(conn, memberId):
    with conn.cursor() as cursor:
        # List the currently scheduled sessions
        cursor.execute("SELECT p.session_id, p.title, p.start_time, p.end_time, t.first_name, t.last_name FROM personal_sessions p JOIN trainers t ON p.trainer_id = t.trainer_id WHERE p.member_id = %s;", (memberId,))
        sessions = cursor.fetchall()
        if sessions:
            print("\nScheduled Personal Training Sessions:")
            for session in sessions:
                print(f"Session Id: {session[0]}, Title: {session[1]}, Trainer: {session[4]} {session[5]}, Date: {session[2].strftime('%Y-%m-%d')}, Start Time: {session[2].strftime('%H:%M')}, End: {session[3].strftime('%H:%M')}")
        else:
            print("You have no sessions to reschedule")
            return
        
        # Get the id of the session to reschedule and check if it exists
        sessionId = input("Enter the id of the session you want to reschedule: ")
        cursor.execute("SELECT session_id, trainer_id, start_time, end_time FROM personal_sessions WHERE session_id = %s AND member_id = %s;", (sessionId, memberId))
        session = cursor.fetchone()
        if session is None:
            print("Session does not exist for member")
            return
        
        # Prompt for new date and time
        try:
            date = input("Enter the new desired date for the session (Use the form yyyy-mm-dd or Hit Enter to keep the same date): ")
            if not date:
                date = session[2].strftime('%Y-%m-%d')
            startTimeInp = input("Enter the new session start time (Use the form hh:mm or Hit Enter to keep the same time): ")
            if not startTimeInp:
                startTimeInp = session[2].strftime('%H:%M')
            endTimeInp = input("Enter the new session end time (Use the form hh:mm or Hit Enter to keep the same time): ")
            if not endTimeInp:
                endTimeInp = session[3].strftime('%H:%M')
            
            startTime = datetime.strptime(f"{date} {startTimeInp}", "%Y-%m-%d %H:%M")
            endTime = datetime.strptime(f"{date} {endTimeInp}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Incorrect format used for date or time")
            return
            
        # Check if trainer is available at that time and if so, update the session
        if checkTrainerAvail(cursor, session[1], startTime, endTime, session[0]):
            try:
                cursor.execute("UPDATE personal_sessions SET start_time = %s, end_time = %s WHERE session_id = %s;", (startTime, endTime, sessionId))
                print("Rescheduled session")
            except psycopg.Error as e:
                print(f"Error when rescheduling personal training session: {e}")
        else:
            print("The trainer is not available at the requested time")

# Function for cancelling a personal training session
def cancelPersonalSession(conn, memberId):
    with conn.cursor() as cursor:
        # List scheduled sessions
        cursor.execute("SELECT p.session_id, p.title, p.start_time, p.end_time, t.first_name, t.last_name FROM personal_sessions p JOIN trainers t ON p.trainer_id = t.trainer_id WHERE p.member_id = %s;", (memberId,))
        sessions = cursor.fetchall()
        if sessions:
            print("\nScheduled Personal Training Sessions:")
            for session in sessions:
                print(f"Session Id: {session[0]}, Title: {session[1]}, Trainer: {session[4]} {session[5]}, Date: {session[2].strftime('%Y-%m-%d')}, Start Time: {session[2].strftime('%H:%M')}, End: {session[3].strftime('%H:%M')}")
        else:
            print("You have no sessions to cancel")
            return
        
        sessionId = input("Enter the id of the session you want to cancel: ")
        
        # Check if session exists and if it does, cancel it
        try:
            cursor.execute("SELECT session_id FROM personal_sessions WHERE session_id = %s AND member_id = %s;", (sessionId, memberId))
            session = cursor.fetchone()
            if session is None:
                print("Session does not exist for member")
                return
            
            cursor.execute("DELETE FROM personal_sessions WHERE session_id = %s;", (sessionId,))
            print("Session cancelled")
        except psycopg.Error as e:
            print(f"Error cancelling session: {e}")

# Function for registering for a group fitness class
def registerGroupClass(conn, memberId):
    with conn.cursor() as cursor:
        # List all group fitness classes available
        cursor.execute("SELECT g.class_id, g.title, g.start_time, g.end_time, t.first_name, t.last_name FROM group_classes g JOIN trainers t ON g.trainer_id = t.trainer_id;")
        classes = cursor.fetchall()
        print("\nGroup Fitness Classes:")
        for groupClass in classes:
            print(f"Class Id: {groupClass[0]}, Title: {groupClass[1]}, Trainer: {groupClass[4]} {groupClass[5]}, Date: {groupClass[2].strftime('%Y-%m-%d')}, Start Time: {groupClass[2].strftime('%H:%M')}, End Time: {groupClass[3].strftime('%H:%M')}")

        classId = input("Enter the id of the class you want to register for: ")
        
        # Check if the member is already registered
        try:
            cursor.execute("SELECT count(*) FROM class_registrations WHERE member_id = %s AND class_id = %s;", (memberId, classId))
            if cursor.fetchone()[0] > 0:
                print("You are already registered for this class")
                return
        except psycopg.Error as e:
            print("No class with that id exists")
            return
        
        # Make sure the class has not reached its max registrations
        cursor.execute("SELECT COUNT(*) FROM class_registrations WHERE class_id = %s;", (classId,))
        numRegistrations = cursor.fetchone()[0]
        cursor.execute("SELECT max_members FROM group_classes WHERE class_id = %s;", (classId,))
        maxRegistrations = cursor.fetchone()[0]
        if numRegistrations >= maxRegistrations:
            print("This class has already reached its maximum registrations")
            return

        # Register for the class
        try:
            cursor.execute("INSERT INTO class_registrations (class_id, member_id) VALUES (%s, %s);", (classId, memberId))
            print("Registered for the group fitness class")
        except psycopg.Error as e:
            print(f"Error occured when registering for group fitness class: {e}")

# Function for cancelling a group fitness class      
def cancelGroupClass(conn, memberId):
    with conn.cursor() as cursor:
        # Get all class registrations for the member
        cursor.execute("SELECT c.registration_id, g.title, g.start_time, g.end_time FROM class_registrations c JOIN group_classes g ON c.class_id = g.class_id WHERE c.member_id = %s;", (memberId,))
        registrations = cursor.fetchall()

        if not registrations:
            print("You have no group fitness classes to cancel")
            return

        # Show the fitness class registrations for the member to select which to cancel
        print("Your group fitness class registrations:")
        for registration in registrations:
            print(f"Registration Id: {registration[0]}, Class: {registration[1]}, Date: {registration[2].strftime('%Y-%m-%d')}, Start Time: {registration[2].strftime('%H:%M')}, End Time: {registration[3].strftime('%H:%M')}")

        registrationId = input("Enter the id of the registration you wish to cancel: ")

        # Cancel the class by removing the registration
        try:
            cursor.execute("DELETE FROM class_registrations WHERE registration_id = %s AND member_id = %s;", (registrationId, memberId))
            if cursor.rowcount:
                print("Class registration cancelled")
            else:
                print("No registration exists with that id")
        except psycopg.Error as e:
            print(f"Error cancelling class registration: {e}")

# Function to add an exercise routine to the exercise_routines table        
def addExerciseRoutine(conn, memberId):
    with conn.cursor() as cursor:
        name = input("\nEnter the name of the exercise: ")
        amount = input("Enter the repetitions/time/distance: ")
        
        # Insert the routine into the table
        try:
            cursor.execute("INSERT INTO exercise_routines (member_id, movement, amount) VALUES (%s, %s, %s);", (memberId, name, amount))
            print("Exercise routine added")
        except psycopg.Error as e:
            print(f"Error adding exercise routine: {e}")

# Function to remove an exercise routine
def removeExerciseRoutine(conn, memberId):
    with conn.cursor() as cursor:
        # Get the members current exercise routines for them to select which one to remove
        cursor.execute("SELECT routine_id, movement, amount FROM exercise_routines WHERE member_id = %s;", (memberId,))
        routines = cursor.fetchall()

        if not routines:
            print("You have no exercise routines to remove")
            return

        print("\nExercise Routines:")
        for routine in routines:
            print(f"Routine Id: {routine[0]}, Exercise: {routine[1]}, Repetitions/Time/Distance: {routine[2]}")

        routineId = input("Enter the id of the routine you want to remove: ")

        # Remove the exercise routine from the table
        try:
            cursor.execute("DELETE FROM exercise_routines WHERE routine_id = %s AND member_id = %s;", (routineId, memberId))
            if cursor.rowcount:
                print("Exercise routine removed")
            else:
                print("No exercise routine exists with that id")
        except psycopg.Error as e:
            print(f"Error removing exercise routine: {e}")