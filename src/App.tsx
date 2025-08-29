/**
 * Main App Component - TypeScript Version
 * 
 * This is the main application component that handles:
 * - Prompt optimization functionality
 * - User authentication (login/signup)
 * - Resizable panel interface
 * - Message management and display
 * - Copy to clipboard functionality
 * 
 * Features:
 * - Resizable panels with drag support
 * - Login/Signup modals
 * - Context-aware prompt optimization
 * - Touch support for mobile devices
 * - Type-safe implementation with TypeScript
 */

import React, { useState, useRef, useEffect } from 'react';
import axios, { AxiosResponse } from 'axios';
import './App.css';
import Login from './components/Login';
import Signup from './components/Signup';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================
/** Represents a user input message */
interface UserMessage {
  id: number;
  type: 'user';
  content: string;
  timestamp: string;
}

/** Represents a successful assistant response with optimization results */
interface AssistantMessage {
  id: number;
  type: 'assistant';
  original: string;
  strategy: string;
  optimized: string;
  timestamp: string;
  isError?: boolean;
}

/** Represents an error message from the assistant */
interface ErrorMessage {
  id: number;
  type: 'assistant';
  content: string;
  timestamp: string;
  isError: true;
}

/** Union type for all possible message types */
type Message = UserMessage | AssistantMessage | ErrorMessage;

/** Interface for copy feedback toast notifications */
interface CopyFeedback {
  show: boolean;
  message: string;
  type: 'success' | 'error' | '';
}

/** User object interface */
interface User {
  name: string;
  email: string;
}

/** Authentication modal mode */
type AuthMode = 'login' | 'signup';

/** Available context options for prompt optimization */
type Context = 'general' | 'business' | 'rephrase' | 'technical' | 'academic' | 'marketing' | 'image_generation' | 'video_generation';

/** Copy button types for different locations */
type ButtonType = 'top' | 'main';

/** API response structure from the optimization endpoint */
interface ApiResponse {
  original: string;
  strategy: string;
  optimized: string;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

const App: React.FC = () => {
  // ============================================================================
  // STATE MANAGEMENT
  // ============================================================================
  
  /** Array of all messages (user inputs and assistant responses) */
  const [messages, setMessages] = useState<Message[]>([]);
  
  /** Current user input value */
  const [inputValue, setInputValue] = useState<string>('');
  
  /** Loading state for API calls */
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  /** Selected context for prompt optimization */
  const [context, setContext] = useState<Context>('general');
  
  /** Copy feedback toast state */
  const [copyFeedback, setCopyFeedback] = useState<CopyFeedback>({ show: false, message: '', type: '' });
  
  /** User authentication state */
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  
  /** Authentication modal visibility */
  const [showAuthModal, setShowAuthModal] = useState<boolean>(false);
  
  /** Current authentication mode (login or signup) */
  const [authMode, setAuthMode] = useState<AuthMode>('login');
  
  /** Current user data */
  const [user, setUser] = useState<User | null>(null);
  
  /** Left panel width percentage for resizable panels */
  const [leftPanelWidth, setLeftPanelWidth] = useState<number>(50);
  
  /** Resizing state for panel drag operations */
  const [isResizing, setIsResizing] = useState<boolean>(false);
  
  /** Reference for auto-scrolling to bottom of messages */
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // ============================================================================
  // UTILITY FUNCTIONS
  // ============================================================================
  
  /** 
   * Scrolls to the bottom of the messages container
   * Used to show the latest message when new ones are added
   */
  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  /** 
   * Effect hook to auto-scroll to bottom when messages change
   */
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // ============================================================================
  // RESIZABLE PANELS FUNCTIONALITY
  // ============================================================================
  
  /**
   * Handles mouse down event on the resizable divider
   * Sets up mouse move and mouse up event listeners for panel resizing
   * @param e - React mouse event from the divider element
   */
  const handleMouseDown = (e: React.MouseEvent<HTMLDivElement>): void => {
    e.preventDefault();
    e.stopPropagation();
    setIsResizing(true);
    
    /**
     * Handles mouse movement during resize operation
     * Calculates new panel width based on mouse position
     * @param moveEvent - Native mouse event
     */
    const startResize = (moveEvent: MouseEvent): void => {
      // Get the app-container element for width calculations
      const container = document.querySelector('.app-container') as HTMLElement;
      if (!container) return;
      
      const rect = container.getBoundingClientRect();
      const mouseX = moveEvent.clientX - rect.left;
      const newLeftWidth = (mouseX / rect.width) * 100;
      
      // Limit the width between 20% and 80% to ensure both panels remain visible
      if (newLeftWidth >= 20 && newLeftWidth <= 80) {
        setLeftPanelWidth(newLeftWidth);
      }
    };
    
    /**
     * Handles mouse up event to stop resizing
     * Removes event listeners and resets resizing state
     */
    const stopResize = (): void => {
      setIsResizing(false);
      document.removeEventListener('mousemove', startResize);
      document.removeEventListener('mouseup', stopResize);
    };
    
    // Attach event listeners for mouse movement and release
    document.addEventListener('mousemove', startResize);
    document.addEventListener('mouseup', stopResize);
  };

  /**
   * Handles touch start event on the resizable divider for mobile devices
   * Sets up touch move and touch end event listeners for panel resizing
   * @param e - React touch event from the divider element
   */
  const handleTouchStart = (e: React.TouchEvent<HTMLDivElement>): void => {
    e.preventDefault();
    e.stopPropagation();
    setIsResizing(true);
    
    /**
     * Handles touch movement during resize operation on mobile
     * Calculates new panel width based on touch position
     * @param touchEvent - Native touch event
     */
    const startTouchResize = (touchEvent: TouchEvent): void => {
      touchEvent.preventDefault(); // Prevent scrolling while resizing
      
      const touch = touchEvent.touches[0];
      // Get the app-container element for width calculations
      const container = document.querySelector('.app-container') as HTMLElement;
      if (!container) return;
      
      const rect = container.getBoundingClientRect();
      const touchX = touch.clientX - rect.left;
      const newLeftWidth = (touchX / rect.width) * 100;
      
      // Limit the width between 20% and 80% to ensure both panels remain visible
      if (newLeftWidth >= 20 && newLeftWidth <= 80) {
        setLeftPanelWidth(newLeftWidth);
      }
    };
    
    /**
     * Handles touch end event to stop resizing
     * Removes event listeners and resets resizing state
     */
    const stopTouchResize = (): void => {
      setIsResizing(false);
      document.removeEventListener('touchmove', startTouchResize);
      document.removeEventListener('touchend', stopTouchResize);
    };
    
    // Attach event listeners for touch movement and release
    document.addEventListener('touchmove', startTouchResize, { passive: false });
    document.addEventListener('touchend', stopTouchResize);
  };

  // ============================================================================
  // AUTHENTICATION FUNCTIONALITY
  // ============================================================================
  
  /**
   * Handles login/logout button click in the navigation bar
   * If user is logged in, performs logout; otherwise shows login modal
   */
  const handleLoginLogout = (): void => {
    if (isLoggedIn) {
      // Logout: clear user data and login state
      setIsLoggedIn(false);
      setUser(null);
    } else {
      // Show login modal
      setAuthMode('login');
      setShowAuthModal(true);
    }
  };

  /**
   * Handles successful login from the Login component
   * Sets user data, login state, and closes the modal
   * @param userData - User information from login process
   */
  const handleLogin = (userData: User): void => {
    setUser(userData);
    setIsLoggedIn(true);
    setShowAuthModal(false);
    setAuthMode('login');
  };

  /**
   * Handles successful signup from the Signup component
   * Sets user data, login state, and closes the modal
   * @param userData - User information from signup process
   */
  const handleSignup = (userData: User): void => {
    setUser(userData);
    setIsLoggedIn(true);
    setShowAuthModal(false);
    setAuthMode('signup');
  };

  /**
   * Opens the authentication modal with specified mode
   * @param mode - Authentication mode ('login' or 'signup')
   */
  const openAuthModal = (mode: AuthMode = 'login'): void => {
    setAuthMode(mode);
    setShowAuthModal(true);
  };

  /**
   * Closes the authentication modal and resets to login mode
   */
  const closeAuthModal = (): void => {
    setShowAuthModal(false);
    setAuthMode('login');
  };

  /**
   * Switches between login and signup modes in the authentication modal
   */
  const switchAuthMode = (): void => {
    setAuthMode(authMode === 'login' ? 'signup' : 'login');
  };

  // ============================================================================
  // FORM HANDLING AND API CALLS
  // ============================================================================
  
  /**
   * Handles form submission for prompt optimization
   * Sends user input to the API and manages the response
   * @param e - Form submission event
   */
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    // Don't submit if input is empty or already loading
    if (!inputValue.trim() || isLoading) return;

    // Create user message object
    const userMessage: UserMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date().toLocaleTimeString()
    };

    // Add user message to conversation and start loading
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call the optimization API with user input and context
      const response: AxiosResponse<ApiResponse> = await axios.post('/api/optimize', {
        prompt: inputValue,
        context: context
      });

      // Create assistant message with optimization results
      const assistantMessage: AssistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        original: response.data.original,
        strategy: response.data.strategy,
        optimized: response.data.optimized,
        timestamp: new Date().toLocaleTimeString()
      };

      // Add assistant response to conversation
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error optimizing prompt:', error);
      
      // Create error message for display
      const errorMessage: ErrorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error while optimizing your prompt. Please try again.',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      
      // Add error message to conversation
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      // Always stop loading state
      setIsLoading(false);
    }
  };

  /**
   * Handles key press events in the textarea
   * Submits form when Enter is pressed (without Shift)
   * @param e - Keyboard event from textarea
   */
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      // Create a form event to match the handleSubmit signature
      const formEvent = {
        preventDefault: () => {},
        currentTarget: e.currentTarget.form
      } as React.FormEvent<HTMLFormElement>;
      handleSubmit(formEvent);
    }
  };

  // ============================================================================
  // CLIPBOARD FUNCTIONALITY
  // ============================================================================
  
  /**
   * Copies text to clipboard and shows feedback
   * Provides visual feedback on the specific button that was clicked
   * @param text - Text to copy to clipboard
   * @param buttonType - Type of button clicked ('top' or 'main')
   */
  const copyToClipboard = async (text: string, buttonType: ButtonType = 'main'): Promise<void> => {
    try {
      // Use modern clipboard API to copy text
      await navigator.clipboard.writeText(text);
      
      // Show success feedback toast
      setCopyFeedback({
        show: true,
        message: 'Copied to clipboard!',
        type: 'success'
      });

      // Add visual feedback to the specific button that was clicked
      if (buttonType === 'top') {
        const topButton = document.querySelector('.copy-button') as HTMLElement;
        if (topButton) {
          topButton.classList.add('copy-success');
          setTimeout(() => topButton.classList.remove('copy-success'), 1000);
        }
      } else if (buttonType === 'main') {
        const mainButton = document.querySelector('.copy-btn') as HTMLElement;
        if (mainButton) {
          mainButton.classList.add('copy-success');
          setTimeout(() => mainButton.classList.remove('copy-success'), 1000);
        }
      }

      // Hide feedback toast after 2 seconds
      setTimeout(() => {
        setCopyFeedback({ show: false, message: '', type: '' });
      }, 2000);

    } catch (err) {
      // Show error feedback if copy operation fails
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

  // ============================================================================
  // HELPER FUNCTIONS
  // ============================================================================
  
  /**
   * Gets the optimized prompt from the latest assistant message
   * Used for extracting the optimization result for display
   * @returns The optimized prompt text or null if no valid message exists
   */
  const getLatestOptimizedPrompt = (): string | null => {
    const lastMessage = messages[messages.length - 1];
    return lastMessage && lastMessage.type === 'assistant' && !lastMessage.isError 
      ? (lastMessage as AssistantMessage).optimized 
      : null;
  };

  /**
   * Gets the latest message from the conversation
   * @returns The most recent message or undefined if no messages exist
   */
  const getLatestMessage = (): Message | undefined => {
    return messages[messages.length - 1];
  };

  // Get the latest message for display purposes
  const latestMessage = getLatestMessage();

  // ============================================================================
  // COMPONENT RENDER
  // ============================================================================
  
  return (
    <div className="app">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-logo">
            <div className="logo-icon">⚡</div>
            <span className="logo-text">PromptPro</span>
          </div>
          
          <div className="nav-links">
            <a href="#" className="nav-link">Home</a>
            <a href="#" className="nav-link">Library</a>
            <a href="#" className="nav-link">Pricing</a>
            {isLoggedIn ? (
              <div className="user-section">
                <span className="user-name">Hi, {user?.name}</span>
                <button 
                  className="nav-button logout"
                  onClick={handleLoginLogout}
                >
                  Logout
                </button>
              </div>
            ) : (
              <button 
                className="nav-button login"
                onClick={handleLoginLogout}
              >
                Login
              </button>
            )}
          </div>
        </div>
      </nav>

      {/* Copy Feedback Toast */}
      {copyFeedback.show && (
        <div className={`copy-feedback ${copyFeedback.type}`}>
          <div className="feedback-icon">
            {copyFeedback.type === 'success' ? '✅' : '❌'}
          </div>
          <span className="feedback-message">{copyFeedback.message}</span>
        </div>
      )}

      <div className={`app-container ${isResizing ? 'resizing' : ''}`}>
        {/* Left Panel - Input */}
        <div className="left-panel" style={{ flex: `0 0 ${leftPanelWidth}%` }}>
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
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setInputValue(e.target.value)}
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
                  onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setContext(e.target.value as Context)}
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

        {/* Resizable Divider */}
        <div 
          className={`resizable-divider ${isResizing ? 'resizing' : ''}`}
          onMouseDown={handleMouseDown}
          onTouchStart={handleTouchStart}
        >
          <div className="divider-handle">
            <div className="handle-line"></div>
            <div className="handle-line"></div>
            <div className="handle-line"></div>
          </div>
        </div>

        {/* Right Panel - Output */}
        <div className="right-panel" style={{ flex: `0 0 ${100 - leftPanelWidth}%` }}>
          <div className="output-header">
            <h2>{context === 'rephrase' ? 'Corrected Text' : 'Optimized Prompt'}</h2>
          </div>
          
          {latestMessage && latestMessage.type === 'assistant' && !latestMessage.isError ? (
            <div className="prompt-output">
              <div 
                className="copy-button" 
                onClick={() => copyToClipboard((latestMessage as AssistantMessage).optimized, 'top')}
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
                    <p>{(latestMessage as AssistantMessage).original}</p>
                  </div>
                </div>

                {/* Section 2: Strategy Applied */}
                <div className="prompt-section-display">
                  <div className="section-header">
                    <div className="section-icon">🎯</div>
                    <h3>{context === 'rephrase' ? 'Correction Strategy' : 'Strategy Applied'}</h3>
                  </div>
                  <div className="section-content">
                    <p>{(latestMessage as AssistantMessage).strategy}</p>
                  </div>
                </div>

                {/* Section 3: Optimized Prompt */}
                <div className="prompt-section-display">
                  <div className="section-header">
                    <div className="section-icon">✨</div>
                    <h3>{context === 'rephrase' ? 'Corrected Text' : 'Optimized Prompt'}</h3>
                  </div>
                  <div className="section-content">
                    <p>{(latestMessage as AssistantMessage).optimized}</p>
                  </div>
                </div>
              </div>
              
              <div className="action-buttons">
                <button 
                  className="copy-btn" 
                  onClick={() => copyToClipboard((latestMessage as AssistantMessage).optimized, 'main')}
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

      {/* Authentication Modals */}
      {showAuthModal && (
        <>
          {authMode === 'login' ? (
            <Login
              onLogin={handleLogin}
              onSwitchToSignup={switchAuthMode}
              onClose={closeAuthModal}
            />
          ) : (
            <Signup
              onSignup={handleSignup}
              onSwitchToLogin={switchAuthMode}
              onClose={closeAuthModal}
            />
          )}
        </>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default App;
