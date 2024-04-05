from database import Database



class PurchasesManagement:
    def menu():
        print("\nPurchases Management Menu")
        print("1. Make a purchase")
        print("2. View purchases")
        print("3. Update a specific purchase")
        print("4. Delete a specific purchase")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: \n")

        if choice == '1':
            PurchasesManagement.make_a_purchase()
        elif choice == '2':
            PurchasesManagement.view_purchases()
        elif choice == '3':
            PurchasesManagement.update_a_purchase()
        elif choice == '4':
            PurchasesManagement.delete_a_purchase()
        elif choice == '5':
            return
        else:
            print("Invalid choice. Please try again.")
            PurchasesManagement.menu()

    def view_purchases():
        # Retrieve and display list of previous purchases from the database
        Database.db_cursor.execute("SELECT * FROM purchases")
        results = Database.db_cursor.fetchall()
        for x in results:
            my_list = list(x)
            my_list[5] = my_list[5].strftime("%c")
            my_list[6] = float(my_list[6])
            my_list[7] = float(my_list[7])
            print(my_list)

    def make_a_purchase():
        # purchases can be divided into two: 
        # type1)Purchase to add a product from a supplier
        type1 = "Purchase to add a product from a supplier"
        # type2)Purchase from a supplier to be update the existing product_quantity of the specified product
        #     i.e., adding more stock of a specified product.
        type2 = "Purchase from a supplier to update the existing product_quantity of the specified product"
        # prompt the user to enter their user_id
        entered_user_id = input("\nEnter your user_id: ")
        # use the user_id to check if the user exists
        Database.db_cursor.execute("SELECT * FROM users WHERE user_id = %s", (entered_user_id,))
        user_exists = Database.db_cursor.fetchone()
        # if the user with the specified user_id exists
        if user_exists:
            # display the type of purchases
            print("\n   Type1 Purchase: " + type1)
            print("\n   Type2 Purchase: " + type2)
            # Ask the user the type of purchase they want to make
            type_of_purchase = input("\nWhat type of purchase would you want to make? (type1/type2): ").lower()
            # if the type of purchase equals type1:
            if type1:
                # ask the user to enter the purchase details
                entered_supplier_id = input("\nEnter the supplier_id of the supplier who supplied the product: ")
                entered_product_id = input("Enter the product_id of the product that is to be supplied: ")
                user_id = entered_user_id
                entered_product_quantity = input("Enter the product_quantity of the product that is to be supplied: ")
                entered_product_unit_price = input("Enter the product_unit_price of the product that is to be supplied: ")
                product_total_price = int(entered_product_unit_price) * int(entered_product_quantity)
                # insert the puchase details into the purchases table
                sql1 = """INSERT INTO purchases(supplier_id, product_id, user_id, product_quantity, 
                            product_unit_price, product_total_price)VALUES(%s, %s, %s, %s, %s, %s)"""
                values1 = (entered_supplier_id, entered_product_id, user_id, entered_product_quantity, entered_product_unit_price, product_total_price)
                Database.db_cursor.execute(sql1, values1)
                Database.db_connection.commit()
                
                # also, insert into products table the product purchased to be able to reflect automatically
                # ask the user to enter the product details of the product that was purchased from the supplier
                entered_product_name = input("\nEnter the name of the product that is to be purchased: ")
                entered_description = input("Enter the description of the product that is to be purchased: ")
                entered_product_category = input("Enter the category of the product that is to be purchased: ")
                sql2 = """INSERT INTO products(product_name, description, product_category, product_unit_price,
                                product_quantity)VALUES(%s, %s, %s, %s, %s)"""
                values2 = (entered_product_name, entered_description, entered_product_category, entered_product_unit_price, entered_product_quantity)
                Database.db_cursor.execute(sql2, values2)
                Database.db_connection.commit()
                # Tell the user that the purchase was made successfully!
                print("\nPurchase made successfully")

            # elif type of purchase equals type 2:
            elif type2:
                # ask the user to enter the product_id of the product whose 
                # product_quantity is to be updated by the purchase to be made
                # use the product_id entered to check if the product exists
                Database.db_cursor.execute("SELECT * FROM products WHERE product_id = %s", (entered_product_id,))
                product_exists = Database.db_cursor.fetchone()
                # if the product exists
                if product_exists:
                    # ask the user to enter the purchase details
                    # use the purchase details entered earlier
                    # insert the puchase details into the purchase table
                    sql3 = """INSERT INTO purchases(supplier_id, product_id, user_id, product_quantity, 
                            product_unit_price, product_total_price)VALUES(%s, %s, %s, %s, %s, %s)"""
                    values3 = (entered_supplier_id, entered_product_id, entered_user_id,entered_product_quantity, entered_product_unit_price, product_total_price)
                    Database.db_cursor.execute(sql3, values3)
                    Database.db_connection.commit()

                    # also, update products table set the product_quantity equal to
                    # the product_quantity entered among the purchase details
                    # to be able to reflect automatically
                    Database.db_cursor.execute("SELECT product_quantity FROM products WHERE product_id= %s", (entered_product_id,))
                    original_product_quantity  = Database.db_cursor.fetchone[5]

                    new_product_quantity = int(original_product_quantity) + int(entered_product_quantity)

                    sql4 = "UPDATE products SET product_quantity = %s WHERE product_id = %s"
                    values4 = (new_product_quantity, entered_product_id)
                    Database.db_cursor.execute(sql4, values4)
                    Database.db_connection.commit()
                    # Tell the user that the purchase was made successfully!
                    print("\nPurchase made successfully")
                # else
                    # Tell the user that the product with the specified product_id does not exist
                else:
                    print("Product with the specified product_id of " + entered_product_id + " does not exist")
            # else
                # display the type1 purchase and type2 purchase for the user
            else:
                print("\n   Type1 Purchase: " + type1)
                print("   Type2 Purchase: " + type2)
                # Tell the user that there is no other type of purchase apart from the ones above
                print("\nThere is no other type of purchase apart from the ones above.\n")
        # else
            # Tell the user that the user with the user_id they entered does not exist
        else:
            print("\nThe user with the user_id of " + entered_user_id + " does not exist.\n")
   


    def update_a_purchase():
        # ask the user to enter their user_id
        entered_user_id = input("Enter your user_id: ")

        # use the user_id to retrieve the user from the database
        Database.db_cursor.execute("SELECT * FROM users WHERE user_id = %s", (entered_user_id,))
        user_exists = Database.db_cursor.fetchone()

        # if the user exists
        if user_exists:
            # Prompt user to select or enter purchase ID
            print("\nThe purchases available are: ")
            PurchasesManagement.view_purchases()

            entered_purchase_id = input("\nEnter the purchase_id of the purchase you want to update: ")

            # retrieve the purchase with the given purchase_id
            Database.db_cursor.execute("SELECT * FROM purchases WHERE purchase_id = %s", (entered_purchase_id,))
            purchase_exists = Database.db_cursor.fetchone()

            # if the purchase exists
            if purchase_exists:
                # Retrieve purchase details from the database
                # Display current purchase information
                for x in purchase_exists:
                    my_list = list(purchase_exists)
                    my_list[5] = my_list[5].strftime("%c")
                    my_list[6] = float(my_list[6])
                    my_list[7] = float(my_list[7])
                print(my_list)

                # Prompt user for updated purchase information
                new_entered_supplier_id = input("\nEnter the supplier_id of the supplier who supplied the product: ")
                new_entered_product_id = input("Enter the product_id of the product that is to be supplied: ")
                user_id = entered_user_id
                new_entered_product_quantity = input("Enter the product_quantity of the product that is to be supplied: ")
                new_entered_product_unit_price = input("Enter the product_unit_price of the product that is to be supplied: ")
                new_product_total_price = int(new_entered_product_unit_price) * int(new_entered_product_quantity)

                # use the updated purchase information from the user to
                # Update purchase information in the database
                sql1 ="""UPDATE purchases SET supplier_id = %s, product_id = %s, user_id = %s, product_quantity = %s,
                        product_unit_price = %s, product_total_price = %s"""
                values1 = (new_entered_supplier_id, new_entered_product_id, user_id, new_entered_product_quantity, new_entered_product_unit_price, new_product_total_price)

                Database.db_cursor.execute(sql1, values1)
                Database.db_connection.commit()

                # fetch the original product_quantity of the given product_id
                Database.db_cursor.execute("SELECT * FROM products WHERE product_id= %s", (new_entered_product_id,))
                original_product_quantity  = Database.db_cursor.fetchone()[5]

                # logic to compute new product quantity
                new_product_quantity = original_product_quantity + int(new_entered_product_quantity)

                # Update the products table to reflect the updated purchase
                sql2 = "UPDATE products SET product_quantity = %s WHERE product_id = %s"
                values2 = (new_product_quantity, new_entered_product_id)

                Database.db_cursor.execute(sql2, values2)
                Database.db_connection.commit()

                # Tell the user that the purchase with the specified purchase_id has been updated successfully
                print("\nPurchase with purchase_id of " + entered_purchase_id + " has been updated successfully!\n")
            # else
            else:
                # Tell the user that the purchase information does not exist.
                print("\nPurchase with purchase_id of " + entered_purchase_id + " does not exist.\n")

                # Let them try again by calling the update_a_purchase() method
                PurchasesManagement.update_a_purchase()
        # else
        else:
            # Tell the user that the user with the user_id entered does not exist.
            print("\nThe user with user_id of " + entered_user_id + " does not exist.\n")

            # Let them try again by calling the update_a_purchase() method
            PurchasesManagement.update_a_purchase()

    def delete_a_purchase():
        # Prompt user to select or enter purchase ID
        entered_purchase_id = input("Enter the purchase_id of the purchase you want to delete: ")

        # Confirm deletion with user
        Database.db_cursor.execute("SELECT * FROM purchases WHERE purchase_id = %s", (entered_purchase_id,))
        purchase_exists = Database.db_cursor.fetchone()

        if purchase_exists:
            # Delete purchase from the database
            Database.db_cursor.execute("DELETE FROM purchases WHERE purchase_id = %s", (entered_purchase_id,))
            Database.db_connection.commit()

            print("\nPurchase with purchase_id of " + entered_purchase_id + " has been deleted successfully.\n")
        else:
            print("Purchase with purchase_id of " + entered_purchase_id + " does not exist.")