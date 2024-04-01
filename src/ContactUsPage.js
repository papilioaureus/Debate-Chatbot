import React from 'react';

// Assuming navigateTo is passed as a prop
const ContactUsPage = ({ navigateTo }) => (
    <div style={{ position: 'relative' }}>
        {/* "Return to Home" button in the top-right */}
        <button
            style={{ position: 'absolute', top: '10px', right: '10px' }}
            onClick={() => navigateTo('home')}
        >
            Return to Home
        </button>
        <h1>Welcome to the Contact Us Page</h1>
        <p>Telephone: </p>
        <p>Mail: </p>
        <p>Location: </p>

    </div>
);

export default ContactUsPage;
