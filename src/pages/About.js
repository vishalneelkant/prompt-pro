import React from 'react';
import SEO from '../components/SEO';
import StructuredData, { aboutPageSchema } from '../components/StructuredData';
import './About.css';

const About = () => {
  return (
    <>
      <SEO 
        title="About PromptVita - AI-Powered Prompt Optimization Platform"
        description="Learn about PromptVita's mission to democratize prompt engineering. Discover how our AI-powered platform helps users create better prompts and improve AI interactions."
        keywords="about promptvita, prompt engineering platform, AI optimization tool, prompt improvement, AI writing assistant, prompt enhancement service"
        canonical="https://www.promptvita.com/about"
      />
      <StructuredData data={aboutPageSchema} />
      <div className="about">
      <div className="about-container">
        <div className="about-hero">
          <div className="hero-icon">⚡</div>
          <h1>About PromptVita</h1>
          <p className="hero-subtitle">
            Transform your messy prompts into powerful AI instructions with our intelligent optimization platform.
          </p>
        </div>

        <div className="about-content">
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Smart Optimization</h3>
              <p>
                Our advanced AI analyzes your prompts and applies proven optimization strategies 
                to improve clarity, specificity, and effectiveness.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🚀</div>
              <h3>Multiple Contexts</h3>
              <p>
                Optimize prompts for various use cases including business, technical, academic, 
                marketing, and creative applications.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">✨</div>
              <h3>Instant Results</h3>
              <p>
                Get optimized prompts in seconds with detailed explanations of the applied 
                strategies and improvements made.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📝</div>
              <h3>Grammar Correction</h3>
              <p>
                Beyond prompt optimization, we also offer text correction and grammar 
                improvement for professional communication.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">💾</div>
              <h3>Save & Organize</h3>
              <p>
                Build your personal library of optimized prompts for easy access and 
                reuse across different projects.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🔄</div>
              <h3>Iterative Improvement</h3>
              <p>
                Continuously refine your prompts with our re-optimization feature to 
                achieve the best possible results.
              </p>
            </div>
          </div>

          <div className="about-mission">
            <h2>Our Mission</h2>
            <p>
              At PromptVita, we believe that effective communication with AI starts with well-crafted prompts. 
              Our mission is to democratize prompt engineering by making it accessible to everyone, regardless 
              of their technical background. We're committed to helping users unlock the full potential of AI 
              through better prompts.
            </p>
          </div>

          <div className="about-stats">
            <div className="stat-item">
              <div className="stat-number">100+</div>
              <div className="stat-label">Prompts Optimized</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">95%</div>
              <div className="stat-label">Improvement Rate</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">10+</div>
              <div className="stat-label">Happy Users</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Available</div>
            </div>
          </div>

          <div className="about-cta">
            <h2>Ready to Optimize Your Prompts?</h2>
            <p>Join thousands of users who have already improved their AI interactions with PromptVita.</p>
            <a href="/" className="cta-button">Start Optimizing</a>
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default About;
