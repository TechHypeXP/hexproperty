/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebarsApi = {
  api: [
    {
      type: 'category',
      label: 'REST API',
      items: [
        'rest/overview',
        'rest/authentication',
        'rest/properties',
        'rest/tenants',
        'rest/leases',
        'rest/maintenance',
        'rest/payments',
        'rest/reports',
      ],
    },
    {
      type: 'category',
      label: 'GraphQL API',
      items: [
        'graphql/overview',
        'graphql/schema',
        'graphql/queries',
        'graphql/mutations',
        'graphql/subscriptions',
      ],
    },
    {
      type: 'category',
      label: 'gRPC API',
      items: [
        'grpc/overview',
        'grpc/services',
        'grpc/messages',
        'grpc/streaming',
      ],
    },
    {
      type: 'category',
      label: 'WebSocket API',
      items: [
        'websocket/overview',
        'websocket/events',
        'websocket/channels',
        'websocket/authentication',
      ],
    },
  ],
};

module.exports = sidebarsApi;
