import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import LoginModal from './LoginModal';
import './Navigation.css';

const Navigation = () => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  const handleLoginClick = () => {
    setShowLoginModal(true);
  };

  const handleLibraryClick = (e) => {
    e.preventDefault();
    // Do nothing as per requirements
  };

  return (
    <>
      <nav className="navigation">
        <div className="nav-container">
          {/* Logo */}
          <Link to="/" className="nav-logo">
            <div className="nav-logo-icon">⚡</div>
            <span className="nav-logo-text">PromptPro</span>
          </Link>

          {/* Navigation Menu */}
          <div className="nav-menu">
            <Link 
              to="/" 
              className={`nav-item ${isActive('/') ? 'active' : ''}`}
            >
              Home
            </Link>
            <Link 
              to="/about" 
              className={`nav-item ${isActive('/about') ? 'active' : ''}`}
            >
              About
            </Link>
            <button 
              onClick={handleLibraryClick}
              className="nav-item nav-library-btn"
            >
              Library
            </button>
            <Link 
              to="/pricing" 
              className={`nav-item ${isActive('/pricing') ? 'active' : ''}`}
            >
              Pricing
            </Link>
            <button 
              onClick={handleLoginClick}
              className="nav-item nav-login-btn"
            >
              Login
            </button>
          </div>
        </div>
      </nav>

      {/* Login Modal */}
      {showLoginModal && (
        <LoginModal onClose={() => setShowLoginModal(false)} />
      )}
    </>
  );
};

export default Navigation;
