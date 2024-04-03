import psycopg
from member import checkTrainerAvail
from datetime import datetime

# This file contains functions related to administrator actions including making room bookings, managing group fitness classes, equipment maintenance, and bill and payment processing

# Function to display the main menu for the admin view
def adminMenu(conn, firstName):
    while True:
        print("\nAdministrator Menu:")
        print("1. Manage room bookings") 
        print("2. Manage group fitness classes") 
        print("3. View the maintenance status of all equipment")
        print("4. Perform maintenance on a piece of equipment")
        print("5. View bill for a member")
        print("6. Generate a bill for a member")
        print("7. Process a member's bill payment")
        print("8. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            manageRoomBookings(conn)
        elif choice == "2":
            manageFitnessClasses(conn)
        elif choice == "3":
            viewEquipmentMaintenance(conn)
        elif choice == "4":
            performMaintenance(conn)
        elif choice == "5":
            viewBill(conn)
        elif choice == "6":
            generateBill(conn)
        elif choice == "7":
            processPayment(conn)
        elif choice == "8":
            print("Bye", firstName + "!")
            break
        else:
            print("Please select a valid option")

# Function to login an administrator      
def adminLogin(conn):
    with conn.cursor() as cursor:
        try:
            email = input("Administrator's email: ")
            password = input("Password: ")

            # Check for the email and password in the admin table and if it exists, log in the user
            cursor.execute("SELECT admin_id, first_name FROM administrators WHERE lower(email) = lower(%s) AND password = %s;", (email, password))
            row = cursor.fetchone()
            if row:
                print(f"Welcome {row[1]}!")
                adminMenu(conn, row[1])
            else:
                print("No administrator with that email and password")
        except psycopg.Error as e:
            print(f"Error logging in administrator: {e}")

# Function to show the menu for room booking management
def manageRoomBookings(conn):
    while True:
        print("\nRoom Booking Menu")
        print("1. Make a room booking")
        print("2. Update a room booking")
        print("3. Cancel a room booking")
        print("4. Go back")
        choice = input("Select an option: ")

        if choice == '1':
            makeRoomBooking(conn)
        elif choice == '2':
            updateRoomBooking(conn)
        elif choice == '3':
            cancelRoomBooking(conn)
        elif choice == '4':
            break
        else:
            print("Please select a valid option")

# Helper function to check room availability
def checkRoomAvailablity(cursor, roomId, date, startTime, endTime, bookingId = None):
    # Check if the there are any bookings in the time frame. if a bookId is given, exclude any booking with that id from the search (for updating room booking time)
    if bookingId:
        cursor.execute("SELECT COUNT(*) FROM room_bookings WHERE room_id = %s AND NOT (end_time <= %s OR start_time >= %s) AND date = %s AND booking_id != %s", (roomId, startTime, endTime, date, bookingId))
    else:
        cursor.execute("SELECT COUNT(*) FROM room_bookings WHERE room_id = %s AND NOT (end_time <= %s OR start_time >= %s) AND date = %s", (roomId, startTime, endTime, date))
    
    # If there is no room booking during that time, it is available
    return cursor.fetchone()[0] == 0

# Function to make a room booking
def makeRoomBooking(conn):
    with conn.cursor() as cursor:
        # Display all the rooms available to book
        cursor.execute("SELECT room_id, name, max_members FROM rooms;")
        rooms = cursor.fetchall()
        print("\nRooms available for booking:")
        for room in rooms:
            print(f"Room Id: {room[0]}, Room Name: {room[1]}, Max Capacity: {room[2]}")
        
        # Get the info for a room booking
        roomId = input("Enter the Id of the room you wish to book: ")
        try:
            dateInp = input("Enter the date for the booking (Use the form yyyy-mm-dd): ")
            date = datetime.strptime(dateInp, "%Y-%m-%d").date()
            startTimeInp = input("Enter the booking start time (Use the form hh:mm): ")
            startTime = datetime.strptime(startTimeInp, "%H:%M").time()
            endTimeInp = input("Enter the booking end time (Use the form hh:mm): ")
            endTime = datetime.strptime(endTimeInp, "%H:%M").time()
        except ValueError:
            print("Incorrect format used for date or time")
            return
        purpose = input("Enter the purpose of the booking: ")

        # Book the room if it is available
        if checkRoomAvailablity(cursor, roomId, date, startTime, endTime):
            try:
                cursor.execute("INSERT INTO room_bookings (room_id, date, start_time, end_time, purpose) VALUES (%s, %s, %s, %s, %s);", (roomId, date, startTime, endTime, purpose))
                print("Room booked")
            except psycopg.Error as e:
                print(f"Error when making room booking: {e}")
        else:
            print("The room is already booked at this time")

# Function to update the time of a room booking
def updateRoomBooking(conn):
    with conn.cursor() as cursor:
        # Get bookings for user to select which to update
        cursor.execute("SELECT booking_id, room_id, date, start_time, end_time, purpose FROM room_bookings ORDER BY date, start_time;")
        bookings = cursor.fetchall()
        
        # Print room bookings if there are room bookings
        if bookings:
            print("\nRoom Bookings:")
            for booking in bookings:
                print(f"Booking Id: {booking[0]}, Room Id: {booking[1]}, Date: {booking[2]}, Start Time: {booking[3]}, End Time: {booking[4]}, Purpose: {booking[5]}")
        else:
            print("No room bookings to update")
            return
        
        bookingId = input("Enter the Id of the booking you wish to update: ")
        
        # Check to see if that booking exists
        cursor.execute("SELECT booking_id, room_id, date, start_time, end_time, purpose FROM room_bookings WHERE booking_id = %s;", (bookingId,))
        booking = cursor.fetchone()
        if booking is None:
            print("No booking with that id exists")
            return   
        roomId = booking[1]
        
        # Prompt for updated date and time
        try:
            dateInp = input("Enter the new date for the booking (Use the form yyyy-mm-dd or hit Enter to keep the same date): ")
            if not date:
                date = booking[2]
            else:
                date = datetime.strptime(dateInp, "%Y-%m-%d").date()
            startTimeInp = input("Enter the new booking start time (Use the form hh:mm or Hit Enter to keep the same time): ")
            if not startTimeInp:
                startTime = booking[3]
            else:
                startTime = datetime.strptime(startTimeInp, "%H:%M").time()
            endTimeInp = input("Enter the new booking end time (Use the form hh:mm or Hit Enter to keep the same time): ")
            if not endTimeInp:
                endTime = booking[4]
            else:
                endTime = datetime.strptime(endTimeInp, "%H:%M").time()
        except ValueError:
            print("Incorrect format used for date or time")
            return
        
        purpose = input("Enter the new purpose of the booking (Hit Enter to keep the same purpose): ")
        if not purpose:
            purpose = booking[5]
        
        # Update the room booking if the room is available
        if checkRoomAvailablity(cursor, roomId, date, startTime, endTime, bookingId):
            try:
                cursor.execute("UPDATE room_bookings SET room_id = %s, date = %s, start_time = %s, end_time = %s, purpose = %s WHERE booking_id = %s", (roomId, date, startTime, endTime, purpose, bookingId))
                print("Room booking updated")
            except psycopg.Error as e:
                print(f"Error when updating room booking: {e}")
        else:
            print("The room is already booked at this time")

# Function to cancel a room booking    
def cancelRoomBooking(conn):
    with conn.cursor() as cursor:
        # Get all room bookings for user to select which to cancel
        cursor.execute("SELECT booking_id, room_id, date, start_time, end_time, purpose FROM room_bookings ORDER BY date, start_time;")
        bookings = cursor.fetchall()
        
        if bookings:
            print("\nRoom Bookings:")
            for booking in bookings:
                print(f"Booking Id: {booking[0]}, Room Id: {booking[1]}, Date: {booking[2]}, Start Time: {booking[3]}, End Time: {booking[4]}, Purpose: {booking[5]}")
        else:
            print("No room bookings to update")
            return
        
        bookingId = input("Enter the Id of the booking you wish to update: ")
        
        # Delete the room booking from the table
        try:
            cursor.execute("DELETE FROM room_bookings WHERE booking_id = %s;", (bookingId,))
            if cursor.rowcount:
                print("Booking cancelled")
            else:
                print("No booking was found with that Id")
        except psycopg.Error as e:
            print(f"Error when cancelling booking: {e}")

# Function to display the menu for group fitness class management
def manageFitnessClasses(conn):
     while True:
        print("\nGroup Fitness Class Menu:")
        print("1. Add a new group fitness class")
        print("2. Update an existing group fitness class")
        print("3. Cancel a group fitness class")
        print("4. Go back")
        choice = input("Choose an option: ")

        if choice == '1':
            scheduleFitnessClass(conn)
        elif choice == '2':
            rescheduleFitnessClass(conn)
        elif choice == '3':
            cancelFitnessClass(conn)
        elif choice == '4':
            break
        else:
            print("Please select a valid option")

# Function for scheduling a group fitness class       
def scheduleFitnessClass(conn):
    with conn.cursor() as cursor:
        # Get the trainers for the club and display them for the user to select which to choose for the session
        print("Trainers available to teach group fitness classes:")
        cursor.execute("SELECT trainer_id, first_name, last_name FROM trainers;")
        for trainer in cursor.fetchall():
            print(f"Trainer Id: {trainer[0]}, Name: {trainer[1]} {trainer[2]}")
        
        # Get information for the class
        title = input("Enter a title for the class: ")
        trainerId = input("Enter the Id of the trainer for the class: ")
        try:
            date = input("Enter the date for the class (Use the form yyyy-mm-dd): ")
            startTimeInp = input("Enter the class start time (Use the form hh:mm): ")
            startTime = datetime.strptime(f"{date} {startTimeInp}", "%Y-%m-%d %H:%M")
            endTimeInp = input("Enter the class end time (Use the form hh:mm): ")
            endTime = datetime.strptime(f"{date} {endTimeInp}", "%Y-%m-%d %H:%M")
            maxMembers = input("Enter maximum number of members allowed: ")
        except ValueError:
            print("Incorrect format used for date or time")
            return

        # If the trainer is available, schedule the group fitness class
        if checkTrainerAvail(cursor, trainerId, startTime, endTime):
            try:
                cursor.execute("INSERT INTO group_classes (title, trainer_id, start_time, end_time, max_members) VALUES (%s, %s, %s, %s, %s);", (title, trainerId, startTime, endTime, maxMembers))
                print("Group fitness class scheduled")
            except psycopg.Error as e:
                print(f"Error adding group fitness class: {e}")
        else:
            print("The trainer is not available at the requested time")

# Function to reschedule the time of a group fitness class        
def rescheduleFitnessClass(conn):
    with conn.cursor() as cursor:
        # Get the group fitness classes scheduled and print them for the user to select which to reschedule
        cursor.execute("SELECT c.class_id, c.title, c.start_time, c.end_time, c.max_members, t.first_name, t.last_name FROM group_classes c JOIN trainers t ON c.trainer_id = t.trainer_id ORDER BY c.start_time;")
        classes = cursor.fetchall()
        if classes:
            print("\nGroup Fitness Classes:")
            for session in classes:
                print(f"Class Id: {session[0]}, Title: {session[1]}, Trainer: {session[5]} {session[6]}, Date: {session[2].strftime('%Y-%m-%d')}, Start Time: {session[2].strftime('%H:%M')}, End: {session[3].strftime('%H:%M')}")
        else:
            print("No group fitness classes to reschedule")
            return
        
        classId = input("Enter the Id of the class you want to reschedule: ")

        # Check if the class exists
        try:
            cursor.execute("SELECT class_id, title, trainer_id, start_time, end_time, max_members FROM group_classes WHERE class_id = %s", (classId,))
            session = cursor.fetchone()
            if session is None:
                print("Class does not exist")
                return
        except psycopg.Error as e:
            print("No class with that id")
            return
            
        # Get updated date and times
        try:
            date = input("Enter the new desired date for the class (Use the form yyyy-mm-dd or Hit Enter to keep the same date): ")
            if not date:
                date = session[3].strftime('%Y-%m-%d')
            startTimeInp = input("Enter the new class start time (Use the form hh:mm or Hit Enter to keep the same time): ")
            if not startTimeInp:
                startTimeInp = session[3].strftime('%H:%M')
            endTimeInp = input("Enter the new class end time (Use the form hh:mm or Hit Enter to keep the same time): ")
            if not endTimeInp:
                endTimeInp = session[4].strftime('%H:%M')
            
            startTime = datetime.strptime(f"{date} {startTimeInp}", "%Y-%m-%d %H:%M")
            endTime = datetime.strptime(f"{date} {endTimeInp}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Incorrect format used for date or time")
            return

        # If the trainer is available, reschedule the session
        if checkTrainerAvail(cursor, session[2], startTime, endTime, classId=classId):
            try:
                cursor.execute("UPDATE group_classes SET start_time = %s, end_time = %s WHERE class_id = %s;", (startTime, endTime, classId))
                print("Rescheduled class")
            except psycopg.Error as e:
                print(f"Error when rescheduling group fitness class: {e}")
        else:
            print("The trainer is not available at the requested time")

# Function to cancel a group fitness class
def cancelFitnessClass(conn):
    with conn.cursor() as cursor:
        # Get the currently scheduled group fitness classes and display them for the user to select which to cancel
        cursor.execute("SELECT c.class_id, c.title, c.start_time, c.end_time, c.max_members, t.first_name, t.last_name FROM group_classes c JOIN trainers t ON c.trainer_id = t.trainer_id ORDER BY c.start_time;")
        classes = cursor.fetchall()
        if classes:
            print("\nGroup Fitness Classes:")
            for session in classes:
                print(f"Class Id: {session[0]}, Title: {session[1]}, Trainer: {session[5]} {session[6]}, Date: {session[2].strftime('%Y-%m-%d')}, Start Time: {session[2].strftime('%H:%M')}, End: {session[3].strftime('%H:%M')}")
        else:
            print("No group fitness classes to cancel")
            return
        
        classId = input("Enter the Id of the class you want to cancel: ")
        
        try:
            # Delete the group class which will also delete all of its registrations
            cursor.execute("DELETE FROM group_classes WHERE class_id = %s;", (classId,))
            if cursor.rowcount:
                print("Class cancelled")
            else:
                print("No class found with that Id")
        except psycopg.Error as e:
            print(f"Error cancelling class: {e}")

# Function to view the equipment maintenance status for all equipment in the gym
def viewEquipmentMaintenance(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT name, condition, last_maintenance FROM equipment;")
        equipment = cursor.fetchall()

        print("\nEquipment Maintenance Status:")
        for e in equipment:
            print(f"Equipment Name: {e[0]}, Condition: {e[1]}, Last Maintenance: {e[2]}")

# Function to perform maintenance on a piece of equipment  
def performMaintenance(conn):
    with conn.cursor() as cursor:
        # Get all equipment and print it for the user to select which to perform maintenance on
        cursor.execute("SELECT equipment_id, name, condition, last_maintenance FROM equipment;")
        equipment = cursor.fetchall()

        print("\nEquipment:")
        for e in equipment:
            print(f"Equipment Id: {e[0]}, Equipment Name: {e[1]}, Condition: {e[2]}, Last Maintenance: {e[3]}")
        
        equipmentId = input("Enter the Id of the equipment you want to perform maintenance on: ")
        
        # Check if the equipment with that id exists
        try:
            cursor.execute("SELECT equipment_id, name, condition, last_maintenance FROM equipment WHERE equipment_id = %s;", (equipmentId,))
            e = cursor.fetchone()
            if e is None:
                print("Equipment does not exist")
                return
        except psycopg.Error as e:
            print("Equipment with that id does not exist")
            return
        
        condition = input("Enter the condition of the equipment (Excellent/Good/Fair/Poor or Enter to keep the same condition): ")
        if not condition:
            condition = e[2]
        
        # Update the last maintenance date to the current date and update the status
        try:
            cursor.execute("UPDATE equipment SET condition = %s, last_maintenance = CURRENT_DATE WHERE equipment_id = %s;", (condition, equipmentId))
            print(f"Equipment maintenance performed")
        except psycopg.Error as e:
            print(f"Error performing equipment maintenance: {e}")

# Function to generate a bill for a member      
def generateBill(conn):
    with conn.cursor() as cursor:
        # Get all members and print them for the user to select which to generate a bill for
        cursor.execute("SELECT member_id, first_name, last_name FROM members;")
        members = cursor.fetchall()
        memberIds = []
        print("Members:")
        for member in members:
            memberIds.append(str(member[0]))
            print(f"Member Id: {member[0]}, Name: {member[1]} {member[2]}")

        # Get the member to generate a bill for and check if they exist
        memberId = input("Enter the Member Id to generate a bill for: ")
        if memberId not in memberIds:
            print("Member with that id does not exist")
            return
        
        # Get the month to generate a bill for
        try:
            yearMonth = input("Enter the year and month to generate the bill for (Use the form yyyy-mm): ")
            datetime.strptime(yearMonth, "%Y-%m")
        except ValueError:
            print("Incorrect format used for date")
            return
        year, month = yearMonth.split("-")
        billingMonth = yearMonth + "-01"

        # Get the number of personal sessions the member did that month
        cursor.execute("SELECT COUNT(*) FROM personal_sessions WHERE member_id = %s AND EXTRACT(MONTH FROM start_time) = %s AND EXTRACT(YEAR FROM start_time) = %s;", (memberId, month, year))
        numPersonalSessions = cursor.fetchone()[0]

        # Get the number of fitness classes the member did that month
        cursor.execute("SELECT COUNT(*) FROM class_registrations c JOIN group_classes g ON c.class_id = g.class_id WHERE c.member_id = %s AND EXTRACT(MONTH FROM g.start_time) = %s AND EXTRACT(YEAR FROM g.start_time) = %s;", (memberId, month, year))
        numGroupClasses = cursor.fetchone()[0]
        
        # Calculate the costs
        costPersonalSessions = 20 * numPersonalSessions
        costGroupClasses = 10 * numGroupClasses
        total = 30 + costPersonalSessions + costGroupClasses
        fees = f"Monthly Fee: $30, Personal Sessions: {numPersonalSessions} x $20 = ${costPersonalSessions}, Group Classes: {numGroupClasses} x $10 = ${costGroupClasses}"
        
        # Add the bill to the bills table
        try:
            cursor.execute("INSERT INTO bills (member_id, amount, billing_month, payment_due_date, status, fees) VALUES (%s, %s, %s, CURRENT_DATE + INTERVAL '1 month', 'Unpaid', %s);", (memberId, total, billingMonth, fees))
        except psycopg.Error as e:
            print(f"Error generating bill: {e}")

        print(f"Bill generated successfully for Member with Id {memberId}. Total amount due is ${total}")

# Function to view a bill      
def viewBill(conn):
    with conn.cursor() as cursor:
        # List all the bills in the bills table
        cursor.execute("SELECT b.bill_id, b.billing_month, m.first_name, m.last_name FROM bills b JOIN members m ON b.member_id = m.member_id;")
        bills = cursor.fetchall()

        # Print the bill id and the member and billing month for the admin to select which to view in full
        print("Bills:")
        for bill in bills:
            print(f"Bill Id: {bill[0]}, Member Name: {bill[2]} {bill[3]}, Billing Month: {str(bill[1])[:-3]}")

        billId = input("Enter the Bill Id you wish to view in full: ")

        # Get all the bill information
        try:
            cursor.execute("SELECT b.bill_id, m.first_name, m.last_name, b.amount, b.billing_month, b.bill_created_date, b.payment_due_date, b.status, b.fees FROM bills b JOIN members m ON b.member_id = m.member_id WHERE b.bill_id = %s;", (billId,))
            bill = cursor.fetchone()
        except psycopg.Error as e:
            print("No bill exists with that Id")
            return

        # Display the bill
        if bill:
            print("\nBill:")
            print(f"Bill Id: {bill[0]}")
            print(f"Bill Creation Date: {bill[5]}")
            print(f"Billing Month: {str(bill[4])[:-3]}")
            print(f"Member Name: {bill[1]} {bill[2]}")
            print(f"Fees: {bill[8]}")
            print(f"Amount Owing: ${bill[3]:.2f}")
            print(f"Payment Due Date: {bill[6]}")
            print(f"Payment Status: {bill[7]}")
        else:
            print("No bill found with that Id")

# Process a payment for a member 
def processPayment(conn):
    with conn.cursor() as cursor:
        # Get all the members and print them for the admin to select which to process a payment for
        cursor.execute("SELECT member_id, first_name, last_name FROM members;")
        members = cursor.fetchall()
        memberIds = []
        print("Members:")
        for member in members:
            memberIds.append(str(member[0]))
            print(f"Member Id: {member[0]}, Name: {member[1]} {member[2]}")

        # Get the member id who is making a payment
        memberId = input("Enter the member Id who is making a payment: ")
        if memberId not in memberIds:
            print("Member with that id does not exist")
            return

        # Get all unpaid bills for the member
        cursor.execute("SELECT bill_id, amount, billing_month, bill_created_date, fees FROM bills WHERE member_id = %s AND status = 'Unpaid' ORDER BY billing_month;", (memberId,))
        bills = cursor.fetchall()

        if not bills:
            print("No unpaid bills for this member")
            return

        # Show the bills that are unpaid
        print("Bills Requiring Payment:")
        for bill in bills:
            print(f"\nBill Id: {bill[0]}")
            print(f"Billing Month: {str(bill[2])[:-3]}") 
            print(f"Bill Creation Date: {bill[3]}") 
            print(f"Fees: {bill[4]}")
            print(f"Amount: ${bill[1]:.2f}") 

        billId = input("\nEnter the Bill Id to pay: ")

        # Update the status of the bill to Paid to reflect the payment
        try:
            cursor.execute("UPDATE bills SET status = 'Paid' WHERE bill_id = %s AND member_id = %s;", (billId, memberId))
            if cursor.rowcount == 0:
                print("Bill with that Id does not exist")
            else:
                print("Bill successfully paid")
        except psycopg.Error as e:
            print(f"Error processing payment: {e}")