import React from 'react';

// Assuming navigateTo is passed as a prop
const AboutUsPage = ({ navigateTo }) => (
    <div>
        <button
            style={{ position: 'absolute', top: '35px', right: '20px' }}
            onClick={() => navigateTo('home')}
        >
            Return to Home
        </button>

        <h1>Welcome to the About Us Page</h1>
        <p style={{textAlign: 'center', fontSize: '30px', fontFamily: "Andale Mono" }}>Our Mission</p>

        <p style={{ textAlign: 'center', fontSize: '20px', fontFamily: "Andale Mono" }}> At Debate Chatbot,  we are driven by a singular mission – to engage users in the art of debate.</p>
        <p style={{ textAlign: 'center', fontSize: '20px', fontFamily: "Andale Mono" }}> We believe in creating an immersive environment that not only encourages discourse but also fosters learning and critical thinking.</p>
        <p style={{ textAlign: 'center', fontSize: '20px', fontFamily: "Andale Mono" }}>Debate is not just a conversation; it's an exploration of ideas, a journey towards understanding diverse perspectives, and a catalyst for intellectual growth. Our platform is designed to be a vibrant hub where users can delve into meaningful discussions, challenge assumptions, and broaden their perspectives.</p>

        <p style={{ textAlign: 'center', fontSize: '20px' , fontFamily: "Andale Mono"}}>We envision a community that embraces the power of dialogue to stimulate intellectual curiosity and nurture a culture of lifelong learning. By providing a space for open and respectful debate, we aim to empower individuals to think critically, communicate effectively, and contribute meaningfully to the world of ideas.</p>

        <p style={{ textAlign: 'center', fontSize: '20px', fontFamily: "Andale Mono" }}>Join us on this exciting journey as we embark on a mission to cultivate a community where the art of debate becomes a catalyst for positive change.</p>

        <p style={{ textAlign: 'center', fontSize: '20px', fontFamily: "Andale Mono"}}>Debate Chatbot :)</p>

    </div>
);

export default AboutUsPage;
