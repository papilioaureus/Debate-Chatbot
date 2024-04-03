import React from 'react';

// Assuming navigateTo is passed as a prop
const ForumPage = ({ navigateTo }) => (
    <div style={{ position: 'relative' }}>
        {/* "Return to Home" button in the top-right */}
        <button
            style={{ position: 'absolute', top: '10px', right: '10px' }}
            onClick={() => navigateTo('home')}
        >
            Return to Home
        </button>

        <h1>Welcome to our Forum Page</h1>
        <p>Here you can chat with other people and .....</p>

    </div>
);

export default ForumPage;
