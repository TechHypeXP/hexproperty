# HexProperty Frontend Architecture

## Overview
HexProperty follows a layered architecture pattern with clear separation of concerns. The frontend is built using Next.js 14, TypeScript, and follows modern React patterns and best practices.

## Directory Structure

```
src/
├── app/                    # Next.js 14 App Router pages and layouts
├── components/            # Shared UI components (domain-agnostic)
│   ├── atoms/            # Basic building blocks (buttons, inputs, etc.)
│   ├── molecules/        # Combinations of atoms (form fields, cards, etc.)
│   └── organisms/        # Complex UI components (headers, sidebars, etc.)
├── features/             # Feature-specific components and logic
│   ├── properties/       # Property management feature
│   ├── tenants/         # Tenant management feature
│   └── dashboard/       # Dashboard feature
├── hooks/               # Custom React hooks
├── lib/                 # Utility functions and shared code
├── providers/          # React context providers
├── services/           # API and external service integrations
├── stores/             # Global state management (Zustand)
├── styles/             # Global styles and Tailwind configuration
├── types/              # TypeScript type definitions
└── utils/              # Helper functions and utilities

```

## Layer Definitions

### 1. Components Layer (`/components`)
- **Purpose**: Reusable, domain-agnostic UI components
- **Structure**:
  - `atoms/`: Basic UI elements (buttons, inputs, icons)
  - `molecules/`: Composite components (cards, dropdowns, form groups)
  - `organisms/`: Complex UI components (navigation bars, sidebars)

### 2. Features Layer (`/features`)
- **Purpose**: Domain-specific feature implementations
- **Structure**:
  - Feature-specific components
  - Feature-specific hooks
  - Feature-specific types
  - Feature-specific utilities

### 3. Application Layer (`/app`)
- **Purpose**: Next.js 14 App Router pages and layouts
- **Structure**:
  - Page components
  - Layout components
  - Route handlers
  - Loading and error states

### 4. Data Layer (`/services`, `/stores`)
- **Purpose**: Data fetching, state management, and API integration
- **Components**:
  - API services
  - Zustand stores
  - React Query configurations

### 5. Shared Layer (`/lib`, `/utils`, `/hooks`)
- **Purpose**: Shared utilities and functionality
- **Components**:
  - Custom hooks
  - Helper functions
  - Constants
  - Type utilities

## Component Organization

### Component Structure
Each component should follow this structure:
```typescript
/ComponentName
  ├── index.ts           # Export file
  ├── ComponentName.tsx  # Main component
  ├── ComponentName.test.tsx  # Tests
  └── types.ts          # Component-specific types
```

### Component Guidelines
1. **Single Responsibility**: Each component should do one thing well
2. **Props Interface**: Every component should have a defined props interface
3. **Type Safety**: Use TypeScript for all components and functions
4. **Testing**: Include unit tests for all components
5. **Documentation**: Include JSDoc comments for complex components

## State Management
- **Local State**: React's useState for component-level state
- **Global State**: Zustand for application-wide state
- **Server State**: React Query for API data management

## Styling
- **Framework**: Tailwind CSS
- **Organization**: 
  - Use utility classes for component-specific styling
  - Custom classes in global.css for shared styles
  - Theme configuration in tailwind.config.js

## Testing Strategy
- **Unit Tests**: Jest + React Testing Library
- **Component Tests**: Storybook (planned)
- **E2E Tests**: Cypress (planned)

## Best Practices
1. **Code Organization**:
   - Keep components small and focused
   - Use TypeScript for everything
   - Follow consistent naming conventions

2. **Performance**:
   - Implement code splitting
   - Use React.memo for expensive components
   - Optimize images and assets

3. **Accessibility**:
   - Follow WCAG guidelines
   - Include proper ARIA attributes
   - Ensure keyboard navigation

4. **Security**:
   - Validate all inputs
   - Sanitize data
   - Follow security best practices

## Development Workflow
1. Create feature branch
2. Implement changes following architecture guidelines
3. Write tests
4. Submit PR with detailed description
5. Code review
6. Merge to main branch

## Tools and Dependencies
- Next.js 14
- TypeScript
- Tailwind CSS
- React Query
- Zustand
- Jest
- React Testing Library
- ESLint
- Prettier

## Future Considerations
- Storybook integration
- Cypress E2E testing
- Automated accessibility testing
- Performance monitoring
- Error tracking integration
