'use client';

import { useState, useEffect } from 'react';

export default function DebugInfoPage() {
  const [apiUrl, setApiUrl] = useState('');
  const [browserInfo, setBrowserInfo] = useState('');

  // Get the API URL from environment variables
  useEffect(() => {
    // Log the API URL being used
    const url = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://abdul-haseeb14-full-stack-todo.hf.space';
    setApiUrl(url);

    // Log browser info
    setBrowserInfo(`
      User Agent: ${navigator.userAgent}
      Platform: ${navigator.platform}
      Host: ${window.location.host}
      Protocol: ${window.location.protocol}
    `);

    console.log('API URL being used:', url);
    console.log('Current window location:', window.location.href);
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>Debug Information</h1>

      <h2>Environment Variables:</h2>
      <p><strong>NEXT_PUBLIC_API_BASE_URL:</strong> {process.env.NEXT_PUBLIC_API_BASE_URL || '(not set or not accessible)'}</p>

      <h2>Derived API URL:</h2>
      <p>{apiUrl}</p>

      <h2>Browser Info:</h2>
      <pre>{browserInfo}</pre>

      <h2>Test API Connection:</h2>
      <button
        onClick={async () => {
          try {
            console.log('Making request to:', `${apiUrl}/health`);
            const response = await fetch(`${apiUrl}/health`);
            console.log('Health check response:', response.status, await response.text());
            alert(`Health check: ${response.status} - ${await response.text()}`);
          } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
          }
        }}
      >
        Test Health Endpoint
      </button>
    </div>
  );
}