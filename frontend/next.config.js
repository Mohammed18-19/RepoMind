/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,

  experimental: {
    serverActions: true
  },

  async rewrites() {
    return [
      {
        source: '/api/repomind/:path*',
        destination: 'http://localhost:5000/:path*'
      }
    ]
  },

  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'avatars.githubusercontent.com',
        port: '',
        pathname: '**'
      }
    ]
  }
}
