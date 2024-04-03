import psycopg
from member import memberLogin, registerMember
from trainer import trainerLogin
from admin import adminLogin

# This file contains the code for starting the system, connecting to the database, and providing the main menu

# Displays the main menu and redirects user to other menus
def mainMenu(conn):
    while True:
        print("\nMain Menu:")
        print("1. Log in as member")
        print("2. Log in as trainer")
        print("3. Log in as administrator")
        print("4. Register as a member")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            memberLogin(conn)
        elif choice == "2":
            trainerLogin(conn)
        elif choice == "3":
            adminLogin(conn)
        elif choice == "4":
            registerMember(conn)
        elif choice == "5":
            break
        else:
            print("Please select a valid option")

def main():
    # Connect to the database (Change the code here if necessary to adhere to your setup)
    try:
        conn = psycopg.connect(dbname="Club", user="postgres", password="postgres", host="localhost", port=5432)
        conn.autocommit = True
    except psycopg.OperationalError as e:
        print(f"Error: {e}")
        exit(1)
    
    print("Welcome to the Health and Fitness Club Management System!")
    mainMenu(conn)
    
    #Close the connection when the user exits the main menu
    conn.close()

if __name__ == "__main__":
    main()