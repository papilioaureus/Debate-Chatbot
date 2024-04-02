import React, { useState, useEffect } from 'react';
import mermaid from 'mermaid';

// Initialize Mermaid
mermaid.initialize({
  startOnLoad: true,
});

const ChatDiagram = ({ conversation }) => {
  // State to hold the Mermaid chart definition
  const [chartDefinition, setChartDefinition] = useState('');

  useEffect(() => {
    // Generate Mermaid sequence diagram definition based on conversation
    const generateSequenceDiagramDefinition = (conversation) => {
      let definition = `
        sequenceDiagram
        participant User
        participant Chatbot`;

      // Add messages to appropriate lanes
      conversation.forEach((msg, index) => {
        if (msg.user === 'User') {
          definition += `
            User->>Chatbot: ${msg.text}`;
        } else {
          definition += `
            Chatbot->>User: ${msg.text}`;
        }
      });
      return definition;
    };

    // Update chart definition whenever conversation changes
    setChartDefinition(generateSequenceDiagramDefinition(conversation));
  }, [conversation]);

  return (
    <div>
      <div className="mermaid">{chartDefinition}</div>
    </div>
  );
};

export default ChatDiagram;
