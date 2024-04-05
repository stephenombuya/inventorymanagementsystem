from database import Database

class SupplierManagement:
    def menu():
        print("\nSupplier Management Menu")
        print("1. Add a supplier")
        print("2. View suppliers")
        print("3. Update a specific supplier")
        print("4. Delete a specific supplier")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            SupplierManagement.add_supplier()
        elif choice == '2':
            SupplierManagement.view_suppliers()
        elif choice == '3':
            SupplierManagement.update_a_supplier()
        elif choice == '4':
            SupplierManagement.delete_a_supplier()
        elif choice == '5':
            return
        else:
            print("Invalid choice. Please try again.")
            SupplierManagement.menu()

    def view_suppliers():
        # Retrieve and display list of suppliers from the database
        query = "SELECT * FROM suppliers"
        Database.db_cursor.execute(query)
        suppliers = Database.db_cursor.fetchall()
        for supplier in suppliers:
            supplier = {
                "supplier_id": supplier[0],
                "product_id": supplier[1],
                "supplier_business_name": supplier[2],
                "supplier_email": supplier[3],
                "supplier_phone_number": supplier[4]
            }
            print(supplier)

    def add_supplier():
            # Prompt user for supplier details
            product_id = input("Enter the product_id of the product supplied: ")
            supplier_business_name = input("Enter the name of the supplier of the product supplied: ")
            supplier_email = input("Enter the email of the supplier of the product supplied: ")
            supplier_phone_number = input("Enter the phone_number of the supplier of the product supplied: ")

            # VALIDATION WILL BE DONE LATER, for now let us
            # check if the supplier_id entered by the user exists,
            # if not then add the supplier
            query1 = "SELECT * FROM suppliers WHERE supplier_business_name = %s"
            value = supplier_business_name
            Database.db_cursor.execute(query1, (value,))
            supplier_exists = Database.db_cursor.fetchone()

            if supplier_exists:
                print("\nSupplier with supplier_business_name, " + supplier_business_name + "," + " exists. Try again!\n")
                SupplierManagement.add_supplier()
            else:
                # Insert new supplier into the database
                query2 = """INSERT INTO suppliers(product_id, supplier_business_name, 
                                        supplier_email, supplier_phone_number) VALUES(%s, %s, %s, %s)"""
                
                values = (product_id,supplier_business_name, supplier_email,supplier_phone_number)
                Database.db_cursor.execute(query2, values)
                Database.db_connection.commit()
                print("\nSupplier added succesfully!")

                add_another_supplier = input("\nDo you want to add another supplier today? (yes/no): ").lower()
                if add_another_supplier == 'yes' or add_another_supplier == 'y':
                    SupplierManagement.add_supplier()
                else:
                    SupplierManagement.menu()

    def update_a_supplier():
        # Prompt user to select or enter supplier ID
        entered_supplier_id = input("Enter the supplier_id of the supplier to be updated: ")

        # Retrieve supplier details from the database based on the supplier_id entered by the user
        Database.db_cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (entered_supplier_id,))
        supplier = Database.db_cursor.fetchone()
        # Display current supplier information
        print(supplier)

        # if supplier is available then 
        if supplier:
             # prompt user for updated information,
            new_product_id = input("Enter the product_id of the product supplied: ")
            new_supplier_business_name = input("Enter the name of the supplier of the product supplied: ")
            new_supplier_email = input("Enter the email of the supplier of the product supplied: ")
            new_supplier_phone_number = input("Enter the phone_number of the supplier of the product supplied: ")

            # Update supplier information in the database
            sql = """UPDATE suppliers SET product_id =%s, supplier_business_name = %s, supplier_email = %s,
                        supplier_phone_number= %s WHERE supplier_id = %s"""
            values = (new_product_id, new_supplier_business_name, new_supplier_email, new_supplier_phone_number, entered_supplier_id)
            Database.db_cursor.execute(sql, values)
            Database.db_connection.commit()
            # and display success!
            print("\nSupplier with supplier_id " + entered_supplier_id + " has been updated successfully!")
        else:
        # else, tell the user that the supplier_id they entered was wrong and they need to try again,
            print("\nSupplier with supplier_id of " + entered_supplier_id + "," + " does not exist. Try again!\n")
        # call back the update_a_supplier method for the user to enter correct details.
            SupplierManagement.update_a_supplier()
    
    def delete_a_supplier():
        # display available suppliers
        Database.db_cursor.execute("SELECT * FROM suppliers")
        results = Database.db_cursor.fetchall()
        for x in results:
            print(x)
        # Prompt user to select or enter supplier ID
        entered_supplier_id = input("\nEnter the supplier_id of the supplier to be deleted: ")
        # check if the supplier exists then delete the supplier
        Database.db_cursor.execute("SELECT * FROM suppliers WHERE supplier_id =%s", (entered_supplier_id,))
        supplier_exists = Database.db_cursor.fetchone()

        if supplier_exists:
            # Delete supplier from the database
            Database.db_cursor.execute("DELETE FROM suppliers WHERE supplier_id = %s", (entered_supplier_id,))
            Database.db_connection.commit()
            # Confirm deletion with user
            print("\nSupplier with supplier_id " + entered_supplier_id + " has been deleted successfully!")
        else:
            # else, tell the user that the supplier_id they entered was wrong and they need to try again,
            print("\nSupplier with supplier_id of " + entered_supplier_id + "," + " does not exist. Try again!\n")
            # call back the delete_a_supplier method for the user to enter correct details.
            SupplierManagement.delete_a_supplier()
