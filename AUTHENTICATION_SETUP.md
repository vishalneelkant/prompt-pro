# Authentication System Setup Guide

## Overview
This project now includes a complete user authentication system with login, signup, and logout functionality.

## Features
- ✅ User registration with name, email, and password
- ✅ User login with email and password
- ✅ Secure password hashing using bcrypt
- ✅ JWT token-based authentication
- ✅ User session management
- ✅ Protected routes and endpoints
- ✅ Responsive authentication modals
- ✅ Form validation and error handling
- ✅ Anonymous user request limiting (3 free optimizations)
- ✅ Automatic login prompts when limit is reached

## Backend Setup

### 1. Install Dependencies
```bash
cd api
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the `api/` directory with the following variables:

```env
# Database Configuration
DATABASE_URL=sqlite:///prompt_optimizer.db

# Security
SECRET_KEY=your-super-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment-here
```

### 3. Database Setup
The system will automatically create the necessary database tables when you start the Flask application.

### 4. Start the Backend
```bash
cd api
python optimize.py
```

## Frontend Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Start the Frontend
```bash
npm start
```

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/signup
- **Purpose**: User registration
- **Body**: `{ "name": "string", "email": "string", "password": "string" }`
- **Response**: `{ "message": "string", "user": "object", "token": "string" }`

#### POST /api/auth/login
- **Purpose**: User login
- **Body**: `{ "email": "string", "password": "string" }`
- **Response**: `{ "message": "string", "user": "object", "token": "string" }`

#### POST /api/auth/logout
- **Purpose**: User logout
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "string" }`

#### GET /api/auth/profile
- **Purpose**: Get current user profile
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "user": "object" }`

#### POST /api/auth/verify-token
- **Purpose**: Verify JWT token validity
- **Body**: `{ "token": "string" }`
- **Response**: `{ "valid": "boolean", "user": "object" }`

### Request Limiting Endpoints

#### GET /api/check-requests
- **Purpose**: Check remaining requests for current user
- **Response**: 
  - **Authenticated users**: `{ "is_authenticated": true, "unlimited": true, "message": "string" }`
  - **Anonymous users**: `{ "is_authenticated": false, "unlimited": false, "remaining_requests": number, "total_limit": number, "message": "string" }`

## Anonymous User Request Limiting

### Overview
The system implements a freemium model where anonymous users can make up to 3 prompt optimizations before being required to login.

### Features
- **3 Free Optimizations**: Anonymous users get 3 free prompt optimizations
- **Hidden Counter**: Request counting happens in the background without visible banners
- **Automatic Login Prompt**: Login modal appears automatically after 3rd request
- **Seamless Experience**: Users can use the service without interruption until limit is reached
- **Session Persistence**: Request count persists across browser sessions

### User Experience
1. **First Visit**: User can use the service normally without any visible counters
2. **After First Use**: No visible indication, counter runs in background
3. **After Second Use**: No visible indication, counter runs in background
4. **After Third Use**: Login modal appears automatically after 1 second
5. **Login Required**: User must login to continue using the service

### Implementation Details
- Request counting is session-based using Flask sessions
- Anonymous user IDs are generated using UUID
- Request limits are enforced at the API level
- No visible banners or counters shown to users
- Login modal appears automatically when limit is reached
- Clean, distraction-free user experience

## Security Features

### Password Security
- Passwords are hashed using bcrypt
- Minimum password length: 6 characters
- Secure password storage in database

### JWT Authentication
- 24-hour token expiration
- Secure token generation and validation
- Automatic token verification on app startup

### Session Management
- Secure logout functionality
- Automatic token cleanup
- Protected API endpoints

## User Experience Features

### Form Validation
- Real-time error feedback
- Client-side validation
- Server-side validation
- User-friendly error messages

### Responsive Design
- Mobile-friendly authentication modals
- Smooth animations and transitions
- Consistent styling with the main application

### State Management
- Persistent user sessions
- Automatic token verification
- Seamless login/logout transitions

## Usage

### For Users
1. **Sign Up**: Click "Login" → "Sign up" to create a new account
2. **Login**: Use your email and password to sign in
3. **Logout**: Click the logout button in the navigation bar

### For Developers
- All authentication state is managed in the main App component
- Authentication modals are conditionally rendered
- User data is stored in localStorage for persistence
- Axios interceptors automatically include auth tokens

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure the database URL is correct in your `.env` file
   - Check that all required packages are installed

2. **Authentication Token Issues**
   - Clear localStorage and try logging in again
   - Check that the JWT_SECRET_KEY is set correctly

3. **CORS Issues**
   - Ensure the Flask-CORS extension is properly configured
   - Check that the frontend is making requests to the correct backend URL

### Debug Mode
Enable debug logging by setting the Flask environment:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

## Security Considerations

### Production Deployment
- Change all default secret keys
- Use HTTPS in production
- Implement rate limiting
- Add password complexity requirements
- Consider adding two-factor authentication

### Database Security
- Use environment variables for sensitive data
- Implement database connection pooling
- Regular security updates and patches

## Future Enhancements

- Password reset functionality
- Email verification
- Social media authentication
- Role-based access control
- Audit logging
- Multi-factor authentication
