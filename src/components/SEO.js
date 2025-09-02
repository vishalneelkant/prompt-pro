import React from 'react';

const SEO = ({ 
  title, 
  description, 
  keywords, 
  canonical, 
  ogImage, 
  ogType = "website",
  twitterCard = "summary_large_image",
  noindex = false 
}) => {
  const siteUrl = "https://www.promptvita.com";
  const defaultTitle = "PromptVita - Transform Messy Prompts into Powerful AI Instructions";
  const defaultDescription = "Turn your messy prompts into powerful AI instructions with PromptVita. AI-powered prompt optimization, grammar correction, and professional text enhancement. Try free!";
  const defaultKeywords = "prompt optimization, AI prompts, prompt engineering, text correction, grammar checker, AI writing, prompt enhancer, ChatGPT prompts";
  
  const pageTitle = title ? `${title} | PromptVita` : defaultTitle;
  const pageDescription = description || defaultDescription;
  const pageKeywords = keywords || defaultKeywords;
  const pageCanonical = canonical || siteUrl;
  const pageOgImage = ogImage || `${siteUrl}/og-image.png`;

  React.useEffect(() => {
    // Update document title
    document.title = pageTitle;
    
    // Update meta description
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.setAttribute('content', pageDescription);
    }
    
    // Update meta keywords
    const metaKeywords = document.querySelector('meta[name="keywords"]');
    if (metaKeywords) {
      metaKeywords.setAttribute('content', pageKeywords);
    }
    
    // Update canonical URL
    let canonical = document.querySelector('link[rel="canonical"]');
    if (canonical) {
      canonical.setAttribute('href', pageCanonical);
    } else {
      canonical = document.createElement('link');
      canonical.setAttribute('rel', 'canonical');
      canonical.setAttribute('href', pageCanonical);
      document.head.appendChild(canonical);
    }
    
    // Update robots meta tag
    let robotsMeta = document.querySelector('meta[name="robots"]');
    if (robotsMeta) {
      robotsMeta.setAttribute('content', noindex ? 'noindex, nofollow' : 'index, follow');
    } else {
      robotsMeta = document.createElement('meta');
      robotsMeta.setAttribute('name', 'robots');
      robotsMeta.setAttribute('content', noindex ? 'noindex, nofollow' : 'index, follow');
      document.head.appendChild(robotsMeta);
    }
    
    // Update Open Graph tags
    const updateOgTag = (property, content) => {
      let ogTag = document.querySelector(`meta[property="${property}"]`);
      if (ogTag) {
        ogTag.setAttribute('content', content);
      } else {
        ogTag = document.createElement('meta');
        ogTag.setAttribute('property', property);
        ogTag.setAttribute('content', content);
        document.head.appendChild(ogTag);
      }
    };
    
    updateOgTag('og:title', pageTitle);
    updateOgTag('og:description', pageDescription);
    updateOgTag('og:url', pageCanonical);
    updateOgTag('og:image', pageOgImage);
    updateOgTag('og:type', ogType);
    
    // Update Twitter Card tags
    const updateTwitterTag = (name, content) => {
      let twitterTag = document.querySelector(`meta[name="${name}"]`);
      if (twitterTag) {
        twitterTag.setAttribute('content', content);
      } else {
        twitterTag = document.createElement('meta');
        twitterTag.setAttribute('name', name);
        twitterTag.setAttribute('content', content);
        document.head.appendChild(twitterTag);
      }
    };
    
    updateTwitterTag('twitter:title', pageTitle);
    updateTwitterTag('twitter:description', pageDescription);
    updateTwitterTag('twitter:image', pageOgImage);
    updateTwitterTag('twitter:card', twitterCard);
    
  }, [pageTitle, pageDescription, pageKeywords, pageCanonical, pageOgImage, ogType, twitterCard, noindex]);

  return null; // This component doesn't render anything
};

export default SEO;
