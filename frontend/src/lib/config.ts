// Configuration management for API endpoints and other environment-specific settings

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  TIMEOUT: 10000, // 10 seconds
  RETRY_ATTEMPTS: 3,
};

// Application Configuration
export const APP_CONFIG = {
  DEFAULT_LANGUAGE: process.env.NEXT_PUBLIC_DEFAULT_LANGUAGE || 'en',
  ENABLE_LOGGING: process.env.NODE_ENV !== 'production',
  MAX_TASK_TITLE_LENGTH: 200,
  MAX_TASK_DESCRIPTION_LENGTH: 1000,
};

// Feature Flags
export const FEATURE_FLAGS = {
  ENABLE_HISTORY: process.env.NEXT_PUBLIC_ENABLE_HISTORY !== 'false',
  ENABLE_LANGUAGE_TOGGLE: process.env.NEXT_PUBLIC_ENABLE_LANGUAGE_TOGGLE !== 'false',
  ENABLE_SEARCH: process.env.NEXT_PUBLIC_ENABLE_SEARCH !== 'false',
  ENABLE_FILTERS: process.env.NEXT_PUBLIC_ENABLE_FILTERS !== 'false',
  ENABLE_SORTING: process.env.NEXT_PUBLIC_ENABLE_SORTING !== 'false',
};

// Export all configurations
export default {
  API_CONFIG,
  APP_CONFIG,
  FEATURE_FLAGS,
};