# UI Specification — Phase II

## Pages

### Authentication Pages

#### Sign Up Page
- Email input field
- Password input field
- Submit button
- Link to sign in page
- Error messages for validation failures

#### Sign In Page
- Email input field
- Password input field
- Submit button
- Link to sign up page
- Error messages for invalid credentials

---

### Task Dashboard

#### Task List View
- Header with user info and sign out button
- Filter tabs (All / Active / Completed)
- List of task items showing:
  - Checkbox for completion toggle
  - Task title
  - Edit button
  - Delete button
- Visual indicator for completed tasks (strikethrough)

#### Add Task Form
- Input field for title (required)
- Textarea for description (optional)
- Add button
- Character limit indicator

#### Edit Task Modal/Inline
- Editable title field
- Editable description field
- Save button
- Cancel button

---

## Components

### TaskItem
- Props: `task`, `onToggle`, `onEdit`, `onDelete`
- Renders task with completion checkbox
- Shows title and description
- Edit and delete action buttons

### TaskForm
- Props: `onSubmit`, `initialData?`
- Title input (required)
- Description textarea (optional)
- Submit button

### AuthForm
- Props: `mode` (signin/signup), `onSubmit`
- Email input
- Password input
- Submit button
- Error display

---

## UI Requirements

### Responsive Design
- Mobile-first approach
- Breakpoints: 640px, 768px, 1024px
- Touch-friendly targets (44px minimum)

### Task Status Indicators
- Checkbox for incomplete tasks
- Strikethrough + dimmed for completed tasks
- Visual distinction between states

### Loading States
- Spinner during API calls
- Skeleton loader for task list
- Disable interactions while loading

### Error States
- Clear error messages
- Highlight invalid fields
- Retry action button

### Authentication Guard
- Redirect to sign in if no JWT
- No task content visible without auth
- Protected route handling

---

## User Flow

```
Unauthenticated:
  → / → Redirect to /signin
  → /signup → Sign Up form
  → /signin → Sign In form

Authenticated:
  → / → Task Dashboard
  → /signout → Clear token, redirect /signin
```

---

**Last Updated**: 2025-12-25
