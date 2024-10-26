from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'aiJugaadu')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

# Establish database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Database connection failed: {str(e)}")

# Helper function to check content type
def check_json_content_type():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

# Get data from a specified table
@app.route('/data/<table_name>', methods=['GET'])
def get_data(table_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        data = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        
        cursor.close()
        conn.close()
        
        return jsonify(data)
    
    except psycopg2.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Add data to a specified table
@app.route('/data/<table_name>', methods=['POST'])
def add_data(table_name):
    # Check content type before processing the request
    content_check = check_json_content_type()
    if content_check:
        return content_check

    try:
        user_data = request.get_json()
        # Extract fields dynamically based on the table structure
        columns = ', '.join(user_data.keys())
        values = ', '.join([f"'{value}'" for value in user_data.values()])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert data into the specified table
        query = f'''
            INSERT INTO {table_name} ({columns}) VALUES ({values});
        '''
        
        cursor.execute(query)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Data added successfully"}), 201
    
    except psycopg2.Error as e:
        return jsonify({"error": f"Failed to insert data: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
