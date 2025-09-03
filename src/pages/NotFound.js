import React from 'react';
import SEO from '../components/SEO';

const NotFound = () => {
  return (
    <>
      <SEO title="Page Not Found" description="The page you are looking for was not found." noindex={true} canonical="https://www.promptvita.com/404" />
      <div style={{ padding: '64px 24px', textAlign: 'center' }}>
        <h1>404 - Page Not Found</h1>
        <p>The page you are looking for might have been removed or is temporarily unavailable.</p>
        <a href="/" style={{ color: '#3b82f6', textDecoration: 'underline' }}>Go back home</a>
      </div>
    </>
  );
};

export default NotFound;

