-- Create the Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    customer_type VARCHAR(20) DEFAULT 'new'  -- 'new' or 'returning'
);

SELECT * FROM users;

INSERT INTO users (username, email, password, phone, address, customer_type)
VALUES ('john_doe', 'john.doe@example.com', 'abcd', '092838923', '123 Example St', 'new');

INSERT INTO users (username, email, password, phone, address, customer_type)
            VALUES ('john_doe_buddhu', 'john.doe3@example.com', 'abcdef', '0928389230', '123 Example St', 'new');

CREATE TABLE products (
    _id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
	image VARCHAR(255),
    description TEXT,
 
	price FLOAT  NOT NULL,

   countInStock INTEGER,
	rating FLOAT,
	numReviews INTEGER,
	Cost_price FLOAT NOT NULL,
	maximum_discount FLOAT, 
	Open_to_negotiation BOOLEAN DEFAULT FALSE
	);
	
	UPDATE products SET countInStock = 0 WHERE _id=6;
	
	UPDATE products SET maximum_discount = 70 WHERE _id=1;
	UPDATE products SET maximum_discount = 450 WHERE _id=2;
	UPDATE products SET maximum_discount = 850 WHERE _id=3;
	UPDATE products SET maximum_discount = 250 WHERE _id=4;
	UPDATE products SET maximum_discount = 35 WHERE _id=5;
	UPDATE products SET maximum_discount = 32 WHERE _id=6;
	
INSERT INTO products (name,image, description, price,countInStock,rating,numReviews,Cost_price,maximum_discount,Open_to_negotiation)
            VALUES ('Airpods Wireless Bluetooth Headphones', 
					'/images/airpods.jpg',
					'Bluetooth technology lets you connect it with compatible devices wirelessly High-quality AAC audio offers immersive listening experience Built-in microphone allows you to take calls while working',
					
					89.99,
					10,
					4.5,
					10,
					60.00,
					15.00,
					FALSE),(
						'iPhone 11 Pro 256GB Memory', 
					'/images/phone.jpg',
					'Introducing the iPhone 11 Pro. A transformative triple-camera system that adds tons of capability without complexity. An unprecedented leap in battery life',
					
					599.99,
					7,
					4.0,
					8,
					400.00,
					15.00,
					FALSE
					
					),(
						'Cannon EOS 80D DSLR Camera', 
					'/images/camera.jpg',
					'Characterized by versatile imaging specs, the Canon EOS 80D further clarifies itself using a pair of robust focusing systems and an intuitive design',
					
					929.99,
					5,
					3.0,
					12,
					800.00,
					15.00,
					FALSE
					
					),(
						'Sony Playstation 4 Pro White Version', 
					'/images/playstation.jpg',
					'The ultimate home entertainment center starts with PlayStation. Whether you are into gaming, HD movies, television, music',
					
					399.99,
					11,
					5.0,
					12,
					200.00,
					15.00,
					FALSE
					
					),(
						'Logitech G-Series Gaming Mouse', 
					'/images/mouse.jpg',
					'Get a better handle on your games with this Logitech LIGHTSYNC gaming mouse. The six programmable buttons allow customization for a smooth playing experience',
					
					49.99,
					7,
					3.5,
					10,
					25.00,
					15.00,
					FALSE
					
					),(
						'Amazon Echo Dot 3rd Generation', 
					'/images/alexa.jpg',
					'Meet Echo Dot - Our most popular smart speaker with a fabric design. It is our most compact smart speaker that fits perfectly into small space',
					
					49.99,
					7,
					3.5,
					10,
					25.00,
					15.00,
					FALSE
					
					)
					;
	DROP TABLE products;
	
	SELECT * FROM products;
	
	



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

select * from products;




-- Create the Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    customer_type VARCHAR(20) DEFAULT 'new'  -- 'new' or 'returning'
);

SELECT * FROM users;

INSERT INTO users (username, email, password, phone, address, customer_type)
VALUES ('john_doe', 'john.doe@example.com', 'abcd', '092838923', '123 Example St', 'new');

INSERT INTO users (username, email, password, phone, address, customer_type)
            VALUES ('john_doe_buddhu', 'john.doe3@example.com', 'abcdef', '0928389230', '123 Example St', 'new');

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
    product_id INT REFERENCES products(_id) ON DELETE CASCADE,
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
    product_id INT REFERENCES products(_id) ON DELETE CASCADE, 
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,  
    final_price DECIMAL(10, 2) NOT NULL     
    );

Drop Table purchase;


CREATE TABLE purchase (
    purchase_id SERIAL PRIMARY KEY,                 
    cart_id INT REFERENCES cart(cart_id) ON DELETE CASCADE,  
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,  
    product_id INT REFERENCES products(_id) ON DELETE CASCADE,  
    cost_price FLOAT NOT NULL,                      
    selling_price FLOAT NOT NULL
);



ALTER TABLE orders
ADD COLUMN product_id INT;

ALTER TABLE orders
ADD CONSTRAINT fk_product
FOREIGN KEY (product_id) REFERENCES products(_id) ON DELETE CASCADE;


-- Step 1: Remove final_price and product_id from the cart table
ALTER TABLE cart
DROP COLUMN final_price,
DROP COLUMN product_id;

-- Step 2: Add final_price and product_id to the purchase table
ALTER TABLE purchase
ADD COLUMN final_price DECIMAL(10, 2) NOT NULL;

-- Step 3: Remove cost_price and selling_price from the purchase table
ALTER TABLE purchase
DROP COLUMN cost_price,
DROP COLUMN selling_price;





-- Inserting data into the products table
INSERT INTO products (name, description, Cost_price, Selling_price, minimum_price, image_of_product, Open_to_negotiation)
VALUES 
('Basmati Rice', 'Premium long grain rice, 5kg', 400.00, 600.00, 500.00, 'https://example.com/images/basmati.jpg', TRUE),
('Darjeeling Tea', 'Organic Darjeeling black tea, 500g', 300.00, 450.00, 350.00, 'https://example.com/images/tea.jpg', TRUE),
('Mysore Silk Saree', 'Traditional Mysore silk saree', 8000.00, 12000.00, 10000.00, 'https://example.com/images/silk_saree.jpg', FALSE),
('Handmade Terracotta Pot', 'Eco-friendly terracotta flower pot', 150.00, 250.00, 200.00, 'https://example.com/images/terracotta.jpg', TRUE),
('Khadi Cotton Shirt', '100% pure khadi cotton shirt for men', 700.00, 1200.00, 900.00, 'https://example.com/images/khadi_shirt.jpg', TRUE),
('Kashmiri Shawl', 'Handwoven pashmina shawl', 5000.00, 8000.00, 6500.00, 'https://example.com/images/shawl.jpg', FALSE),
('Spice Box', 'Traditional wooden spice box with 9 compartments', 300.00, 500.00, 400.00, 'https://example.com/images/spice_box.jpg', TRUE),
('Chikankari Kurta', 'Lucknowi Chikankari Kurta for women', 1200.00, 1800.00, 1500.00, 'https://example.com/images/chikankari_kurta.jpg', TRUE),
('Brass Idols', 'Handcrafted brass idols of Hindu deities', 2000.00, 3500.00, 2500.00, 'https://example.com/images/brass_idol.jpg', FALSE),
('Handloom Bedsheet', 'Cotton handloom bedsheet, double size', 900.00, 1500.00, 1200.00, 'https://example.com/images/handloom_bedsheet.jpg', TRUE);



