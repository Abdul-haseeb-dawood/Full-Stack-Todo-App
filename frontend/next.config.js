/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'https://abdul-haseeb14-full-stack-todo.hf.space',
  },
};

module.exports = nextConfig;