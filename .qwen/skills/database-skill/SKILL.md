---
name: database-skill
description: Design and manage databases including table creation, migrations, and schema design best practices.
---

# Database Skill

## Instructions

1. **Table Creation**
   - Design normalized database tables
   - Define proper primary and foreign keys
   - Use appropriate data types and constraints

2. **Schema Design**
   - Structure schemas for scalability and maintainability
   - Avoid redundant data
   - Model relationships clearly (one-to-one, one-to-many, many-to-many)

3. **Database Migrations**
   - Create versioned migrations for schema changes
   - Ensure migrations are reversible when possible
   - Apply migrations safely across environments

4. **Indexes & Performance**
   - Add indexes for frequently queried fields
   - Avoid unnecessary indexes
   - Optimize queries based on schema design

5. **Data Integrity**
   - Enforce constraints and validations at database level
   - Use transactions for critical operations
   - Handle cascading rules carefully

## Best Practices
- Keep schema changes backward-compatible
- Use naming conventions consistently
- Test migrations before production
- Separate migration logic from application logic
- Document schema decisions clearly

## Example Structure
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
