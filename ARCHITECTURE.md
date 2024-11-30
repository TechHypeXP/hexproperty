# HexProperty Architecture

## Overview
HexProperty follows a combination of Hexagonal Architecture (Ports and Adapters) and the 8-layer model, providing a clear separation of concerns while maintaining flexibility and testability.

## Directory Structure

```
src/
├── domain/                  # Domain Layer (Core)
│   ├── models/             # Domain entities and value objects
│   ├── repositories/       # Repository interfaces
│   ├── services/          # Domain service interfaces
│   └── events/            # Domain events
├── application/           # Application Layer
│   ├── usecases/         # Use cases/application services
│   ├── dtos/             # Data Transfer Objects
│   └── ports/            # Port interfaces (in/out)
├── infrastructure/        # Infrastructure Layer
│   ├── persistence/      # Database implementations
│   ├── external/         # External service implementations
│   └── config/           # Infrastructure configuration
├── interface/            # Interface Layer (Adapters)
│   ├── api/              # API adapters (REST, GraphQL)
│   ├── web/              # Web interface components
│   │   ├── components/   # Reusable UI components
│   │   │   ├── atoms/    # Basic building blocks
│   │   │   ├── molecules/# Composite components
│   │   │   └── organisms/# Complex UI components
│   │   ├── features/     # Feature-specific components
│   │   │   ├── properties/
│   │   │   ├── tenants/
│   │   │   └── dashboard/
│   │   ├── layouts/     # Page layouts
│   │   └── pages/       # Next.js pages
│   └── mobile/          # Mobile interface (future)
├── support/             # Support Layer
│   ├── utils/          # Utility functions
│   ├── constants/      # Constants and enums
│   └── types/          # TypeScript types/interfaces
├── shared/             # Shared Layer
│   ├── hooks/          # Custom React hooks
│   ├── providers/      # Context providers
│   ├── stores/         # State management
│   └── lib/            # Shared libraries
├── presentation/        # Presentation Layer
│   ├── styles/         # Global styles and themes
│   ├── layouts/        # Layout components
│   └── theme/          # Theme configuration
└── enterprise/         # Enterprise Layer
    ├── policies/       # Enterprise-wide policies
    ├── rules/          # Cross-context rules
    └── shared/         # Shared business logic
```

## Layer Definitions

### 1. Presentation Layer (`/presentation`)
- UI/UX implementation
- Styling and theming
- Layout management
- Responsive design

### 2. Interface Layer (`/interface`)
- Component behavior
- Event handling
- Data presentation

### 3. Application Layer (`/application`)
- Use case orchestration
- Business process flows
- Application state management

### 4. Domain Layer (`/domain`)
- Business rules
- Domain entities
- Value objects

### 5. Infrastructure Layer (`/infrastructure`)
- External service integration
- Data persistence
- Technical capabilities

### 6. Enterprise Layer (`/enterprise`)
- Cross-context business rules
- Enterprise-wide policies
- Shared business logic

### 7. Support Layer (`/support`)
- Utilities and helpers
- Constants
- Cross-cutting concerns

### 8. Shared Layer (`/shared`)
- Common types
- Shared state
- Reusable components

## Core Architectural Patterns

### 1. Hexagonal Architecture (Ports & Adapters)

The core principle of our architecture is the Hexagonal (Ports & Adapters) pattern, which ensures:
- Business logic is isolated from external concerns
- Dependencies point inward
- External systems interact through well-defined ports

```
[External] → [Adapter] → [Port] → [Domain Core] → [Port] → [Adapter] → [External]
```

#### Ports (Interfaces)
- **Primary Ports**: Use cases that our domain exposes
  ```typescript
  interface PropertyManagementPort {
    listProperties(): Promise<Property[]>;
    addProperty(property: PropertyDTO): Promise<void>;
    updateProperty(id: string, property: PropertyDTO): Promise<void>;
  }
  ```

- **Secondary Ports**: Services our domain requires
  ```typescript
  interface PropertyRepository {
    findAll(): Promise<Property[]>;
    findById(id: string): Promise<Property>;
    save(property: Property): Promise<void>;
  }
  ```

#### Adapters
- **Primary Adapters**: Drive our application (UI, API routes)
  ```typescript
  // React component adapter
  const PropertyList: React.FC = () => {
    const propertyManagement = usePropertyManagement();
    // Uses primary port to interact with domain
  };
  ```

- **Secondary Adapters**: Driven by our application (DB, External Services)
  ```typescript
  class ApiPropertyRepository implements PropertyRepository {
    // Implements secondary port to provide infrastructure
  }
  ```

### 2. 8-Layer Model

Our architecture is organized into 8 distinct layers, each with specific responsibilities and constraints:

```
┌─────────────────────────────────────────────────────┐
│                  External World                      │
├─────────────────────────────────────────────────────┤
│ Presentation Layer                                  │
│  ├─ UI/UX Components                               │
│  ├─ Styling (Tailwind, CSS)                        │
│  └─ Layout Management                              │
├─────────────────────────────────────────────────────┤
│ Interface Layer                                     │
│  ├─ Web Components (React)                          │
│  ├─ API Routes                                      │
│  └─ External Interfaces                             │
├─────────────────────────────────────────────────────┤
│ Application Layer                                   │
│  ├─ Use Cases                                       │
│  ├─ Application Services                            │
│  └─ Orchestration                                   │
├─────────────────────────────────────────────────────┤
│ Domain Layer                                        │
│  ├─ Entities                                        │
│  ├─ Value Objects                                   │
│  ├─ Domain Services                                 │
│  └─ Domain Events                                   │
├─────────────────────────────────────────────────────┤
│ Infrastructure Layer                                │
│  ├─ Persistence                                     │
│  ├─ External Services                               │
│  └─ Technical Services                              │
├─────────────────────────────────────────────────────┤
│ Enterprise Layer                                    │
│  ├─ Cross-Context Business Rules                    │
│  ├─ Enterprise Policies                             │
│  └─ Shared Business Logic                          │
├─────────────────────────────────────────────────────┤
│ Support Layer                                       │
│  ├─ Utilities                                       │
│  ├─ Constants                                       │
│  └─ Cross-cutting Concerns                          │
├─────────────────────────────────────────────────────┤
│ Shared Layer                                        │
│  ├─ Common Types                                    │
│  ├─ Shared Libraries                                │
│  └─ State Management                                │
└─────────────────────────────────────────────────────┘
```

#### Layer Interactions

1. **Presentation → Interface**
   ```typescript
   // Theme configuration
   const theme = {
     colors: {
       primary: '#1a365d',
       secondary: '#2d3748',
     },
     typography: {
       heading: 'font-bold text-2xl',
       body: 'text-base leading-relaxed',
     },
   };

   // Layout component
   const DashboardLayout: React.FC = ({ children }) => {
     return (
       <div className="min-h-screen bg-gray-100">
         <Sidebar />
         <div className="ml-64 p-8">
           {children}
         </div>
       </div>
     );
   };
   ```

2. **Interface → Application**
   ```typescript
   // Component using application use case
   const PropertyForm: React.FC = () => {
     const addProperty = useAddPropertyUseCase();
     // Component logic
   };
   ```

3. **Application → Domain**
   ```typescript
   class AddPropertyUseCase {
     constructor(private propertyRepository: PropertyRepository) {}
     
     async execute(propertyData: PropertyDTO): Promise<void> {
       const property = Property.create(propertyData);
       await this.propertyRepository.save(property);
     }
   }
   ```

4. **Domain → Infrastructure**
   ```typescript
   class Property {
     private constructor(
       private readonly id: PropertyId,
       private details: PropertyDetails
     ) {}

     static create(data: PropertyDTO): Property {
       // Domain logic for creating a property
     }
   }
   ```

### 3. Integration with Domain-Driven Design

Our architecture combines Hexagonal Architecture and the 8-layer model with DDD principles:

```
┌─────────────────────────────────────────────────────┐
│                 Bounded Contexts                     │
├─────────────────────────────────────────────────────┤
│ Property Management │ Tenant Management │ Financial  │
│    ┌──────────┐    │    ┌──────────┐   │ Operations│
│    │ Hexagonal│    │    │ Hexagonal│   │   ...     │
│    │   Arch   │    │    │   Arch   │   │          │
│    └──────────┘    │    └──────────┘   │          │
└─────────────────────────────────────────────────────┘
```

#### Example: Property Management Bounded Context

1. **Domain Model**
   ```typescript
   // Domain Entity
   class Property {
     private constructor(
       private readonly id: PropertyId,
       private details: PropertyDetails,
       private status: PropertyStatus
     ) {}

     // Rich domain behavior
     markAsAvailable(): void {
       if (!this.canBeMarkedAvailable()) {
         throw new PropertyNotAvailableError();
       }
       this.status = PropertyStatus.Available;
       this.addDomainEvent(new PropertyBecameAvailable(this.id));
     }
   }

   // Value Object
   class PropertyDetails {
     constructor(
       private readonly address: Address,
       private readonly features: PropertyFeatures
     ) {}
   }
   ```

2. **Application Layer**
   ```typescript
   // Use Case
   class ListAvailablePropertiesUseCase {
     constructor(private propertyRepository: PropertyRepository) {}

     async execute(): Promise<PropertyDTO[]> {
       const properties = await this.propertyRepository.findAvailable();
       return properties.map(p => PropertyMapper.toDTO(p));
     }
   }
   ```

3. **Interface Layer**
   ```typescript
   // React Component (Primary Adapter)
   const AvailableProperties: React.FC = () => {
     const listProperties = useListAvailablePropertiesUseCase();
     // Component logic using the use case
   };
   ```

4. **Infrastructure Layer**
   ```typescript
   // Repository Implementation (Secondary Adapter)
   class ApiPropertyRepository implements PropertyRepository {
     async findAvailable(): Promise<Property[]> {
       const response = await api.get('/properties?status=available');
       return response.data.map(PropertyMapper.toDomain);
     }
   }
   ```

## Directory Structure Implementation

Our codebase follows this structure to implement the architecture:

```
src/
├── presentation/           # Presentation Layer
│   ├── styles/            # Global styles and themes
│   ├── layouts/           # Layout components
│   └── theme/             # Theme configuration
├── interface/             # Interface Layer
│   └── web/
│       ├── components/    # React Components
│       │   ├── atoms/
│       │   ├── molecules/
│       │   └── organisms/
│       └── features/      # Feature Components
├── application/           # Application Layer
│   ├── usecases/         # Application Use Cases
│   ├── dtos/             # Data Transfer Objects
│   └── ports/            # Port Interfaces
├── domain/               # Domain Layer
│   ├── models/           # Entities & Value Objects
│   ├── repositories/     # Repository Interfaces
│   ├── services/         # Domain Services
│   └── events/           # Domain Events
├── infrastructure/       # Infrastructure Layer
│   ├── persistence/      # Repository Implementations
│   ├── external/         # External Service Adapters
│   └── config/           # Configuration
├── enterprise/          # Enterprise Layer
│   ├── policies/        # Enterprise-wide policies
│   ├── rules/           # Cross-context rules
│   └── shared/          # Shared business logic
├── support/             # Support Layer
│   ├── utils/           # Utilities
│   ├── constants/       # Constants
│   └── types/           # TypeScript Types
└── shared/             # Shared Layer
    ├── hooks/           # React Hooks
    ├── providers/       # Context Providers
    ├── stores/          # State Management
    └── lib/             # Shared Libraries
```

## Key Principles

1. **Clean Architecture**
   - Dependencies point inward
   - Domain layer has no external dependencies
   - Outer layers depend on inner layers

2. **Hexagonal Architecture**
   - Clear ports and adapters
   - Domain core isolation
   - Pluggable external interfaces

3. **8-Layer Model**
   - Clear separation of concerns
   - Organized dependencies
   - Maintainable structure

4. **Domain-Driven Design**
   - Rich domain model
   - Bounded contexts
   - Ubiquitous language

## Implementation Guidelines

1. **Dependencies**
   - Inner layers must not depend on outer layers
   - Use dependency injection
   - Define clear interfaces

2. **Testing**
   - Domain logic highly testable
   - Mock external dependencies
   - Integration tests for adapters

3. **State Management**
   - Domain state in entities
   - UI state in stores
   - Clear state boundaries

4. **Data Flow**
   - Unidirectional data flow
   - Clear input/output ports
   - Consistent DTOs

## Best Practices

1. **Code Organization**
   - Follow layer responsibilities
   - Clear module boundaries
   - Consistent naming

2. **Component Design**
   - Single responsibility
   - Composition over inheritance
   - Props interface definition

3. **Testing Strategy**
   - Unit tests for domain
   - Integration tests for adapters
   - E2E tests for features

4. **Performance**
   - Lazy loading
   - Code splitting
   - Optimized builds

## Migration Plan

1. **Phase 1: Core Structure**
   - Set up layer directories
   - Define key interfaces
   - Establish boundaries

2. **Phase 2: Domain Model**
   - Implement core entities
   - Define repositories
   - Create services

3. **Phase 3: Interface Layer**
   - Migrate UI components
   - Implement adapters
   - Set up API endpoints

4. **Phase 4: Infrastructure**
   - Implement persistence
   - Set up external services
   - Configure systems

## Development Workflow

1. Start with domain model design
2. Implement use cases in application layer
3. Create necessary infrastructure adapters
4. Build UI components following Atomic Design
5. Integrate all layers ensuring proper separation

## Testing Strategy

### 1. Domain Layer
- Unit tests for entities and value objects
- Unit tests for domain services
- Event testing for domain events

### 2. Application Layer
- Use case tests with mocked dependencies
- Integration tests for complex flows

### 3. Interface Layer
- Component unit tests
- Integration tests for complex components
- E2E tests for critical user journeys

## Best Practices

1. **Domain Focus**
   - Always start with domain model
   - Use ubiquitous language consistently
   - Keep domain logic pure

2. **Clean Architecture**
   - Maintain proper dependency direction
   - Use interfaces for layer communication
   - Keep concerns separated

3. **Component Design**
   - Follow Atomic Design principles
   - Keep components focused
   - Implement proper prop typing

4. **Testing**
   - Test domain logic thoroughly
   - Implement integration tests
   - Use E2E tests for critical paths
