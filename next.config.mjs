/** @type {import('next').NextConfig} */
const nextConfig = {
  // Development server configuration
  webpackDevMiddleware: config => {
    // Solve hot-reloading issue
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300
    }
    return config
  },
  // Disable compression for development
  compress: false,
  // Increase timeout
  experimental: {
    serverTimeout: 60000
  },
  // Disable HTTPS for development
  server: {
    https: false
  }
}

export default nextConfig
