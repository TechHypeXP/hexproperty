# Event Infrastructure Layer

This layer handles event sourcing, event storage, and event processing across the application.

## Structure

```
events/
├── sourcing/         # Event sourcing implementation
│   ├── store/        # Event store
│   └── snapshots/    # Event snapshots
├── bus/              # Event bus implementation
│   ├── publishers/   # Event publishers
│   └── subscribers/  # Event subscribers
├── handlers/         # Event handlers
├── streams/          # Event streams
├── projections/      # Event projections
└── aggregates/       # Event aggregates
```

## Responsibilities

- Event sourcing
- Event storage
- Event processing
- Event streaming
- Event projections
- Event aggregation
- Event replay
