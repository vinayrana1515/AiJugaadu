// import React from "react";
// import { Button } from "react-bootstrap";

// const ChatBot = ({ onClose }) => {
//   return (
//     <div className='chatbot-window'>
//       <div className='chatbot-header'>
//         <h4>Chat with Us</h4>
//         <Button variant='close' onClick={onClose} />
//       </div>
//       <div className='chatbot-body'>
//         {/* Chat interface here */}
//         <p>Hello! How can we assist you today?</p>
//       </div>
//     </div>
//   );
// };

// export default ChatBot;

import React, { useState } from "react";
import { Button, Form, ListGroup } from "react-bootstrap";
//import "./ChatBot.css"; // Make sure to include your CSS

const ChatBot = ({ onClose, productId }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");

  const handleSend = async (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      setMessages([...messages, { text: inputValue, sender: "user" }]);

      try {
        const response = await fetch("http://127.0.0.1:5002/process-llm", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: inputValue,
            product_id: productId, // Adding product ID to the request body
          }),
        });
        const data = await response.json();

        // Add the chatbot's response to the chat
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: data.response[0].statement, sender: "bot" },
        ]);
      } catch (error) {
        console.error("Error fetching chatbot response:", error);
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "Sorry, something went wrong.", sender: "bot" },
        ]);
      }
      setInputValue("");

      // Simulate a bot response (you can customize this)
      // setTimeout(() => {
      //   setMessages((prevMessages) => [
      //     ...prevMessages,
      //     {
      //       text: "Thank you for your message! We'll get back to you shortly.",
      //       sender: "bot",
      //     },
      //   ]);
      // }, 1000);
    }
  };

  return (
    <div className='chatbot-window'>
      <div className='chatbot-header'>
        <h4>Chat with Us</h4>
        <Button variant='close' onClick={onClose} />
      </div>
      <div className='chatbot-body'>
        <ListGroup>
          {messages.map((msg, index) => (
            <ListGroup.Item key={index} className={msg.sender}>
              {msg.text}
            </ListGroup.Item>
          ))}
        </ListGroup>
      </div>
      <Form onSubmit={handleSend} className='chatbot-input'>
        <Form.Group controlId='messageInput'>
          <Form.Control
            type='text'
            placeholder='Type a message...'
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
        </Form.Group>
        <Button type='submit'>Send</Button>
      </Form>
    </div>
  );
};

export default ChatBot;
