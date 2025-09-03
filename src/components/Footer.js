import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-brand">
          <div className="brand-icon">⚡</div>
          <div>
            <div className="brand-name">PromptVita</div>
            <div className="brand-tag">Turn messy prompts into powerful AI instructions.</div>
          </div>
        </div>
        <div className="footer-links">
          <a href="/about">About</a>
          <a href="/pricing">Pricing</a>
          <a href="https://www.promptvita.com/sitemap.xml" target="_blank" rel="noreferrer">Sitemap</a>
        </div>
      </div>
      <div className="footer-bottom">
        <span>© {new Date().getFullYear()} PromptVita</span>
        <span className="dot">•</span>
        <span><a href="https://twitter.com/promptvita" target="_blank" rel="noreferrer">Twitter</a></span>
      </div>
    </footer>
  );
};

export default Footer;

