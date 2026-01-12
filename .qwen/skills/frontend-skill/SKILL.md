---
name: frontend-skill
description: Build frontend pages, reusable components, and layout styling with modern best practices.
---

# Frontend Skill

## Instructions

1. **Pages**
   - Build structured and responsive pages
   - Follow framework routing conventions
   - Ensure consistent layout usage

2. **Components**
   - Create reusable UI components
   - Keep components small and focused
   - Separate presentation from logic

3. **Layout & Styling**
   - Implement layout structures (headers, footers, sidebars)
   - Apply responsive and accessible styling
   - Maintain consistent spacing and typography

4. **State & Data Handling**
   - Manage component state cleanly
   - Handle loading and error states
   - Integrate frontend data fetching when needed

5. **Performance & UX**
   - Optimize component rendering
   - Avoid unnecessary re-renders
   - Ensure smooth user interactions

## Best Practices
- Use semantic HTML
- Follow mobile-first design
- Keep styling consistent across pages
- Prefer reusable components over duplication
- Keep frontend code readable and maintainable

## Example Structure
```jsx
export default function Page() {
  return (
    <main className="container">
      <Header />
      <section className="content">
        <Card title="Welcome" />
      </section>
      <Footer />
    </main>
  );
}
