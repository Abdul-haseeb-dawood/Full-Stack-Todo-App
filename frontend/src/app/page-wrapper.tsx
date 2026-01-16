'use client';

import React from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import DashboardContent from './components/DashboardContent';

const HomePage = () => {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
};

export default HomePage;