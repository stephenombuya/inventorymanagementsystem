import sys
from usermanagement import UserManagement
from productmanagement import ProductManagement
from database import Database
from salesmanagement import SalesManagement
from suppliermanagement import SupplierManagement
from purchasesmanagement import PurchasesManagement


def main_menu():
    print("============================================================================================")
    print("Welcome to our Inventory Management System, select the operation you want to perform: ")
    print("\n============================================================================================")
    
    while True:
        print("\n1. User Management")
        print("2. Product Management")
        print("3. Supplier Management")
        print("4. Sales Management")
        print("5. Purchases Management")
        print("6. Exit")

        choice = input("\nEnter your choice: \n")

        if choice == '1':
            UserManagement.menu()
        elif choice == '2':
            ProductManagement.menu()
        elif choice == '3':
            SupplierManagement.menu()
        elif choice == '4':
            SalesManagement.menu()
        elif choice == '5':
            PurchasesManagement.menu()
        elif choice == '6':
            print("Exiting program...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

        any_other_business = input("\nDo you have any other business today? (yes/no): ").lower()
        if any_other_business == 'yes' or any_other_business == 'y':
            continue
        else:
            print("Exiting program...")
            sys.exit()

if __name__ == "__main__":
    main_menu()

