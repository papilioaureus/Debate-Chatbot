// HomePage.js
import React from 'react';
import './HomePage.css';

const HomePage = ({ navigateTo }) => {
    return (
        <div className="homepage-container">
            <div className="links">
                <button onClick={() => navigateTo('about')}>About Us</button> |
                <button onClick={() => navigateTo('forum')}>Forum</button> |
                <button onClick={() => navigateTo('help')}>Help</button> |
                <button onClick={() => navigateTo('contact')}>Contact Us</button>
            </div>
            <h1 className="title">WELCOME TO</h1>
            <button className="start-chat-button" onClick={() => navigateTo('chat')}>
                Start ChatBot
            </button>

        </div>
    );
};

export default HomePage;
