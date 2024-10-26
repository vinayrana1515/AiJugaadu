# app.py

from flask import Flask, request, jsonify
import psycopg2
import openai
import os
from flask_cors import CORS
# from config import key
from LLM import *
import tracemalloc
tracemalloc.start()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Set up OpenAI API key
openai.api_key = os.getenv(key)  # or directly set the API key here


class Conversation:
    def __init__(self,customer_type,purchase_history,purchase_history_total,min_selling_prize,selling_price) -> None:
        # Example usage
        self.iteration = 0
        self.customer_type = customer_type
        self.purchase_history = purchase_history
        self.purchase_history_total_spend = purchase_history_total
        self.current_cart_value = 0
        self.time_spent = '25 min'
        self.previous_negotiations = []
        self.previous_counters = []
        self.min_selling_prize = min_selling_prize
        self.curr_selling_prize = selling_price
        self.actual_selling_prize = selling_price
        self.current_negotiation = ''
        self.previous_counters = []

# PostgreSQL Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'aiJugaadu')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

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

def get_user_product_info(user_id, product_id):
    try:
        
        # Check if required parameters are provided
        if user_id is None or product_id is None:
            return jsonify({"error": "User ID and Product ID are required"}), 400

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Define CTE query
        query = """
        WITH user_info AS (
            SELECT customer_type 
            FROM users 
            WHERE user_id = %s
        ),
        items_purchased AS (
            SELECT COUNT(p.purchase_id) AS items_purchased_previously
            FROM purchase p
            JOIN orders o ON p.order_id = o.order_id
            WHERE o.user_id = %s
        ),
        purchase_history AS (
            SELECT COALESCE(SUM(o.total_amount), 0) AS purchase_history
            FROM orders o
            WHERE o.user_id = %s
        ),
        product_info AS (
            SELECT price AS current_product_value, maximum_discount AS minimum_product_value
            FROM products
            WHERE _id = %s
        )
        SELECT 
            u.customer_type,
            i.items_purchased_previously,
            ph.purchase_history,
            pi.current_product_value,
            pi.minimum_product_value
        FROM user_info u, items_purchased i, purchase_history ph, product_info pi;
        """

        # Execute the query with parameters
        cursor.execute(query, (user_id, user_id, user_id, product_id))
        
        # Fetch the result
        row = cursor.fetchone()
        if row is None:
            return jsonify({"error": "No data found for the provided user or product ID"}), 404

        # Prepare the result as a dictionary
        columns = ['customer_type', 'items_purchased_previously', 'purchase_history', 'current_product_value', 'minimum_product_value']
        data = dict(zip(columns, row))

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the data as JSON
        return jsonify(data), 200

    except psycopg2.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Define a route for processing LLM requests
@app.route("/process-llm", methods=["POST"])
async def process_llm():
    data = request.json  # Get the JSON data from the request
    message = data.get("message")
    product_id = data.get("product_id")

    data_response,_ = get_user_product_info(1,product_id)
    data_response = data_response.json
    print(data_response)

    conversation = Conversation(data_response['customer_type'],data_response['purchase_history'],data_response['items_purchased_previously'],data_response['minimum_product_value'],data_response['current_product_value'])
  
    try:
        conversation.iteration+=1
        conversation.current_negotiation = message
        demanded_discount = await analyse_customer_response(conversation.actual_selling_prize,conversation.current_negotiation)
        demanded_discount = json_to_dict(demanded_discount)[0]['cost_asked']
        print(demanded_discount)
        conversation.previous_counters.append(demanded_discount)
        response = await generate_conversation(conversation.iteration,conversation.customer_type,conversation.purchase_history,conversation.purchase_history_total_spend,conversation.current_cart_value,conversation.time_spent,conversation.previous_negotiations,conversation.min_selling_prize,conversation.curr_selling_prize,conversation.actual_selling_prize,conversation.current_negotiation,demanded_discount)
        conversation.previous_negotiations.append(f"customer: {conversation.current_negotiation}\nseller: {response}")

        print(response)
        
        return jsonify({"response": json_to_dict(response)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app (only when this script is run directly)
if __name__ == "__main__":
    app.run(debug=True,port=5002)