# HexProperty Project Structure Definition (PSD)

## Overview
This document defines the standardized project structure for HexProperty, ensuring consistent organization across all components and facilitating the implementation of our hexagonal architecture.

## Root Structure
```
hexproperty/
├── apps/                    # Application entry points
│   ├── web/                # Next.js web application
│   └── mobile/             # React Native mobile app
├── packages/               # Shared packages and domain logic
│   ├── core/              # Core domain logic
│   ├── ui/                # Shared UI components
│   └── utils/             # Shared utilities
├── libs/                  # External adapters and ports
│   ├── api/              # API adapters
│   ├── storage/          # Storage adapters
│   └── security/         # Security infrastructure
├── docs/                 # Project documentation
│   ├── architecture/    # Architecture documents
│   ├── business/       # Business process docs
│   └── implementation/ # Implementation guides
└── tools/              # Development and deployment tools
```

## Detailed Structure

### Web Application (`apps/web/`)
```
web/
├── src/
│   ├── pages/           # Next.js pages
│   ├── components/      # Web-specific components
│   ├── hooks/          # React hooks
│   ├── styles/         # CSS/SCSS files
│   └── utils/          # Web-specific utilities
├── public/             # Static assets
└── tests/             # Web app tests
```

### Mobile Application (`apps/mobile/`)
```
mobile/
├── src/
│   ├── screens/        # Mobile screens
│   ├── components/     # Mobile-specific components
│   ├── navigation/     # Navigation configuration
│   └── utils/         # Mobile-specific utilities
└── tests/            # Mobile app tests
```

### Core Package (`packages/core/`)
```
core/
├── src/
│   ├── domain/        # Domain models and logic
│   │   ├── models/    # Domain entities
│   │   ├── services/  # Domain services
│   │   └── events/    # Domain events
│   ├── application/   # Application services
│   │   ├── commands/  # Command handlers
│   │   ├── queries/   # Query handlers
│   │   └── services/  # Application services
│   └── ports/        # Port definitions
│       ├── primary/   # Primary ports (APIs)
│       └── secondary/ # Secondary ports (SPI)
└── tests/           # Core logic tests
```

### UI Package (`packages/ui/`)
```
ui/
├── src/
│   ├── components/    # Shared UI components
│   ├── hooks/        # Shared React hooks
│   ├── styles/       # Shared styles
│   └── utils/        # UI utilities
└── tests/           # UI component tests
```

### API Library (`libs/api/`)
```
api/
├── src/
│   ├── adapters/     # API adapters
│   ├── handlers/     # Request handlers
│   ├── middleware/   # API middleware
│   └── validation/   # Request validation
└── tests/          # API tests
```

### Storage Library (`libs/storage/`)
```
storage/
├── src/
│   ├── adapters/    # Storage adapters
│   ├── migrations/  # Database migrations
│   ├── models/     # Storage models
│   └── utils/      # Storage utilities
└── tests/         # Storage tests
```

### Security Library (`libs/security/`)
```
security/
├── src/
│   ├── auth/       # Authentication
│   ├── crypto/     # Cryptography
│   ├── policies/   # Security policies
│   └── utils/      # Security utilities
└── tests/        # Security tests
```

## Implementation Guidelines

### 1. Package Organization
- Each package must have its own `package.json` and clear dependencies
- Shared code must be placed in appropriate packages
- No circular dependencies between packages

### 2. Code Organization
- Follow domain-driven design principles
- Keep adapters separate from core logic
- Use clear and consistent naming conventions

### 3. Testing Structure
- Tests should mirror source code structure
- Integration tests should be separate from unit tests
- E2E tests should be in their own directory

### 4. Documentation Organization
- Architecture documents in `docs/architecture/`
- Business process documents in `docs/business/`
- Implementation guides in `docs/implementation/`

### 5. Development Workflow
- Feature branches should follow package structure
- PRs should maintain package independence
- CI/CD pipelines should respect package boundaries

## Version Control Guidelines

### 1. Repository Structure
- Monorepo approach using pnpm workspaces
- Shared configurations at root level
- Package-specific configurations in package roots

### 2. Branch Organization
- Main branches: `main`, `develop`
- Feature branches: `feature/package-name/feature-description`
- Release branches: `release/version`

### 3. Commit Organization
- Conventional commits
- Package-scoped commits
- Clear change descriptions

## Deployment Structure

### 1. Build Artifacts
```
dist/
├── apps/
│   ├── web/
│   └── mobile/
└── packages/
    ├── core/
    ├── ui/
    └── utils/
```

### 2. Environment Configuration
```
.env.development
.env.staging
.env.production
```

## Migration Guidelines

### 1. Code Migration
- Follow package boundaries
- Migrate core domain first
- Adapt existing code to new structure

### 2. Data Migration
- Version-controlled migrations
- Backward compatibility support
- Clear rollback procedures

## Conclusion
This structure supports our hexagonal architecture while maintaining clear boundaries between different concerns. It facilitates:
- Independent deployment of components
- Clear separation of concerns
- Easy testing and maintenance
- Scalable development workflow
