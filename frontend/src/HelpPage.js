import React, { useState } from 'react';

// Assuming navigateTo is passed as a prop
const HelpPage = ({ navigateTo }) => {
    const [userInput, setUserInput] = useState('');

    const handleInputChange = (event) => {
        setUserInput(event.target.value);
    };

    const handleFormSubmit = (event) => {
        event.preventDefault();
        // Here, you can handle the user's input, such as sending it to a backend or processing it in some way.
        // For now, let's just log it to the console.
        console.log('User input:', userInput);

        // Clear the text area by resetting the state
        setUserInput('');
    };

    return (
        <div style={{ position: 'relative' }}>
            {/* "Return to Home" button in the top-right */}
            <button
                style={{ position: 'absolute', top: '10px', right: '10px' }}
                onClick={() => navigateTo('home')}
            >
                Return to Home
            </button>

            <h1>Welcome to the Help Page</h1>
            <h2>Our Mission</h2>
            <p>Engage users in the art of debate through creating an environment that fosters learning and critical thinking.</p>

            <h1>How can we help you?</h1>

            <form onSubmit={handleFormSubmit}>
                <label>

                    <textarea
                        value={userInput}
                        onChange={handleInputChange}
                        placeholder="Type your help request here..."
                        rows="4"
                        cols="50"
                    />
                </label>
                <br />
                <button type="submit">Submit</button>
            </form>

            <h1>Frequent questions:</h1>
            <p>1. </p>
            <p>2. </p>
            <p>3. </p>
            <p>4. </p>
        </div>
    );
};

export default HelpPage;
