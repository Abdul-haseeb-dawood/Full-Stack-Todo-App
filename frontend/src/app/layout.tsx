'use client';

import { TaskProvider } from '@/contexts/TaskContext';
import { LanguageProvider } from '@/contexts/LanguageContext';
import { AuthProvider } from '@/contexts/AuthContext';
import '@/../styles/globals.css';

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
              {children}
            </LanguageProvider>
          </TaskProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
