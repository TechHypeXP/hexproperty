import type { NextConfig } from 'next';
import type { Configuration as WebpackConfig } from 'webpack';

const config: NextConfig = {
  // Development server configuration
  webpackDevMiddleware: (config: WebpackConfig) => {
    // Solve hot-reloading issue
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    };
    return config;
  },
  // Disable compression for development
  compress: false,
  // Increase timeout
  experimental: {
    serverTimeout: 60000,
  },
  // Disable HTTPS for development
  server: {
    https: false,
  },
};

export default config;
