/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro', 'quickstart', 'installation'],
    },
    {
      type: 'category',
      label: 'Architecture',
      items: [
        'architecture/overview',
        'architecture/folder-structure',
        'architecture/layers',
        'architecture/patterns',
        'architecture/security',
      ],
    },
    {
      type: 'category',
      label: 'Domain Layer',
      items: [
        'domain/entities',
        'domain/value-objects',
        'domain/aggregates',
        'domain/repositories',
        'domain/services',
      ],
    },
    {
      type: 'category',
      label: 'Application Layer',
      items: [
        'application/use-cases',
        'application/services',
        'application/dtos',
        'application/mappers',
      ],
    },
    {
      type: 'category',
      label: 'Infrastructure',
      items: [
        'infrastructure/persistence',
        'infrastructure/messaging',
        'infrastructure/caching',
        'infrastructure/logging',
      ],
    },
    {
      type: 'category',
      label: 'Interface Layer',
      items: [
        'interface/rest-api',
        'interface/graphql',
        'interface/websockets',
        'interface/grpc',
      ],
    },
    {
      type: 'category',
      label: 'Support Layer',
      items: [
        'support/monitoring',
        'support/logging',
        'support/tracing',
        'support/alerting',
      ],
    },
    {
      type: 'category',
      label: 'Service Mesh',
      items: [
        'service-mesh/overview',
        'service-mesh/routing',
        'service-mesh/security',
        'service-mesh/observability',
      ],
    },
    {
      type: 'category',
      label: 'Development',
      items: [
        'development/setup',
        'development/guidelines',
        'development/testing',
        'development/deployment',
      ],
    },
  ],
};

module.exports = sidebars;
