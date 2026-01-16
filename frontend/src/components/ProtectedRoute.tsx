'use client';

import React from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect } from 'react';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Don't redirect if user is on signin or signup page
    if (!loading && !isAuthenticated && pathname !== '/signin' && pathname !== '/signup') {
      router.push('/signin');
    }
  }, [isAuthenticated, loading, router, pathname]);

  // Show nothing while checking authentication status
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-purple-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // If user is authenticated or on auth pages, render children
  if (isAuthenticated || pathname === '/signin' || pathname === '/signup') {
    return <>{children}</>;
  }

  // Don't render anything if not authenticated and not on auth pages
  return null;
};

export default ProtectedRoute;