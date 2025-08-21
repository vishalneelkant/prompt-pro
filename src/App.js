import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [context, setContext] = useState('general');
  const [copyFeedback, setCopyFeedback] = useState({ show: false, message: '', type: '' });
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
      // Use relative path for Vercel and local
      const apiBase = process.env.REACT_APP_API_BASE_URL || window.location.origin;
      const response = await axios.post(`${apiBase}/api/optimize`, {
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
      
      // Show success feedback
      setCopyFeedback({
        show: true,
        message: 'Copied to clipboard!',
        type: 'success'
      });

      // Add visual feedback to the specific button
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

      // Hide feedback after 2 seconds
      setTimeout(() => {
        setCopyFeedback({ show: false, message: '', type: '' });
      }, 2000);

    } catch (err) {
      // Show error feedback
      setCopyFeedback({
        show: true,
        message: 'Failed to copy. Please try again.',
        type: 'error'
      });

      // Hide error feedback after 3 seconds
      setTimeout(() => {
        setCopyFeedback({ show: false, message: '', type: '' });
      }, 3000);
    }
  };

  const getLatestOptimizedPrompt = () => {
    const lastMessage = messages[messages.length - 1];
    return lastMessage && lastMessage.type === 'assistant' && !lastMessage.isError 
      ? lastMessage.optimized 
      : null;
  };

  const getLatestMessage = () => {
    return messages[messages.length - 1];
  };

  const latestMessage = getLatestMessage();
  const latestPrompt = getLatestOptimizedPrompt();

  return (
    <div className="app">
      {/* Copy Feedback Toast */}
      {copyFeedback.show && (
        <div className={`copy-feedback ${copyFeedback.type}`}>
          <div className="feedback-icon">
            {copyFeedback.type === 'success' ? '✅' : '❌'}
          </div>
          <span className="feedback-message">{copyFeedback.message}</span>
        </div>
      )}

      <div className="app-container">
        {/* Left Panel - Input */}
        <div className="left-panel">
          <div className="panel-header">
            <div className="logo">
              <div className="logo-icon">⚡</div>
              <span className="logo-text">PromptPro</span>
            </div>
          </div>
          
          <div className="input-section">
            <h1 className="main-title">
              {context === 'rephrase' 
                ? 'Turn messy text into polished, professional writing.' 
                : 'Turn messy prompts into powerful AI instructions.'
              }
            </h1>
            
            <form onSubmit={handleSubmit} className="input-form">
              <div className="input-group">
                <textarea
                  className="input-field"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={
                    context === 'rephrase' 
                      ? "e.g., i recieve ur messege and will definately respond"
                      : "e.g., Write a business plan for an AI startup in fintech."
                  }
                  disabled={isLoading}
                  rows={4}
                />
              </div>
              
              <div className="input-group">
                <select 
                  className="context-dropdown"
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                >
                  <option value="general">Select context</option>
                  <option value="business">Business</option>
                  <option value="rephrase">Rephrase & Grammar</option>
                  <option value="technical">Technical</option>
                  <option value="academic">Academic</option>
                  <option value="marketing">Marketing</option>
                  <option value="image_generation">Image Generation</option>
                  <option value="video_generation">Video Generation</option>
                </select>
              </div>
              
              <button
                type="submit"
                className="optimize-button"
                disabled={!inputValue.trim() || isLoading}
              >
                {isLoading 
                  ? (context === 'rephrase' ? 'Correcting...' : 'Optimizing...') 
                  : (context === 'rephrase' ? 'Correct Text' : 'Optimize Prompt')
                }
              </button>
            </form>
          </div>
        </div>

        {/* Right Panel - Output */}
        <div className="right-panel">
          <div className="output-header">
            <h2>{context === 'rephrase' ? 'Corrected Text' : 'Optimized Prompt'}</h2>
          </div>
          
          {latestMessage && latestMessage.type === 'assistant' && !latestMessage.isError ? (
            <div className="prompt-output">
              <div 
                className="copy-button" 
                onClick={() => copyToClipboard(latestMessage.optimized, 'top')}
                title={context === 'rephrase' ? 'Copy corrected text' : 'Copy optimized prompt'}
              >
                📋
              </div>
              
              {/* Three Sections Display */}
              <div className="prompt-sections">
                {/* Section 1: Original Prompt */}
                <div className="prompt-section-display">
                  <div className="section-header">
                    <div className="section-icon">📝</div>
                    <h3>{context === 'rephrase' ? 'Original Text' : 'Original Prompt'}</h3>
                  </div>
                  <div className="section-content">
                    <p>{latestMessage.original}</p>
                  </div>
                </div>

                {/* Section 2: Strategy Applied */}
                <div className="prompt-section-display">
                  <div className="section-header">
                    <div className="section-icon">🎯</div>
                    <h3>{context === 'rephrase' ? 'Correction Strategy' : 'Strategy Applied'}</h3>
                  </div>
                  <div className="section-content">
                    <p>{latestMessage.strategy}</p>
                  </div>
                </div>

                {/* Section 3: Optimized Prompt */}
                <div className="prompt-section-display">
                  <div className="section-header">
                    <div className="section-icon">✨</div>
                    <h3>{context === 'rephrase' ? 'Corrected Text' : 'Optimized Prompt'}</h3>
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
                >
                  <span className="btn-icon">📋</span>
                  {context === 'rephrase' ? 'Copy Corrected Text' : 'Copy Optimized'}
                </button>
                <button className="save-btn">
                  <span className="btn-icon">⭐</span>
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
                >
                  Re-optimize &gt;
                </button>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">✨</div>
              <h3>
                {context === 'rephrase' ? 'No text corrected yet' : 'No prompt optimized yet'}
              </h3>
              <p>
                {context === 'rephrase' 
                  ? 'Enter text on the left to see the corrections here.' 
                  : 'Enter a prompt on the left to see the optimization here.'
                }
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
