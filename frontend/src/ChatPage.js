// Import necessary hooks and dependencies
import React, { useState } from 'react';
import { ForceGraph2D } from 'react-force-graph';
import './ChatPage.css';
import userLogo from './guy.jpg'; // Import user logo image
import botLogo from './bot.jpg'; // Import bot logo image

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  const addMessageToGraph = (userInput, botResponse) => {

    const timestamp = Date.now(); // Use a timestamp to create unique IDs
    const userNode = { id: `user-${timestamp}`, group: 'user', label: userInput };
    const botNode = { id: `bot-${timestamp}`, group: 'bot', label: botResponse };

    const newNodes = [...graphData.nodes, userNode, botNode];
    const newLinks = [...graphData.links, { source: `user-${timestamp}`, target: `bot-${timestamp}` }];

    setGraphData({ nodes: newNodes, links: newLinks });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault(); // Prevent the form from refreshing the page
    if (!currentMessage.trim()) return; // Ignore empty messages

    try {
      const response = await fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: currentMessage }),
      });

      const data = await response.json();
      if (data.answer) {
        const userMessage = { role: 'user', text: currentMessage };
        const botMessage = { role: 'bot', text: data.answer };

        setMessages(prevMessages => [...prevMessages, userMessage, botMessage]);
        addMessageToGraph(currentMessage, data.answer);
      }
    } catch (error) {
      console.error('Error:', error);
    }

    setCurrentMessage(''); // Clear the input field after sending
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* Chat section */}
      <div className="chatbot-container">
        <h2>Chat with Us</h2>
        <div className="messages-container">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role === 'user' ? 'user' : 'bot'}`}
            >
              <img
                src={message.role === 'user' ? userLogo : botLogo}
                alt={message.role}
                className="avatar"
              />
              <div className="message-text">{message.text}</div>
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            placeholder="Type your message..."
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>

      {/* Conversation Graph */}
      <div style={{ width: '100%', height: '500px' }}>
        <ForceGraph2D
          graphData={graphData}
          zoom={false}
          nodeAutoColorBy="group"
          nodeCanvasObject={(node, ctx, globalScale) => {
            const label = node.label;
            const fontSize = 12 / globalScale;
            ctx.font = `${fontSize}px Sans-Serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            const maxNodeWidth = 120;
            const words = label.split(' ');
            const lines = [];
            let line = '';

            words.forEach((word) => {
              const testLine = line + word + ' ';
              const metrics = ctx.measureText(testLine);
              if (metrics.width > maxNodeWidth && line) {
                lines.push(line);
                line = word + ' ';
              } else {
                line = testLine;
              }
            });

            if (line) {
              lines.push(line);
            }

            const lineHeight = fontSize * 1.2;
            const nodeHeight = lineHeight * lines.length;

            // Draw each line of text
            ctx.fillStyle = node.color || 'rgba(0,0,0,0.8)'; // Set text color
            let y = node.y - nodeHeight / 2 + lineHeight / 2;
            lines.forEach((ln) => {
              ctx.fillText(ln.trim(), node.x, y);
              y += lineHeight;
            });
          }}
          linkDirectionalArrowLength={5}
          linkDirectionalArrowRelPos={1}
          width={window.innerWidth}
          height={500}
        />
      </div>
    </div>
  );
};

export default ChatPage;
