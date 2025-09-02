import React from 'react';

const StructuredData = ({ data }) => {
  React.useEffect(() => {
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(data);
    script.id = 'structured-data';
    
    // Remove existing structured data script if it exists
    const existingScript = document.getElementById('structured-data');
    if (existingScript) {
      document.head.removeChild(existingScript);
    }
    
    document.head.appendChild(script);
    
    return () => {
      const scriptToRemove = document.getElementById('structured-data');
      if (scriptToRemove) {
        document.head.removeChild(scriptToRemove);
      }
    };
  }, [data]);

  return null;
};

// Predefined structured data schemas
export const homePageSchema = {
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "PromptVita",
  "description": "AI-powered prompt optimization tool that transforms messy prompts into powerful AI instructions",
  "url": "https://www.promptvita.com",
  "applicationCategory": "ProductivityApplication",
  "operatingSystem": "Any",
  "browserRequirements": "Requires JavaScript",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD",
    "description": "Free plan available"
  },
  "creator": {
    "@type": "Organization",
    "name": "PromptVita",
    "url": "https://www.promptvita.com",
    "logo": "https://www.promptvita.com/logo.png"
  },
  "featureList": [
    "AI-powered prompt optimization",
    "Grammar and text correction", 
    "Multiple context options",
    "Professional text enhancement",
    "Real-time optimization",
    "Copy and save functionality"
  ],
  "screenshot": "https://www.promptvita.com/screenshot.png"
};

export const aboutPageSchema = {
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "name": "About PromptVita",
  "description": "Learn about PromptVita's mission to democratize prompt engineering and help users create better AI prompts",
  "url": "https://www.promptvita.com/about",
  "mainEntity": {
    "@type": "Organization",
    "name": "PromptVita",
    "description": "AI-powered prompt optimization platform",
    "url": "https://www.promptvita.com",
    "foundingDate": "2024",
    "sameAs": [
      "https://twitter.com/promptvita",
      "https://linkedin.com/company/promptvita"
    ],
    "knowsAbout": [
      "Prompt Engineering",
      "AI Optimization",
      "Natural Language Processing",
      "Text Enhancement",
      "Grammar Correction"
    ]
  }
};

export const pricingPageSchema = {
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "PromptVita",
  "description": "AI-powered prompt optimization tool with flexible pricing plans",
  "url": "https://www.promptvita.com/pricing",
  "brand": {
    "@type": "Brand",
    "name": "PromptVita"
  },
  "offers": [
    {
      "@type": "Offer",
      "name": "Free Plan",
      "description": "Perfect for getting started with prompt optimization",
      "price": "0",
      "priceCurrency": "USD",
      "billingIncrement": "P1M",
      "eligibleQuantity": {
        "@type": "QuantitativeValue",
        "value": 10,
        "unitText": "optimizations per day"
      }
    },
    {
      "@type": "Offer", 
      "name": "Pro Plan",
      "description": "Ideal for professionals and content creators",
      "price": "5",
      "priceCurrency": "USD",
      "billingIncrement": "P1M",
      "eligibleQuantity": {
        "@type": "QuantitativeValue",
        "value": "unlimited",
        "unitText": "optimizations"
      }
    },
    {
      "@type": "Offer",
      "name": "Enterprise Plan", 
      "description": "Built for teams and organizations",
      "price": "9",
      "priceCurrency": "USD",
      "billingIncrement": "P1M",
      "eligibleQuantity": {
        "@type": "QuantitativeValue",
        "value": "unlimited",
        "unitText": "optimizations"
      }
    }
  ]
};

export default StructuredData;
