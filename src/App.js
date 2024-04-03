import React, { useState } from 'react';
import HomePage from './HomePage';
import ChatPage from './ChatPage';
import AboutUsPage from './AboutUsPage'; // Make sure the path is correct
import ForumPage from './ForumPage'; // Make sure the path is correct
import HelpPage from './HelpPage'; // Make sure the path is correct
import ContactUsPage from './ContactUsPage'; // Make sure the path is correct

// Import or define additional components for About Us, Forum, Help, Contact Us

const Page = {
    HOME: "home",
    CHAT: "chat",
    ABOUT: "about",
    FORUM: "forum",
    HELP: "help",
    CONTACT: "contact",
    // Define other pages as needed
};

const App = () => {
    const [currentPage, setCurrentPage] = useState(Page.HOME);

    const navigateTo = (page) => {
        setCurrentPage(page);
    };

    const renderPage = () => {
        switch (currentPage) {
            case Page.CHAT:
                return <ChatPage />;
            case Page.ABOUT:
                return <AboutUsPage navigateTo={navigateTo} />;
            case Page.FORUM:
                return <ForumPage navigateTo={navigateTo} />;
            case Page.HELP:
                return <HelpPage navigateTo={navigateTo} />;
            case Page.CONTACT:
                return <ContactUsPage navigateTo={navigateTo} />;
            default:
                return <HomePage navigateTo={navigateTo} />;
        }
    };

    return (
        <div>
            {renderPage()}
        </div>
    );
};

export default App;
