/** @type {import('next').NextConfig} */
const nextConfig = {
  // Сборка в standalone-режиме нужна для компактного Docker-образа.
  output: "standalone",
  reactStrictMode: true,
};

module.exports = nextConfig;
