'use client';

import { TaskProvider } from '@/contexts/TaskContext';
import { LanguageProvider } from '@/contexts/LanguageContext';
import { AuthProvider } from '@/contexts/AuthContext';
import { useAuth } from '@/contexts/AuthContext';
import { ChatWidget } from '@/components/ChatWidget';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import '@/../styles/globals.css';
import React from 'react';

// Component to conditionally render the chat widget only when authenticated
const ConditionalChatWidget = () => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return null;
  }

  return <ChatWidget />;
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <TaskProvider>
            <LanguageProvider>
              <LayoutContent>
                {children}
              </LayoutContent>
            </LanguageProvider>
          </TaskProvider>
        </AuthProvider>
      </body>
    </html>
  );
}

// Separate component to avoid using hooks directly in the layout
const LayoutContent = ({ children }: { children: React.ReactNode }) => {
  const pathname = usePathname();
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-xl font-bold text-indigo-600">
                TaskMaster AI
              </Link>
            </div>
            <nav className="flex items-center space-x-4">
              <Link
                href="/"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname === '/'
                    ? 'text-indigo-600 bg-indigo-100'
                    : 'text-gray-700 hover:text-indigo-600 hover:bg-gray-50'
                }`}
              >
                Tasks
              </Link>
              <Link
                href="/chat"
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  pathname === '/chat'
                    ? 'text-indigo-600 bg-indigo-100'
                    : 'text-gray-700 hover:text-indigo-600 hover:bg-gray-50'
                }`}
              >
                AI Assistant
              </Link>
              {user && (
                <span className="px-3 py-2 text-sm text-gray-600">
                  Welcome, {user.username || user.email}!
                </span>
              )}
            </nav>
          </div>
        </div>
      </header>

      <main>
        {children}
      </main>

      <ConditionalChatWidget />
    </div>
  );
};
