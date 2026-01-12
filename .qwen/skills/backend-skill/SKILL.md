---
name: backend-skill
description: Build and manage backend logic including API routes, request/response handling, and database connectivity.
---

# Backend Skill

## Instructions

1. **API Routes**
   - Create RESTful API endpoints
   - Follow clear and consistent route naming
   - Separate routing logic from business logic

2. **Request Handling**
   - Validate incoming requests
   - Parse parameters, headers, and body safely
   - Handle edge cases and invalid inputs

3. **Response Handling**
   - Return structured and consistent responses
   - Use appropriate HTTP status codes
   - Handle and format errors clearly

4. **Database Connectivity**
   - Connect backend services to the database
   - Execute queries or ORM operations safely
   - Manage connections efficiently

5. **Error Handling**
   - Centralize error handling logic
   - Avoid leaking sensitive information
   - Log errors appropriately

## Best Practices
- Keep controllers thin and focused
- Use async/await for non-blocking operations
- Validate data at API boundaries
- Maintain clear separation of concerns
- Write reusable and maintainable backend code

## Example Structure
```js
// Route handler
app.post("/users", async (req, res) => {
  const { email } = req.body;

  const user = await db.user.create({ email });

  return res.status(201).json({
    success: true,
    data: user
  });
});
