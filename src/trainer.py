import psycopg
from datetime import datetime

# This file contains all of the functionality related to the trainer, including functions for schedule management and member profile viewing

# Displays the main trainer menu for post login
def trainerMenu(conn, trainerId, firstName):
    while True:
        print("\nTrainer Menu:")
        print("1. View schedule")
        print("2. Add or update availability")
        print("3. Remove availability")
        print("4. View a member's profile")
        print("5. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            viewSchedule(conn, trainerId)
        elif choice == "2":
            addAvailability(conn, trainerId)
        elif choice == "3":
            removeAvailability(conn, trainerId)
        elif choice == "4":
            viewMemberProfile(conn)
        elif choice == "5":
            print("Bye", firstName + "!")
            break
        else:
            print("Please select a valid option")

# Function to log in a trainer   
def trainerLogin(conn):
    with conn.cursor() as cursor:
        try:
            email = input("Trainer's email: ")
            password = input("Password: ")

            # Check to see if a trainer exists with that email and password
            cursor.execute("SELECT trainer_id, first_name FROM trainers WHERE lower(email) = lower(%s) AND password = %s;", (email, password))
            row = cursor.fetchone()
            if row:
                print(f"Welcome {row[1]}!")
                trainerMenu(conn, row[0], row[1])
            else:
                print("No trainer with that email and password")
        except psycopg.Error as e:
            print(f"Error logging in trainer: {e}")

# Function view the trainer's schedule
def viewSchedule(conn, trainerId):
    with conn.cursor() as cursor:
        # Get all availability for the trainer
        cursor.execute("SELECT day, start_time, end_time FROM trainer_availability WHERE trainer_id = %s;", (trainerId,))
        schedule = cursor.fetchall()

        # Sort the schedule to display it in order
        days = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
        schedule = sorted(schedule, key=lambda x: days[x[0]])

        # Print the trainers schedule
        print("\nYour Schedule:")
        for day in schedule:
            print(f"{day[0]}: {day[1].strftime('%H:%M')} - {day[2].strftime('%H:%M')}")

# Function to add or update availablity to the schedule
def addAvailability(conn, trainerId):
    with conn.cursor() as cursor:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        # Prompt for the day to add/update and check if it is a real day
        day = input("Enter the day you want to add/update availability for (Monday, Tuesday, etc.): ")
        day = day.capitalize()
        if day not in days:
            print("Please input a valid day of the week")
            return
        
        # Get start and end times
        try:
            startTimeInp = input("Enter your start time (Use the form hh:mm): ")
            startTime = datetime.strptime(startTimeInp, "%H:%M").time()
            endTimeInp = input("Enter your end time (Use the form hh:mm): ")
            endTime = datetime.strptime(endTimeInp, "%H:%M").time()
        except ValueError:
            print("Incorrect format used for date or time")
            return
        
        # Check if there's existing availability for the given day
        cursor.execute("SELECT COUNT(*) FROM trainer_availability WHERE trainer_id = %s AND day = %s;", (trainerId, day))
        
        # If there's existing availability, update it. Otherwise, insert new availability
        if cursor.fetchone()[0] > 0:
            try:
                cursor.execute("UPDATE trainer_availability SET start_time = %s, end_time = %s WHERE trainer_id = %s AND day = %s;", (startTime, endTime, trainerId, day))
                print("Availability updated")
            except psycopg.Error as e:
                print(f"Error updating availability: {e}")
        else:
            try:
                cursor.execute("INSERT INTO trainer_availability (trainer_id, day, start_time, end_time) VALUES (%s, %s, %s, %s);", (trainerId, day, startTime, endTime))
                print("Availability added")
            except psycopg.Error as e:
                print(f"Error when adding availability: {e}")

# Function to remove availability from the trainer's schedule
def removeAvailability(conn, trainerId):
    with conn.cursor() as cursor:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Get the day to remove availability for
        day = input("Enter the day you want to remove availability for (Monday, Tuesday, etc.): ")
        day = day.capitalize()
        if day not in days:
            print("Please input a valid day of the week")
            return
        
        # Remove the availability from the table
        try:
            cursor.execute("DELETE FROM trainer_availability WHERE trainer_id = %s AND day = %s;", (trainerId, day))
            if cursor.rowcount > 0:
                print("Availability was removed")
            else:
                print(f"You have no availability to remove for that day")
        except psycopg.Error as e:
            print(f"Error when removing availability: {e}")

# Function to search a member by name and view their profile, including email, join date, gender, and achievements    
def viewMemberProfile(conn):
    with conn.cursor() as cursor:
        # Prompt for the name to search for
        firstName = input("Enter the member's first name: ")
        lastName = input("Enter the member's last name: ")
        cursor.execute("SELECT member_id, first_name, last_name, email, join_date, gender FROM members WHERE lower(first_name) = lower(%s) AND lower(last_name) = lower(%s);", (firstName, lastName))
        members = cursor.fetchall()

        if not members:
            print("No members are registered with that name")
            return

        # Print all the members profile found with that name
        for member in members:
            print(f"\nMember Id: {member[0]}")
            print(f"Name: {member[1]} {member[2]}")
            print(f"Email: {member[3]}")
            print(f"Join Date: {member[4].strftime('%Y-%m-%d')}")
            print(f"Gender: {member[5]}")
            
            # Get the members fitness achievements to show as part of the profile
            cursor.execute("SELECT name, achieved_date FROM fitness_achievements WHERE member_id = %s ORDER BY achieved_date DESC;", (member[0],))
            achievements = cursor.fetchall()

            if achievements:
                print("Fitness Achievements:")
                for achievement in achievements:
                    print(f"- {achievement[0]} on {achievement[1].strftime('%Y-%m-%d')}")
            else:
                print("Fitness Achievements: Member has no fitness achievements")
