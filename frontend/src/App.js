import React, { useState } from 'react';
import HomePage from './HomePage';
import ChatPage from './ChatPage';
import AboutUsPage from './AboutUsPage'; // Make sure the path is correct
import HelpPage from './HelpPage'; // Make sure the path is correct

const Page = {
    HOME: "home",
    CHAT: "chat",
    ABOUT: "about",
    HELP: "help",
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
            case Page.HELP:
                return <HelpPage navigateTo={navigateTo} />;
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
