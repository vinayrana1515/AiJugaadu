-- Create the Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email email TYPE TEXT NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    customer_type VARCHAR(20) DEFAULT 'new'  -- 'new' or 'returning'
);


INSERT INTO users (username, email, password, phone, address, customer_type)
VALUES ('john_doe', 'john.doe@example.com', 'abcd', '092838923', '123 Example St', 'new');


CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    Cost_price FLOAT NOT NULL,
	Selling_price FLOAT  NOT NULL,
    minimum_price FLOAT, 
    image_of_product VARCHAR(255),
	Open_to_negotiation BOOLEAN DEFAULT FALSE
	);

	-- Create a trigger function to set minimum_price to Cost_price if it's NULL
CREATE OR REPLACE FUNCTION set_minimum_price()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.minimum_price IS NULL THEN
        NEW.minimum_price := NEW.Cost_price;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to invoke the function before inserting into products
CREATE TRIGGER trigger_set_minimum_price
BEFORE INSERT ON products
FOR EACH ROW
EXECUTE FUNCTION set_minimum_price();


-- Create the Orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'shipped', 'delivered', etc.
    total_amount FLOAT NOT NULL
);

CREATE TABLE purchase ( -- dropped
    purchase_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    Cost_price FLOAT NOT NULL,
    Selling_price FLOAT NOT NULL,
	purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Sessions table
CREATE TABLE sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    number_of_iterations INT NOT NULL,
    final_price DECIMAL(10, 2) NOT NULL,
    deal_or_no_deal BOOLEAN NOT NULL,  -- TRUE for deal, FALSE for no deal
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    session_id INT REFERENCES sessions(session_id) ON DELETE CASCADE,
    message_text TEXT NOT NULL
    
);

CREATE TABLE cart (
    cart_id SERIAL PRIMARY KEY,               
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE, 
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,  
    final_price DECIMAL(10, 2) NOT NULL     
    );

Drop Table purchase;


CREATE TABLE purchase (
    purchase_id SERIAL PRIMARY KEY,                 
    cart_id INT REFERENCES cart(cart_id) ON DELETE CASCADE,  
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,  
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,  
    cost_price FLOAT NOT NULL,                      
    selling_price FLOAT NOT NULL
);
	