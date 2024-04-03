import React from 'react';
import './HelpPage.css';

const HelpPage = ({ navigateTo }) => {
    return (
        <div className="container">
            
            <button
                style={{ position: 'absolute', top: '50px', right: '20px' }}
                onClick={() => navigateTo('home')}
            >
                Return to Home
            </button>

            <h1 style={{marginLeft: '600px'}}>Welcome to the Help Page</h1>
            <h2 style={{marginLeft: '600px'}}>If you have any questions or you are having trouble, please send us an email, thanks :) </h2>

        </div>
    );
};

export default HelpPage;
