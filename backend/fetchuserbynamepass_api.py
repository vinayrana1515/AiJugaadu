from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)  # Correcting __name__ usage

# PostgreSQL Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'RetailDB')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'Helloworld@123')

# Establish database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# Define API endpoint to fetch data
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Get username and password from query parameters
        username = request.args.get('username')
        password = request.args.get('password')

        # If neither username nor password is provided, return an error message
        if not username and not password:
            return jsonify({"error": "Username and password are required as query parameters"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # If both username and password are provided, fetch the specific user
        if username and password:
            # Use a parameterized query to avoid SQL injection
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            
            # Fetch the first matching row
            row = cursor.fetchone()

            if row:
                # Convert the row to a JSON object
                data = dict(zip([column[0] for column in cursor.description], row))
                result = jsonify(data)
            else:
                result = jsonify({"message": "User not found"}), 404
        else:
            # If no username and password are provided, fetch all users
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()

            # Convert rows to JSON
            data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
            result = jsonify(data)

        # Close the connection
        cursor.close()
        conn.close()
        
        return result
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
