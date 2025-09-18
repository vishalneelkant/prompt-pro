import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import SEO from '../components/SEO';
import StructuredData, { homePageSchema } from '../components/StructuredData';
import './Home.css';

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [context, setContext] = useState('general');
  const [copyFeedback, setCopyFeedback] = useState({ show: false, message: '', type: '' });
  const [charCount, setCharCount] = useState(0);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await axios.post('/api/optimize', {
        prompt: inputValue,
        context: context
      });

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        original: response.data.original,
        strategy: response.data.strategy,
        optimized: response.data.optimized,
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error optimizing prompt:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error while optimizing your prompt. Please try again.',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const copyToClipboard = async (text, buttonType = 'main') => {
    try {
      await navigator.clipboard.writeText(text);
      
      setCopyFeedback({
        show: true,
        message: 'Copied to clipboard!',
        type: 'success'
      });

      if (buttonType === 'top') {
        const topButton = document.querySelector('.copy-button');
        if (topButton) {
          topButton.classList.add('copy-success');
          setTimeout(() => topButton.classList.remove('copy-success'), 1000);
        }
      } else if (buttonType === 'main') {
        const mainButton = document.querySelector('.copy-btn');
        if (mainButton) {
          mainButton.classList.add('copy-success');
          setTimeout(() => mainButton.classList.remove('copy-success'), 1000);
        }
      }

      setTimeout(() => {
        setCopyFeedback({ show: false, message: '', type: '' });
      }, 2000);

    } catch (err) {
      setCopyFeedback({
        show: true,
        message: 'Failed to copy. Please try again.',
        type: 'error'
      });

      setTimeout(() => {
        setCopyFeedback({ show: false, message: '', type: '' });
      }, 3000);
    }
  };

  const getLatestMessage = () => {
    return messages[messages.length - 1];
  };

  const latestMessage = getLatestMessage();

  return (
    <>
      <SEO 
        title="PromptVita - AI Prompt Engineer & Cursor Prompt Optimizer"
        description="Transform messy prompts into powerful AI instructions. Free AI-powered prompt engineering, grammar correction, and professional text enhancement. Multiple contexts available."
        keywords="AI prompt engineer, AI prompts, ChatGPT prompts, prompt engineering, grammar checker, text correction, AI writing assistant, prompt enhancer, Cursor prompt optimizer"
        canonical="https://www.promptvita.com/"
      />
      <StructuredData data={homePageSchema} />
      <div className="home">
      {/* Copy Feedback Toast */}
      {copyFeedback.show && (
        <div className={`copy-feedback ${copyFeedback.type}`}>
          <div className="feedback-icon">
            {copyFeedback.type === 'success' ? '✅' : '❌'}
          </div>
          <span className="feedback-message">{copyFeedback.message}</span>
        </div>
      )}

      <div className="home-container">
        {/* Left Panel - Input */}
        <div className="left-panel">
          <div className="input-section">
            <h1 className="main-title">
              {context === 'rephrase' 
                ? 'PromptVita – Turn messy text into polished, professional writing.' 
                : context === 'cursor_code_optimizer'
                ? 'PromptVita – AI Prompt Engineer for Cursor code optimization.'
                : 'PromptVita – AI Prompt Engineer for powerful AI instructions.'
              }
            </h1>
            
            <form onSubmit={handleSubmit} className="input-form">
              <div className="input-group">
                <textarea
                  className="input-field"
                  value={inputValue}
                  onChange={(e) => { setInputValue(e.target.value); setCharCount(e.target.value.length); }}
                  onKeyPress={handleKeyPress}
                  placeholder={
                    context === 'rephrase' 
                      ? "e.g., i recieve ur messege and will definately respond"
                      : context === 'cursor_code_optimizer'
                      ? "e.g., Add user authentication to my React app with login/signup forms"
                      : "e.g., Write a business plan for an AI startup in fintech."
                  }
                  disabled={isLoading}
                  rows={4}
                  aria-label="Enter your prompt or text to optimize"
                  aria-describedby="input-help-text"
                  role="textbox"
                />
                <div className="counter-row">
                  <span id="input-help-text">Tip: Be specific about role, task, constraints, and examples.</span>
                  <span aria-live="polite">{charCount} chars</span>
                </div>
              </div>
              
              <div className="input-group">
                <select 
                  className="context-dropdown"
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                  aria-label="Select optimization context"
                  aria-describedby="context-help-text"
                >
                  <option value="general">Select context</option>
                  <option value="cursor_code_optimizer">Cursor Code Optimizer</option>
                  <option value="rephrase">Rephrase & Grammar</option>
                  <option value="technical">Technical</option>
                  <option value="academic">Academic</option>
                  <option value="image_generation">Image Generation</option>
                  <option value="video_generation">Video Generation</option>
                </select>
              </div>
              
              <button
                type="submit"
                className="optimize-button"
                disabled={!inputValue.trim() || isLoading}
                aria-label={isLoading 
                  ? (context === 'rephrase' ? 'Correcting text...' : context === 'cursor_code_optimizer' ? 'Optimizing code prompt...' : 'Optimizing prompt...') 
                  : (context === 'rephrase' ? 'Correct text' : context === 'cursor_code_optimizer' ? 'Optimize for Cursor' : 'Optimize prompt')
                }
                aria-describedby="button-help-text"
              >
                {isLoading 
                  ? (context === 'rephrase' ? 'Correcting...' : context === 'cursor_code_optimizer' ? 'Optimizing Code...' : 'Optimizing...') 
                  : (context === 'rephrase' ? 'Correct Text' : context === 'cursor_code_optimizer' ? 'Optimize for Cursor' : 'Optimize Prompt')
                }
              </button>
            </form>
          </div>
        </div>

        {/* Right Panel - Output */}
        <div className="right-panel">
          <div className="output-header">
            <h2 id="output-heading">{context === 'rephrase' ? 'Corrected Text' : context === 'cursor_code_optimizer' ? 'Cursor-Optimized Code Prompt' : 'Optimized Prompt'}</h2>
          </div>
          
          {isLoading ? (
            <div className="prompt-output" role="status" aria-live="polite" aria-label="Processing your request">
              <div className="skeleton" style={{ width: '55%' }}></div>
              <div className="skeleton" style={{ width: '85%', marginTop: 12 }}></div>
              <div className="skeleton" style={{ width: '75%', marginTop: 12 }}></div>
            </div>
          ) : latestMessage && latestMessage.type === 'assistant' && !latestMessage.isError ? (
            <div className="prompt-output" role="region" aria-labelledby="output-heading">
              <button 
                className="copy-button" 
                onClick={() => copyToClipboard(latestMessage.optimized, 'top')}
                aria-label={context === 'rephrase' ? 'Copy corrected text' : context === 'cursor_code_optimizer' ? 'Copy Cursor-optimized code prompt' : 'Copy optimized prompt'}
                title={context === 'rephrase' ? 'Copy corrected text' : context === 'cursor_code_optimizer' ? 'Copy Cursor-optimized code prompt' : 'Copy optimized prompt'}
              >
                📋
              </button>
              
              <div className="prompt-sections">
                <div className="prompt-section-display" role="region" aria-labelledby="original-section">
                  <div className="section-header">
                    <div className="section-icon" aria-hidden="true">📝</div>
                    <h3 id="original-section">{context === 'rephrase' ? 'Original Text' : context === 'cursor_code_optimizer' ? 'Original Code Request' : 'Original Prompt'}</h3>
                  </div>
                  <div className="section-content">
                    <p>{latestMessage.original}</p>
                  </div>
                </div>

                <div className="prompt-section-display" role="region" aria-labelledby="strategy-section">
                  <div className="section-header">
                    <div className="section-icon" aria-hidden="true">🎯</div>
                    <h3 id="strategy-section">{context === 'rephrase' ? 'Correction Strategy' : context === 'cursor_code_optimizer' ? 'Cursor Optimization Strategy' : 'Strategy Applied'}</h3>
                  </div>
                  <div className="section-content">
                    <p>{latestMessage.strategy}</p>
                  </div>
                </div>

                <div className="prompt-section-display" role="region" aria-labelledby="optimized-section">
                  <div className="section-header">
                    <div className="section-icon" aria-hidden="true">✨</div>
                    <h3 id="optimized-section">{context === 'rephrase' ? 'Corrected Text' : context === 'cursor_code_optimizer' ? 'Cursor-Optimized Prompt' : 'Optimized Prompt'}</h3>
                  </div>
                  <div className="section-content">
                    <p>{latestMessage.optimized}</p>
                  </div>
                </div>
              </div>
              
              <div className="action-buttons">
                <button 
                  className="copy-btn" 
                  onClick={() => copyToClipboard(latestMessage.optimized, 'main')}
                  aria-label={context === 'rephrase' ? 'Copy corrected text to clipboard' : context === 'cursor_code_optimizer' ? 'Copy Cursor-optimized prompt to clipboard' : 'Copy optimized prompt to clipboard'}
                >
                  <span className="btn-icon" aria-hidden="true">📋</span>
                  {context === 'rephrase' ? 'Copy Corrected Text' : context === 'cursor_code_optimizer' ? 'Copy Cursor Prompt' : 'Copy Optimized'}
                </button>
                <button className="save-btn" aria-label="Save optimized prompt to library">
                  <span className="btn-icon" aria-hidden="true">⭐</span>
                  Save to library
                </button>
              </div>
              
              <div className="re-optimize">
                <button 
                  className="re-optimize-btn"
                  onClick={() => {
                    setInputValue('');
                    setMessages([]);
                  }}
                  aria-label="Start a new optimization"
                >
                  Re-optimize &gt;
                </button>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">✨</div>
              <h3>
                {context === 'rephrase' ? 'No text corrected yet' : context === 'cursor_code_optimizer' ? 'No code prompt optimized yet' : 'No prompt optimized yet'}
              </h3>
              <p>
                {context === 'rephrase' 
                  ? 'Enter text on the left to see the corrections here.' 
                  : context === 'cursor_code_optimizer'
                  ? 'Enter your code request on the left to see the Cursor-optimized prompt here.'
                  : 'Enter a prompt on the left to see the optimization here. Learn more on our About page or view plans on Pricing.'
                }
              </p>
              <div className="examples-bar">
                {[
                  'Role: Assistant • Task: Summarize this article',
                  'Create 5 marketing headlines for eco-friendly bottles',
                  'Rephrase this email in professional tone',
                  'Write a product spec for a TODO app'
                ].map((ex, i) => (
                  <button key={i} className="example-chip" onClick={() => setInputValue(ex)}>{ex}</button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
    </>
  );
};

export default Home;
