import json
import datetime
import http.server
import http.client
from http import HTTPStatus
import socketserver
import mysql.connector
import os
from dotenv import load_dotenv
import decimal
import bcrypt
from urllib.parse import urlparse, parse_qs


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return super().default(obj)

# Database Configuration(replace with your database settings)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'stock'
}

# Create a MySQL database connection
db_connection = mysql.connector.connect(**db_config)

# Create a cursor object to execute SQL queries
db_cursor = db_connection.cursor()

# CRUD OPERATIONS
# This class deals with CORS functionality
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == '/':
            # Serve the index.html file
            # self.path = 'index.html_url' - **The Front-End url**
            pass
        
        elif path == '/api/productManagement':
            if 'product_id' in query_params:
                # Get a specific product by ID
                product_id = query_params['product_id'][0]
                db_cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
                result = db_cursor.fetchone()

                if result:
                    product = {
                        'product_id' : result[0],
                        'product_name' : result[1],
                        'description' : result[2],
                        'category' : result[3],
                        'unit_price' : float(result[4]),
                        'quantity' : result[5],
                        'created_at' : result[6].isoformat(),
                        'updated_at' : result[7].isoformat()
                    }

                    self.send_response(200)
                    self.send_cors_headers()
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(product, cls=CustomJSONEncoder).encode())
                else:
                    self.send_response(404)
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Product not found'}).encode())
            else:
                # List all products
                db_cursor.execute("SELECT * FROM products")
                results = db_cursor.fetchall()
                
                products = [{
                    'product_id' : row[0],
                    'product_name' : row[1],
                    'description' : row[2],
                    'category' : row[3],
                    'unit_price' : float(row[4]),
                    'quantity' : row[5],
                    'created_at' : row[6].isoformat(),
                    'updated_at' : row[7].isoformat()
                } for row in results]

                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(products).encode())

        elif path == '/api/purchaseManagement':
            if 'purchase_id' in query_params:
                # Get a specific purchase by ID
                purchase_id = query_params['purchase_id'][0]
                db_cursor.execute("SELECT * FROM purchases WHERE purchase_id = %s", (purchase_id,))
                result = db_cursor.fetchone()

                if result:
                    purchase = {
                        'purchase_id' : result[0],
                        'supplier_id' : result[1],
                        'purchase_date' : result[2].isoformat()
                    }

                    self.send_response(200)
                    self.send_cors_headers()
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(purchase, cls=CustomJSONEncoder).encode())
                else:
                    self.send_response(404)
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Purchase not found'}).encode())
            else:
                # List all purchases
                db_cursor.execute("SELECT * FROM purchases")
                results = db_cursor.fetchall()
                
                purchases = [{
                        'purchase_id' : row[0],
                        'supplier_id' : row[1],
                        'purchase_date' : row[2].isoformat()
                } for row in results]

                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(purchases).encode())

        elif path == '/api/salesManagement':
            if 'sale_id' in query_params:
                # Get a specific sale by ID
                sale_id = query_params['sale_id'][0]
                db_cursor.execute("SELECT * FROM sales WHERE sale_id = %s", (sale_id,))
                result = db_cursor.fetchone()

                if result:
                    sale = {
                        'sale_id' : result[0],
                        'product_id' : result[1],
                        'customer_name' : result[2],
                        'user_id' : result[3],
                        'quantity' : result[4],
                        'sale_date' : result[5].isoformat(),
                        'unit_price' : result[6],
                        'total_price' : result[7]
                    }

                    self.send_response(200)
                    self.send_cors_headers()
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(sale, cls=CustomJSONEncoder).encode())
                else:
                    self.send_response(404)
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Sale not found'}).encode())
            else:
                # List all sales
                db_cursor.execute("SELECT * FROM sales")
                results = db_cursor.fetchall()

                sales = [{
                        'sale_id' : row[0],
                        'product_id' : row[1],
                        'customer_name' : row[2],
                        'user_id' : row[3],
                        'quantity' : row[4],
                        'sale_date' : row[5].isoformat(),
                        'unit_price' : row[6],
                        'total_price' : row[7]
                } for row in results]

                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(sales).encode())

        elif path == '/api/supplierManagement':
            if 'supplier_id' in query_params:
                # Get a specific supplier by ID
                supplier_id = query_params['supplier_id'][0]
                db_cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (supplier_id,))
                result = db_cursor.fetchone()

                if result:
                    supplier = {
                        'supplier_id' : result[0],
                        'supplier_name' : result[1],
                        'email' : result[2],
                        'phone' : result[3]
                    }

                    self.send_response(200)
                    self.send_cors_headers()
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(supplier, cls=CustomJSONEncoder).encode())
                else:
                    self.send_response(404)
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Supplier not found'}).encode())
            else:
                # List all suppliers
                db_cursor.execute("SELECT * FROM suppliers")
                results = db_cursor.fetchall()

                suppliers = [{
                    'supplier_id' : row[0],
                    'supplier_name' : row[1],
                    'email' : row[2],
                    'phone' : row[3]
                } for row in results]

                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(suppliers).encode())

        elif path == '/api/userManagement':
            if 'user_id' in query_params:
                # Get a specific user by ID
                user_id = query_params['user_id'][0]
                db_cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
                result = db_cursor.fetchone()

                if result:
                    user = {
                        'user_id' : result[0],
                        'username' : result[1]
                    }

                    self.send_response(200)
                    self.send_cors_headers()
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(user, cls=CustomJSONEncoder).encode())
                else:
                    self.send_response(404)
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'User not found'}).encode())
            else:
                # List all users
                db_cursor.execute("SELECT * FROM users")
                results = db_cursor.fetchall()

                users = [{
                        'user_id' : row[0],
                        'username' : row[1],
                } for row in results]

                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(users).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/productManagement':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode())

            print(post_data)

            # Create a product
            db_cursor.execute("INSERT INTO products(product_name, description, category, unit_price, quantity) VALUES(%s, %s, %s, %s, %s)",
                              (post_data['product_name'], post_data['description'], post_data['category'], post_data['unit_price'], post_data['quantity']))
            db_connection.commit()

            product_id = db_cursor.lastrowid
            self.send_response(201)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {"code": 201, "message": "Product created successfully", "product_id": product_id}
            self.wfile.write(json.dumps(response_data).encode())

        elif self.path == '/api/purchaseManagement':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode())

            print(post_data)
            supplier_id = post_data.get('supplier_id')
            

            # Create a purchase
            db_cursor.execute("INSERT INTO purchases(supplier_id) VALUES(%s)", (supplier_id,))
            db_connection.commit()

            purchase_id = db_cursor.lastrowid
            self.send_response(201)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {"code": 201, "message": "Purchase created successfully", "purchase_id": purchase_id}
            self.wfile.write(json.dumps(response_data).encode())

        elif self.path == '/api/salesManagement':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode())

            print(post_data)
            sale_id = post_data.get('sale_id')
            

            # Create a sale
            db_cursor.execute("INSERT INTO sales(product_id, customer_name, user_id, quantity, sale_date, unit_price, totsl_price) VALUES(%s, %s, %s, %s, %s, %s, %s)", (sale_id,))
            db_connection.commit()

            sale_id = db_cursor.lastrowid
            self.send_response(201)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {"code": 201, "message": "Sale created successfully", "sale_id": sale_id}
            self.wfile.write(json.dumps(response_data).encode())
        
        elif self.path == '/api/supplierManagement':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode())

            print(post_data)

            # Create a supplier
            db_cursor.execute("INSERT INTO suppliers(supplier_name, email, phone, product_id) VALUES(%s, %s, %s, %s)",
                              (post_data['supplier_name'], post_data['email'], post_data['phone'], post_data['product_id']))
            db_connection.commit()

            supplier_id = db_cursor.lastrowid
            self.send_response(201)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {"code": 201, "message": "Supplier created successfully", "supplier_id": supplier_id}
            self.wfile.write(json.dumps(response_data).encode())

        # Add/Register a user
        elif self.path == '/api/userManagement/register':
            # User registration
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode())
            print(post_data)

            # Hash the password before storing it in the database
            password = post_data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            db_cursor.execute("INSERT INTO users (username, password, full_name, email, role) VALUES (%s, %s, %s, %s, %s)",
                            (post_data['username'], hashed_password.decode('utf-8'), post_data['full_name'], post_data['email'], post_data['role']))
            db_connection.commit()

            user_id = db_cursor.lastrowid
            self.send_response(201)
            self.send_cors_headers()
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {'message': 'User registered successfully', 'user_id': user_id}
            self.wfile.write(json.dumps(response_data).encode())
        elif self.path == '/api/userManagement/login':
            # User login
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode())
            print(post_data)

            # Extract username and password from post_data
            username = post_data.get('username')
            password = post_data.get('password')

            if username and password:
                # Hash the password before storing it in the database
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                db_cursor.execute("SELECT user_id, username, password FROM users WHERE username = %s", (username,))
                user_data = db_cursor.fetchone()

                if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[2].encode('utf-8')):
                    self.send_response(200)
                    self.send_cors_headers()
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = {'message': 'Login successfully', 'user_id': user_data[0], 'username': user_data[1]}
                    self.wfile.write(json.dumps(response_data).encode())
                    return
            self.send_response(401)
            self.send_cors_headers()
            self.send_header('WWW-Authenticate', 'Basic realm="Inventory Management System"')
            self.end_headers()
            self.wfile.write(b'Unauthorized')
        else:
            super().do_POST()

    def do_PUT(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == '/api/productManagement' and 'product_id' in query_params:
            # Get a specific product by ID
            product_id = query_params['product_id'][0]
            db_cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            result = db_cursor.fetchone()
            if result:
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                put_data = json.loads(put_data.decode())

                # Update product information
                db_cursor.execute("UPDATE products SET product_name = %s, description = %s, category = %s, unit_price = %s, quantity = %s WHERE product_id = %s",
                                (put_data['product_name'], put_data['description'], put_data['category'], put_data['unit_price'], put_data['quantity'], product_id))
                db_connection.commit()

                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = {"code": 200, "message": "Product information updated successfully", "product_id": product_id}
                self.wfile.write(json.dumps(response_data).encode())

            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Product Not Found')

        elif path == '/api/purchaseManagement' and 'purchase_id' in query_params:
            # Get a specific purchase by ID
            purchase_id = query_params['purchase_id'][0]
            db_cursor.execute("SELECT * FROM purchases WHERE purchase_id = %s", (purchase_id,))
            result = db_cursor.fetchone()
            if result:
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                put_data = json.loads(put_data.decode())
                supplier_id = put_data.get('supplier_id')

                # Check if the new supplier_id exists
                db_cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (supplier_id,))
                supplier_exists = db_cursor.fetchone()

                if supplier_exists:
                    # Update purchase information with valid supplier_id
                    db_cursor.execute("UPDATE purchases SET supplier_id = %s WHERE purchase_id = %s", (supplier_id, purchase_id))
                    db_connection.commit()
                    self.send_response(200)
                    # ... (rest of the response logic for successful update)
                    self.send_cors_headers()
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = {"code": 200, "message": "Purchase information updated successfully", "purchase_id": purchase_id}
                    self.wfile.write(json.dumps(response_data).encode())
                else:
                    # Handle case where supplier_id doesn't exist
                    self.send_response(400)  # Bad Request
                    self.send_cors_headers()
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "Invalid supplier ID"}).encode())
            else:
                # Handle case where purchase with the ID is not found
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Purchase Not Found')

        elif path == '/api/supplierManagement' and 'supplier_id' in query_params:
            # Get a specific supplier by ID
            supplier_id = query_params['supplier_id'][0]
            db_cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (supplier_id,))
            result = db_cursor.fetchone()
            if result:
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                put_data = json.loads(put_data.decode())

                # Update supplier information
                db_cursor.execute("UPDATE suppliers SET supplier_name = %s, product_id = %s, email = %s, phone = %s WHERE supplier_id = %s",
                                (put_data['supplier_name'], put_data['product_id'], put_data['email'], put_data['phone'], supplier_id))
                db_connection.commit()

                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = {"code": 200, "message": "Supplier information updated successfully", "supplier_id": supplier_id}
                self.wfile.write(json.dumps(response_data).encode())

            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Supplier Not Found')
        
        elif path == '/api/salesManagement' and 'sale_id' in query_params:
            # Get a specific sale by ID
            sale_id = query_params['sale_id'][0]
            db_cursor.execute("SELECT * FROM sales WHERE sale_id = %s", (sale_id,))
            result = db_cursor.fetchone()
            if result:
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                put_data = json.loads(put_data.decode())

                # Update sale information
                db_cursor.execute("UPDATE sales SET product_id = %s, customer_name = %s, user_id = %s, quantity = %s, sale_date = %s, unit_price = %s, total_price = %s WHERE sale_id = %s",
                                (put_data['product_id'], put_data['customer_name'], put_data['user_id'], 
                                put_data['quantity'], put_data['sale_date'], put_data['unit_price'], put_data['total_price'],supplier_id))
                db_connection.commit()

                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = {"code": 200, "message": "Sale information updated successfully", "sale_id": sale_id}
                self.wfile.write(json.dumps(response_data).encode())

            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Sale Not Found')
        else:   
            super().do_PUT()
                
    def do_DELETE(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == '/api/productManagement' and 'product_id' in query_params:
            # Get a specific product by ID
            product_id = query_params['product_id'][0]
            db_cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            result = db_cursor.fetchone()
            if result:
                # Delete product information
                db_cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                db_connection.commit()
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Product Not Found')  

        elif path == '/api/supplierManagement' and 'supplier_id' in query_params:
            # Get a specific supplier by ID
            supplier_id = query_params['supplier_id'][0]
            db_cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (supplier_id,))
            result = db_cursor.fetchone()
            if result:
                # Delete supplier information
                db_cursor.execute("DELETE FROM suppliers WHERE supplier_id = %s", (supplier_id,))
                db_connection.commit()
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Supplier Not Found') 

        elif path == '/api/purchaseManagement' and 'purchase_id' in query_params:
            # Get a specific purchase by ID
            purchase_id = query_params['purchase_id'][0]
            db_cursor.execute("SELECT * FROM purchases WHERE purchase_id = %s", (purchase_id,))
            result = db_cursor.fetchone()
            if result:
                # Delete purchase information
                db_cursor.execute("DELETE FROM purchases WHERE purchase_id = %s", (purchase_id,))
                db_connection.commit()
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Purchase Not Found')

        elif path == '/api/salesManagement' and 'sale_id' in query_params:
            # Get a specific sale by ID
            sale_id = query_params['sale_id'][0]
            db_cursor.execute("SELECT * FROM sales WHERE sale_id = %s", (sale_id,))
            result = db_cursor.fetchone()
            if result:
                # Delete sale information
                db_cursor.execute("DELETE FROM sales WHERE sale_id = %s", (sale_id,))
                db_connection.commit()
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Sale Not Found')  

        elif path == '/api/userManagement' and 'user_id' in query_params:
            # Get a specific user by ID
            user_id = query_params['user_id'][0]
            db_cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            result = db_cursor.fetchone()
            if result:
                # Delete user information
                db_cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                db_connection.commit()
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'User Not Found')  
        else:   
            super().do_DELETE()

# Define the host and port for the server
host = 'localhost'
port = 8080

# Create and start the server
with socketserver.TCPServer((host, port), MyHandler) as server:
    print(f'Starting server on https://{host}:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server Stopped')
