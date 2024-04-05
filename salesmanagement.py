from database import Database
from productmanagement import ProductManagement
import sys

class SalesManagement:
    def menu():
        print("\nSales Management Menu")
        print("1. Buy a product")
        print("2. View sales")
        print("3. Update a specific sale")
        print("4. Delete a specific sale")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            SalesManagement.sell_a_product()
        elif choice == '2':
            SalesManagement.view_sales()
        elif choice == '3':
            SalesManagement.update_a_sale()
        elif choice == '4':
            SalesManagement.delete_a_sale()
        elif choice == '5':
            return
        else:
            print("Invalid choice. Please try again.")
            SalesManagement.menu()

    def sell_a_product():
        # call the view_products method of the productmanagement module
        print("\nThe list of products currently available is: ")
        ProductManagement.view_products()
        # enter your user_id
        user_id = input("\nEnter your user_id: ")
        sql = "SELECT user_id FROM users WHERE user_id = %s"
        value1 = user_id
        Database.db_cursor.execute(sql, (value1,))
        user = Database.db_cursor.fetchone()

        if user:
            while True:
                # enter the product_id of the product you want to buy
                entered_product_id = input("Enter the product_id of the product you want to buy: ")
                # enter the product quantity you want to buy
                entered_product_quantity = input("Enter the product_quantity: ")
                # enter the product_unit_price
                product_unit_price1 = input("Enter the product_unit_price: ")

                # ** I WAS TRYING SOME VALIDATION LOGIC HERE **
                # # retrieve the product_unit_price from the database table named products
                # sql2 = "SELECT product_unit_price FROM products WHERE product_id = %s"
                # Database.db_cursor.execute(sql2, (entered_product_id,))
                # product_unit_price2 = Database.db_cursor.fetchone()[0]
                
                product_total_price = int(product_unit_price1) * int(entered_product_quantity)
                sql3 = """INSERT INTO sales(product_id, user_id, product_quantity, 
                                product_unit_price, product_total_price) VALUES(%s, %s, %s, %s, %s)"""
                values1 = (entered_product_id, user_id, entered_product_quantity, product_unit_price1, product_total_price)
                operation = Database.db_cursor.execute(sql3, values1)
                Database.db_connection.commit()
                print(operation)

                Database.db_cursor.execute("SELECT product_quantity FROM products WHERE product_id = %s", (entered_product_id,))
                product_quantity1 = Database.db_cursor.fetchone()[0]
                new_product_quantity = product_quantity1 - int(entered_product_quantity)
                values2 = (new_product_quantity, entered_product_id)
                sql4 = "UPDATE products SET product_quantity =%s WHERE product_id = %s"
                Database.db_cursor.execute(sql4, values2)
                Database.db_connection.commit()
                print("\nProduct with product_id of " + entered_product_id + " sold successfully")

                buy_more = input("Do you want to buy more products? (yes/no): ").lower()
                if buy_more == 'yes' or buy_more == 'y':
                    SalesManagement.sell_a_product()
                else:
                    print("Exiting program...")
                    sys.exit()
        else:
            print("Enter your correct user_id")

    def view_sales():
    #    show the user what is happening in the code
       sql1 = "SELECT * FROM sales"
       Database.db_cursor.execute(sql1)
       sales = Database.db_cursor.fetchall()
       for sale in sales:
           sale = {
                "sale_id": sale[0],
                "product_id": sale[1],
                "user_id": sale[2],
                "product_quantity": sale[3],
                "product_sale_date": sale[4].strftime("%c"),
                "product_unit_price": float(sale[5]),
                "product_total_price": float(sale[6])
            }
           print(sale) 

    def update_a_sale():
    # Retrieve the details of the sale from the database
        entered_sale_id = input("\nEnter the sale_id of the sale you want to update: ")
        sql = "SELECT * FROM sales WHERE sale_id = %s"
        Database.db_cursor.execute(sql, (entered_sale_id,))
        sale = Database.db_cursor.fetchone()

        if sale:
            print("\nCurrent Sale Details:")
            print("Sale ID:", sale[0])
            print("Product ID:", sale[1])
            print("User ID:", sale[2])
            print("Product Quantity:", sale[3])
            print("Product Sale Date:", sale[4].strftime("%c"))
            print("Product Unit Price:", sale[5])
            print("Product Total Price:", sale[6])

            # Prompt the user to enter updated information
            new_product_id = input("Enter new product ID: ")
            new_user_id = input("Enter new user ID: ")
            new_product_quantity = input("Enter new product quantity: ")
            new_product_unit_price = input("Enter new product unit price: ")
            new_product_total_price = int(new_product_quantity) * int(new_product_unit_price)

            # Update the sale in the database
            sql_update = """UPDATE sales SET product_id = %s, user_id = %s, product_quantity = %s,
                            product_unit_price = %s, product_total_price = %s WHERE sale_id = %s"""
            values = (new_product_id, new_user_id, new_product_quantity,
                    new_product_unit_price, new_product_total_price, entered_sale_id)
            Database.db_cursor.execute(sql_update, values)
            Database.db_connection.commit()

            print("\nSale with sale_id of " + entered_sale_id + " updated successfully.")
        else:
            print("Sale with sale_id of " + entered_sale_id + " not found.")


    def delete_a_sale():
        SalesManagement.view_sales()
        # Retrieve the details of the sale from the database
        entered_sale_id = input("\nEnter the sale_id of the sale you want to delete: ")
        sql1 = "SELECT * FROM sales WHERE sale_id = %s"
        Database.db_cursor.execute(sql1, (entered_sale_id,))
        sale = Database.db_cursor.fetchone()

        if sale:
            sql2 = "DELETE FROM sales WHERE sale_id = %s"
            value = entered_sale_id

            Database.db_cursor.execute(sql2, (value,))
            Database.db_connection.commit()
            print("Sale with sale_id of " + entered_sale_id + " has been deleted successfully.")
        else:
           print("Sale with sale_id of " + entered_sale_id + " not found.") 
