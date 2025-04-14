from connection import DatabaseConnection
from weed import WeedStrainCreator

def main():
    db_conn = DatabaseConnection()
    db, cursor = db_conn.get_connection()

    # weed strain creator object
    creator = WeedStrainCreator(db, cursor)

    # menu
    while True:
        print("\n--- WEED MENU ---")
        print("1. Add a new weed strain")
        print("2. View existing weed strains (COMING SOON)")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            creator.create_strain()
        elif choice == '2':
            print("view strains selection (implement later)")  
        elif choice == '3':
            print("exiting...")
            break
        else:
            print("Invalid option. Try again.")

    # Close connection before exiting
    db_conn.close()
if __name__ == "__main__":
    main()