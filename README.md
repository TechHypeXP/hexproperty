# HexProperty Frontend

A modern, responsive property management dashboard built with Next.js 14 and TypeScript.

## 🚀 Features

- **Modern Tech Stack**: Next.js 14, TypeScript, and React 18
- **Responsive Dashboard**: Beautiful and functional property management interface
- **Real-time Updates**: Live data synchronization using TanStack Query
- **Type-Safe**: End-to-end type safety with TypeScript and Zod
- **State Management**: Efficient state handling with Zustand
- **Beautiful UI**: Styled with Tailwind CSS and Framer Motion animations
- **Data Visualization**: Interactive charts using Chart.js
- **Docker Support**: Containerized development and production environments

## 🛠️ Getting Started

### Prerequisites

- Node.js 20.x or later
- Docker and Docker Compose
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hexproperty.git
   cd hexproperty
   ```

2. **Using Docker (Recommended)**
   ```bash
   # Start the development environment
   docker-compose up
   ```
   The application will be available at http://localhost:3000

3. **Local Development**
   ```bash
   # Install dependencies
   npm install

   # Start development server
   npm run dev
   ```

### Production Build

```bash
# Build the Docker image
docker build -t hexproperty .

# Run the container
docker run -p 3000:3000 hexproperty
```

## 📁 Project Structure

```
src/
├── components/          # React components
│   ├── atoms/          # Basic building blocks
│   ├── molecules/      # Composite components
│   ├── organisms/      # Complex components
│   └── templates/      # Page layouts
├── hooks/              # Custom React hooks
├── lib/               # Utility libraries
├── services/          # API services
├── stores/            # Zustand stores
├── styles/            # Global styles
├── types/             # TypeScript types
└── utils/             # Helper functions
```

## 🧪 Testing

```bash
# Run unit tests
npm test

# Run e2e tests
npm run test:e2e
```

## 📚 Documentation

- [Frontend Implementation Plan](docs/frontend/frontend-implementation-plan.md)
- [Technical Specification](docs/frontend/frontend-technical-specification.md)

## 🛡️ Security

- Type-safe implementation
- Runtime validation with Zod
- Secure development practices
- Regular dependency updates

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Next.js team for the amazing framework
- All contributors and maintainers
