import React, { useState } from 'react';
import axios from 'axios';

const ChatPage = () => {
    const [messages, setMessages] = useState([]);
    const [currentMessage, setCurrentMessage] = useState('');
    const [backendMessage, setBackendMessage] = useState('');

    const handleSendMessage = async (e) => {
        e.preventDefault();
        const trimmedMessage = currentMessage.trim();
        if (!trimmedMessage) return; // Ignore empty messages

        // Append the user message to the chat
        const newMessages = [...messages, { author: "User", text: trimmedMessage }];
        setMessages(newMessages);
        setCurrentMessage(''); // Clear the input field after sending

        try {
            // Make a POST request to the Flask backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: trimmedMessage }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.text();
            const botMessage = data ? JSON.parse(data) : "";
            setMessages([...newMessages, { author: "Bot", text: botMessage }]);
        } catch (error) {
            console.error('Error:', error);
            console.error('Network error:', error);
        }
    };

    const handleCheckBackend = async () => {
        try {
            const response = await axios.get('/api/check-connection', {
                headers: {
                }
            });
            setBackendMessage(response.data.message);

        } catch (error) {
            setBackendMessage('Error connecting to the backend');
        }
    };


    return (
        <div style={{ display: 'flex', height: '100vh' }}>
            {/* Chat section */}
            <div style={{ flex: 1, overflowY: 'auto', padding: '20px' }}>
                <h2>Chat with Us</h2>
                <div>
                    {messages.map((message, index) => (
                        <p key={index}>
                            <strong>{message.author}:</strong> {message.text}
                        </p>
                    ))}
                </div>
                <form onSubmit={handleSendMessage}>
                    <input
                        type="text"
                        value={currentMessage}
                        onChange={(e) => setCurrentMessage(e.target.value)}
                        placeholder="Type your message here..."
                        style={{ width: '70%', marginRight: '10px' }}
                    />
                    <button type="submit">Send</button>
                </form>
                <button onClick={handleCheckBackend}>Check Backend Connection</button>
                <p>{backendMessage}</p>
            </div>

            {/* Space reserved for conversation diagram or additional content */}
            <div style={{ flex: 1, backgroundColor: '#f0f0f0', padding: '20px' }}>
                <h2>Conversation Diagram</h2>
                {/* Implementation of the diagram will go here */}
            </div>
        </div>
    );
};

export default ChatPage;
