'use client';

import React from 'react';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import Dashboard from './page-content'; // We'll create this next

const HomePage = () => {
  return (
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  );
};

export default HomePage;