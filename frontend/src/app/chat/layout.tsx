import React from 'react';
import Link from 'next/link';
import { ReactNode } from 'react';

interface ChatLayoutProps {
  children: ReactNode;
}

const ChatLayout = ({ children }: ChatLayoutProps) => {
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
                className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50"
              >
                Tasks
              </Link>
              <Link 
                href="/chat" 
                className="px-3 py-2 rounded-md text-sm font-medium text-indigo-600 bg-indigo-100"
              >
                AI Assistant
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main>
        {children}
      </main>
    </div>
  );
};

export default ChatLayout;