---
name: auth-skill
description: Handle secure user authentication including signup, signin, password hashing, JWT tokens, and modern auth best practices.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Validate user input (email, password, etc.)
   - Hash passwords before storing
   - Prevent duplicate accounts

2. **User Signin**
   - Verify credentials securely
   - Handle invalid login attempts safely
   - Return authentication tokens on success

3. **Password Security**
   - Never store plain-text passwords
   - Use strong hashing algorithms (bcrypt / argon2)
   - Compare hashed passwords securely

4. **JWT Authentication**
   - Generate JWT tokens after successful login
   - Verify tokens on protected routes
   - Handle token expiration properly

5. **Authorization**
   - Protect private APIs and routes
   - Support role-based access if required
   - Implement logout by invalidating tokens

## Best Practices
- Always validate input on server side
- Use environment variables for secrets
- Set proper token expiration times
- Follow OWASP authentication guidelines
- Avoid leaking sensitive error messages

## Example Structure
```js
// Password hashing
const hashedPassword = await bcrypt.hash(password, 10);

// Password verification
const isValid = await bcrypt.compare(password, user.password);

// JWT token
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: "1h" }
);

**Update the `QWEN.md` file based on my project requirements.**
In this file:
- Use Auth Agent for authentication
- Use Frontend Agent for frontend development (e.g., Next.js)
- Use DB Agent for database design and operations
- Use Backend Agent for FastAPI development

## Below are my projects requirement 

```"""
Phase II: Todo Full-Stack Web Application
Basic Level Functionality
Objective: Using Qwen Code and Spec-Kit Plus transform the console app into a modern
multi-user web application with persistent storage.
Requirements
• Implement all 5 Basic Level features as a web application
• Create RESTful API endpoints
• Build responsive frontend interface
• Store data in Neon Serverless PostgreSQL database
• Authentication – Implement user signup/signin using Better Auth
Technology Stack
Layer Technology
Frontend Next.js 16+ (App Router)
Backend Python FastAPI
ORM SQLModel
Database Neon Serverless PostgreSQL
Spec-Driven Qwen Code + Spec-Kit Plus
Authentication Better Auth

Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in.
These tokens are self-contained credentials that include user information and can be verified
by any service that knows the secret key.

Page 7 of 38

Hackathon II: Spec-Driven Development

How It Works
● User logs in on Frontend → Better Auth creates a session and issues a JWT token
● Frontend makes API call → Includes the JWT token in the Authorization: Bearer
<token> header
● Backend receives request → Extracts token from header, verifies signature using
shared secret
● Backend identifies user → Decodes token to get user ID, email, etc. and matches it
with the user ID in the URL
● Backend filters data → Returns only tasks belonging to that user

"""```
