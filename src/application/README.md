# Application Layer

This layer orchestrates the flow of data and implements use cases by coordinating domain objects.

## Structure

```
application/
├── usecases/         # Application use cases
├── ports/            # Input/Output ports (interfaces)
│   ├── input/        # Input ports (use case interfaces)
│   └── output/       # Output ports (repository interfaces)
├── services/         # Application services
├── commands/         # CQRS command handlers
├── queries/          # CQRS query handlers
└── events/           # Application event handlers
```

## Responsibilities

- Use case implementation
- Command and Query handling (CQRS)
- Application event handling
- Transaction management
- Input validation
- Output formatting
