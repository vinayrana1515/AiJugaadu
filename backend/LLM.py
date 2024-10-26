import openai
from openai import OpenAI
import json 
import asyncio

key = "OPENAI_KEY"

async def call_llm(api_key,model_name="gpt-4o-mini",system_prompt ="",user_prompt = "Write a haiku about recursion in programming.",temperature=0):

    client = OpenAI(api_key=api_key)

    completion = None

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_prompt
            }
        ],
            temperature=temperature
    )


    if completion == None:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=temperature
        )
    else:

        while completion.choices[0].message.content  is None:

            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=temperature
            )


    return completion.choices[0].message.content

def json_to_dict(json_string):
    # Remove the markdown code block delimiters
    if json_string.startswith('```json\n') and json_string.endswith('\n```'):
        json_string = json_string[8:-4]

    # Strip any leading or trailing whitespace
    json_string = json_string.strip()

    try:
        # Convert JSON string to dictionary
        #import pdb
        #pdb.set_trace()
        dictionary = json.loads(json_string)

        return dictionary
    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)
        return None

async def analyse_customer_response(actual_selling_prize,conversation,model="gpt-4o-mini", temperature=0.7)->str:
    # Construct the prompt to provide context for the conversation
    system_prompt = '''Analyse the given conversation related to a negotiation of a product done by a customer to a seller, and return give the following data points:
        Data Points -
          1. cost_asked: The cost of product asked by customer in the given conversation....
          2. realism: Tell whether the demands made by customer is realistic or not

        -Return the output strictly in the defined format only:

        ```json
            [
              {{
                  "cost_asked":<int>,
                  "realistic":<boolean>
              }}
            ]
        ```

    '''

    prompt = f'''Analyse the given conversation respectively :-
      conversation: {conversation}
      actual_Selling_price: {actual_selling_prize}

      - Return the output strictly in the defined format only:

        ```json
            [
              {{
                  "cost_asked":<int>,
                  "realistic":<boolean>
              }}
            ]
        ```
    '''
    print(prompt)
    # Call the OpenAI API to generate a conversation response
    response = ''
    try:
        response = await call_llm(api_key=key,model_name=model,system_prompt=system_prompt,user_prompt=prompt,temperature=temperature)
        response = response.choices[0].message['content'].strip()
        return response

    except Exception as e:
        # print(f"Error generating conversation: {e}")

        return response
    
def get_user_prompt(iteration,customer_type,purchase_history,purchase_history_total_spend,current_cart_value,time_spent,previous_negotiations,min_selling_prize,curr_selling_prize,actual_selling_prize,current_negotiation,demanded_discount):
  #  {min_steps} steps (atleast) to {max_steps} steps (atmax)
    prompt=f'''
          You are a shopkeeper, who is trying to maximize the sales , keeping in mind to have maximum profit, negotiate with user as customer and attain profit as per the rules defined:

          Data Points -
          0. iteration: {iteration}
          1. Customer Type (New/Returning): {customer_type}
          2. Purchase History: {purchase_history}, {purchase_history_total_spend}
          3. Cart Value: {current_cart_value}
          4. Time on Site: {time_spent}
          5. previous_negotiations: {previous_negotiations}
          6. minimum_selling_prize: {min_selling_prize}
          7. current_selling_prize: {curr_selling_prize}
          8. actual_selling_prize: {actual_selling_prize}
          9. current_statement: {current_negotiation}
          10.Demanded_discount: {demanded_discount}

          from the above given current_statement and previous_negotiation derive the user sentiments and use it as the data point for furthur generation.

          Generate a single statement having variables ie statement, discount, overall_chat_sentiment (python compatible) to be used in form on json string in the given format

          ** Thing to consider**
          Do not exceed iteration count of the strategy being followed
          Do not provide more discount than the demanded discount
          Do not go beyond the suggest minimum_selling_prize
          Do not make any assumptions.
          Don't repeat yourself
          Discount provided should in percentage format
          Do not mention customer type in response.
          If user tends to stick to a certain price give some details about the product in order to justify the product's value.

          - Mention the status of negotiation under deal_status as closed once the deal is finalised on both ends, else set it as ongoing
          - Once the deal is closed, save price in closed_price variable, else set it as 0.
          - The cost should not be less than {min_selling_prize}
          - The cost should not be more than {actual_selling_prize}
          - The cost should not be more than {demanded_discount}

          **Format for Output to be followed strictly**:
          After generating the conversation, structure it like this:

          ```json
          [
              {{
                  "statement": "<string>",
                  "discount": <int>,
                  "overall_chat_sentiment": "<string>",
                  "deal_status": "<string>",
                  "closed_price": <int>,
              }}
          ]
          ```

    '''
    return prompt

async def generate_conversation(iteration,customer_type,purchase_history,purchase_history_total_spend,current_cart_value,time_spent,previous_negotiations,min_selling_prize,curr_selling_prize,actual_selling_prize,current_negotiation,demanded_discount,model="gpt-4o-mini", temperature=0.7)->str:
    # Construct the prompt to provide context for the conversation
    system_prompt = '''You are a shopkeeper, who is trying to maximize the sales , keeping in mind to have maximum profit, negotiate with user as customer and attain profit as per the rules defined:
        Data Points -
          1. Customer Type (New/Returning): Whether the customer is visiting your platform for the first time or has made purchases before.
          2. Purchase History: Number of previous purchases and total spend.
          3. Cart Value: The current value of items in the customer's cart.
          4. Time on Site: How long the customer has been browsing during the current session.
          5. Geographical Location: Customer’s location (city, country) for regional offers.
          6. Chat Sentiment: The tone of the customer’s messages during the chat (positive, neutral, negative).


          1. Introductory Offer:
          Customer Segment: New Customer
          Target: New customers with no purchase history. (No purchase history, low cart value)
          Tactics: Offer a small discount to entice the customer to make their first purchase. Highlight product quality, customer reviews, and secure payment options to build trust.
          Iterations: 2
          Discount Flow Range Relative to Max Discount:
            - First Iteration: 20% - 30% of Max Discount
            - Second Iteration: 40% - 50% of Max Discount


          2. Loyalty Recognition:
          Customer Segment: Returning Customer
          Target: Returning customers with 1-2 previous purchases. (1-2 previous purchases, moderate cart value)
          Tactics: Recognize their loyalty with a small discount. Mention past positive experiences or purchases to reinforce their connection with your brand.
          Iterations: 3
          Discount Flow Range Relative to Max Discount:
            - First Iteration: 20% - 30% of Max Discount
            - Second Iteration: 30% - 45% of Max Discount
            - Third Iteration: 45% - 60% of Max Discount

          3. Value-Based Offer:
          Customer Segment: High Cart Value
          Target: Customers with a high cart value and who have spent a long time on the site. (High cart value, long time on site)
          Tactics: Offer a tiered discount that increases with cart value, encouraging them to add more items. Suggest small, complementary products to nudge them toward a higher discount tier.
          Iterations: 3
          Discount Flow Range Relative to Max Discount:
            - First Iteration: 20% - 30% of Max Discount
            - Second Iteration: 40% - 50% of Max Discount
            - Third Iteration: 75% - 100% of Max Discount

          4. Quick Close:
          Customer Segment: Low Cart Value
          Target: Customers with a low cart value and short time on the site. (Low cart value, short time on site)
          Tactics: Offer a small discount to encourage a quick purchase. Emphasize limited-time offers or low stock levels to create a sense of urgency.
          Iterations: 2
          Discount Flow Range Relative to Max Discount:
            - First Iteration: 30% - 45% of Max Discount
            - Second Iteration: 50% - 65% of Max Discount


          5. Build Trust:
          Customer Segment: Positive Sentiment
          Target: New customers with a positive chat sentiment. (Positive chat sentiment, new customer)
          Tactics: Reinforce their positive attitude by offering a small discount or a bonus item. Express appreciation for their interest and emphasize the benefits of your products.
          Iterations: 2
          Discount Flow Range Relative to Max Discount:
            - First Iteration: 20% - 30% of Max Discount
            - Second Iteration: 40% - 50% of Max Discount


          6. Resolve Concerns:
          Customer Segment: Negative Sentiment
          Target: Returning customers with a negative chat sentiment. (Negative chat sentiment, returning customer)
          Tactics: Acknowledge any issues or concerns raised during the chat. Offer a meaningful discount or other compensation to address their concerns and restore confidence in your brand.
          Iterations: 3
          Discount Flow Range Relative to Max Discount:
            - First Iteration: 45% - 55% of Max Discount
            - Second Iteration: 60% - 75% of Max Discount
            - Third Iteration: 85% - 100% of Max Discount

          7. Guided Decision:
          Customer Segment: Indecisive Customer
          Target: Indecisive customers with a high cart value. (Browsing for a long time, high cart value)
          Tactics: Provide helpful recommendations or comparisons to assist in their decision-making. Offer a small discount to incentivize them to finalize their purchase.
          Iterations: 3
          Discount Flow Range Relative to Max Discount:
            - First Iteration: 20% - 30% of Max Discount
            - Second Iteration: 40% - 50% of Max Discount
            - Third Iteration: 60% - 75% of Max Discount


          8. Urgency Close:
          Customer Segment: Time-Sensitive Customer
          Target: Time-sensitive customers with a high cart value. (Short time on site, high cart value)
          Tactics: Highlight the urgency of completing the purchase by focusing on time-limited discounts or limited stock availability. Offer instant rewards or discounts to encourage a quick close.
          Iterations: 2
          Discount Flow Range Relative to Max Discount:
            - First Iteration: 45% - 55% of Max Discount
            - Second Iteration: 75% - 100% of Max Discount

          Generate a single statement having variables (python compatible) to be used in form on json string in the given format
          ** Do not exceed the interation count **
          ** always generate discount in percentage **
          ** Use the previous conversation to analyse what discount has already been given to avoid reducing the discount **
          - Mention the status of negotiation under deal_status as closed once the deal is finalised on both ends, else set it as ongoing
          - Once the deal is closed, save price in closed_price variable, else set it as 0.
          - If the customer is ready to close the deal in the given bracket of discount then, close the deal without giving any furthur discount.
          - Don't exceed number of iterations and close the deal once iterations are exceeded.
          - If same amount is repeated more than three times, suggest the user to look for similar product and close the deal
          - 

          **Format for Output to be followed strictly**:
          After generating the conversation, structure it like this:

          ```json
          [
              {{
                  "statement": "<string>",
                  "discount_strategy": <int>,
                  "overall_chat_sentiment": "<string>",
                  "deal_status": "<string>",
                  "closed_price": <int>,
              }}
          ]
          ```

    '''
    prompt = get_user_prompt(iteration, customer_type, purchase_history, purchase_history_total_spend, current_cart_value, time_spent, previous_negotiations, min_selling_prize, curr_selling_prize, actual_selling_prize, current_negotiation, demanded_discount)

    # Call the OpenAI API to generate a conversation response
    response = ''
    try:
        response = await call_llm(api_key=key,model_name=model,system_prompt=system_prompt,user_prompt=prompt,temperature=temperature)
        response = response.choices[0].message['content'].strip()

        return response

    except Exception as e:
        # print(f"Error generating conversation: {e}")

        return response