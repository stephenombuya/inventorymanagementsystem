from database import Database
import bcrypt


class UserManagement:
    def menu():
        print("\nUser Management Menu")
        print("1. Add User")
        print("2. View Users")
        print("3. Update a User")
        print("4. Delete User")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            UserManagement.add_user()
        elif choice == '2':
            UserManagement.view_users()
        elif choice == '3':
            UserManagement.update_user()
        elif choice == '4':
            UserManagement.delete_user()
        elif choice == '5':
            return
        else:
            print("Invalid choice. Please try again.")
            UserManagement.menu()

    def add_user():
        username = input("\nEnter username: ")
        password = input("Enter password: ")
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        role = input("Enter role: ")

        try:
            Database.db_cursor.execute("INSERT INTO users(username, hashed_password, first_name, last_name, email, role) VALUES (%s, %s, %s, %s, %s, %s)",
                            (username, hashed_password, first_name, last_name, email, role))
            Database.db_connection.commit()
            print("\nUser added successfully.")

        except Database.mysql.connector.Error as e:
            print("Error:", e)
            Database.db_connection.rollback()

    def view_users():
        sql = "SELECT user_id, username, first_name, last_name, email, role FROM users"
        Database.db_cursor.execute(sql)
        all_users = Database.db_cursor.fetchall()
        for user in all_users:
            print(user)


    def update_user():
        # select from the database username and password from users
        sql = 'SELECT username, hashed_password FROM users WHERE username = %s'
        value = input("Enter your username: ")
        Database.db_cursor.execute(sql, (value,))
        result = Database.db_cursor.fetchone()  # Fetch a single row

        if result:
            username, password1 = result  # Unpack the tuple
            password2 = input("\nEnter your password: ")
            if bcrypt.checkpw(password2.encode('utf-8'), password1):
                print("Success")
                new_username = input("Enter new username: ")
                new_password = input("Enter new password: ")
                hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                new_email = input("Enter new email: ")
                new_role = input("Enter new role: ")

                sql = "UPDATE users SET username = %s, hashed_password = %s, email = %s, role = %s WHERE username = %s"
                values = (new_username, hashed_new_password, new_email, new_role, username)  # Corrected order
                Database.db_cursor.execute(sql, values)
                Database.db_connection.commit()
                print("\nUser updated successfully.")
            else:
                print("Failure")
        else:
            print("User not found.")



    def delete_user():
        # select from the database username and password from users
        sql = 'SELECT username, hashed_password FROM users WHERE username = %s'
        value = input("Enter your username: ")
        Database.db_cursor.execute(sql, (value,))
        result = Database.db_cursor.fetchone()  # Fetch a single row

        if result:
            username, password1 = result  # Unpack the tuple
            password2 = input("\nEnter your password: ")
            if bcrypt.checkpw(password2.encode('utf-8'), password1):
                print("Success")

                sql = "DELETE FROM users WHERE username = %s"
                value = (username)
                Database.db_cursor.execute(sql, (value,))
                Database.db_connection.commit()
                print("\nUser deleted successfully.")
            else:
                print("Failure")
        else:
            print("User not found.")
