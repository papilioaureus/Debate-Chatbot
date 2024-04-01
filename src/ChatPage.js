import React, { useState } from 'react';

const ChatPage = () => {
    const [messages, setMessages] = useState([]);
    const [currentMessage, setCurrentMessage] = useState('');

    const handleSendMessage = (e) => {
        e.preventDefault(); // Prevent the form from refreshing the page
        if (!currentMessage.trim()) return; // Ignore empty messages
        setMessages([...messages, currentMessage]);
        setCurrentMessage(''); // Clear the input field after sending
    };

    return (
        <div style={{ display: 'flex', height: '100vh' }}>
            {/* Chat section */}
            <div style={{ flex: 1, overflowY: 'auto', padding: '20px' }}>
                <h2>Chat with Us</h2>
                <div>
                    {messages.map((msg, index) => (
                        <p key={index}>{msg}</p>
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
