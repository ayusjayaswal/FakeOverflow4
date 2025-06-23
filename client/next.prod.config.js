// next.prod.config.js
const basePath = '/tangerines';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  basePath,
  assetPrefix: basePath,
  trailingSlash: true,
  publicRuntimeConfig: {
    basePath,
  },
};

module.exports = nextConfig;
