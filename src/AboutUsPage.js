import React from 'react';

// Assuming navigateTo is passed as a prop
const AboutUsPage = ({ navigateTo }) => (
    <div style={{ position: 'relative' }}>
        {/* "Return to Home" button in the top-right */}
        <button
            style={{ position: 'absolute', top: '10px', right: '10px' }}
            onClick={() => navigateTo('home')}
        >
            Return to Home
        </button>

        <h1>Welcome to the About Us Page</h1>

        <h2>Our Mission</h2>

        <p> At Debate Chatbot,  we are driven by a singular mission – to engage users in the art of debate. We believe in creating an immersive environment that not only encourages discourse but also fosters learning and critical thinking.</p>

        <p>Debate is not just a conversation; it's an exploration of ideas, a journey towards understanding diverse perspectives, and a catalyst for intellectual growth. Our platform is designed to be a vibrant hub where users can delve into meaningful discussions, challenge assumptions, and broaden their perspectives.</p>

        <p>We envision a community that embraces the power of dialogue to stimulate intellectual curiosity and nurture a culture of lifelong learning. By providing a space for open and respectful debate, we aim to empower individuals to think critically, communicate effectively, and contribute meaningfully to the world of ideas.</p>

        <p>Join us on this exciting journey as we embark on a mission to cultivate a community where the art of debate becomes a catalyst for positive change.</p>

        <p>Debate Chatbot :)</p>

    </div>
);

export default AboutUsPage;
