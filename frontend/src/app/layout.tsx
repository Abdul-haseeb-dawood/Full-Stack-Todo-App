'use client';

import { TaskProvider } from '@/contexts/TaskContext';
import { LanguageProvider } from '@/contexts/LanguageContext';
import '@/../styles/globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <TaskProvider>
          <LanguageProvider>
            {children}
          </LanguageProvider>
        </TaskProvider>
      </body>
    </html>
  );
}
