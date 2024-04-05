from database import Database


class ProductManagement:
    def menu():
        print("\nProduct Management Menu")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update a Product")
        print("4. Delete a Product")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            ProductManagement.add_product()
        elif choice == '2':
            ProductManagement.view_products()
        elif choice == '3':
            ProductManagement.update_product()
        elif choice == '4':
            ProductManagement.delete_product()
        elif choice == '5':
            return
        else:
            print("Invalid choice. Please try again.")
            ProductManagement.menu()

    def add_product():
        product_name = input("Enter the product name: ")
        description = input("Enter the product's description: ")
        product_category = input("Enter the product_category: ")
        product_unit_price = input("Enter the product_unit_price: ")
        product_quantity = input("Enter the product_quantity: ")
        
        try:
            Database.db_cursor.execute("""INSERT INTO products(product_name, description, product_category, 
                           product_unit_price, product_quantity) VALUES(%s, %s, %s, %s, %s)""",
                           (product_name, description, product_category, product_unit_price, product_quantity))
            Database.db_connection.commit()
            print("\nProduct added successfully.")

        except Database.mysql.connector.Error as e:
            print("Error:", e)
            Database.db_connection.rollback()

    def view_products():
        Database.db_cursor.execute("SELECT product_id, product_name, description, product_category, product_unit_price, product_quantity FROM products")
        products = Database.db_cursor.fetchall()
        for product in products:
            my_list = list(product)
            my_list[4] = float(my_list[4])
            product = tuple(my_list)
            print(product)

    def update_product():
        # enter product id
        # retrieve the product using the entered id
        # if the product exists then update it otherwise 
        # return product with given id not found
        product_id = input("Enter the product id: ")
        sql = "SELECT * FROM products WHERE product_id = %s"
        value = (product_id)
        Database.db_cursor.execute(sql, (value,))
        product = Database.db_cursor.fetchone()

        if product:

            new_product_quantity = input("Enter the new product_quantity: ")
            
            try:
                sql = "UPDATE products SET product_quantity = %s WHERE product_id = %s"
                values = (new_product_quantity, product[0])
                Database.db_cursor.execute(sql, values)
                Database.db_connection.commit()
                print("\nProduct updated successfully.")

            except Database.mysql.connector.Error as e:
                print("Error:", e)
                Database.db_connection.rollback()

        else:
            print("Product with given id not found")



    def delete_product():
        # enter product id
        # retrieve the product using the entered id
        # if the product exists then delete it otherwise 
        # return product with given id not found
        product_id = input("Enter the product id: ")
        sql = "SELECT * FROM products WHERE product_id = %s"
        value = (product_id)
        Database.db_cursor.execute(sql, (value,))
        product = Database.db_cursor.fetchone()

        if product:
            try:
                sql = "DELETE FROM products WHERE product_id = %s"
                value = (product_id)
                Database.db_cursor.execute(sql, (value,))
                Database.db_connection.commit()
                print("\nProduct deleted successfully.")

            except Database.mysql.connector.Error as e:
                print("Error:", e)
                Database.db_connection.rollback()

        else:
            print("Product with given id not found")
            
