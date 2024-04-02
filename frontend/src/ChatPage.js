import React, { useState, useEffect } from 'react';

const ChatPage = () => {
    const [messages, setMessages] = useState([]);
    const [currentMessage, setCurrentMessage] = useState('');
    const [conversationDiagram, setConversationDiagram] = useState('');

    useEffect(() => {
        // Load the conversation flow diagram image when the component mounts
        const loadImage = async () => {
            try {
                const diagram = require('./conversation_flow.png');
                setConversationDiagram(diagram.default);
            } catch (error) {
                console.error('Error loading conversation flow diagram:', error);
            }
        };

        loadImage();
    }, []);

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

            {/* Space reserved for conversation diagram */}
            <div style={{ flex: 1, backgroundColor: '#f0f0f0', padding: '20px' }}>
                <h2>Conversation Diagram</h2>
                {conversationDiagram && <img src={conversationDiagram} alt="Conversation Flow" style={{ maxWidth: '100%' }} />}
            </div>
        </div>
    );
};

export default ChatPage;
