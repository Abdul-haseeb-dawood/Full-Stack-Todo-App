// app/debug-api/page.tsx
'use client';

import { useState, useEffect } from 'react';

export default function DebugApiPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        console.log('Making request to:', process.env.NEXT_PUBLIC_API_BASE_URL || 'https://abdul-haseeb14-full-stack-todo.hf.space' + '/api/v1/tasks');
        const response = await fetch(process.env.NEXT_PUBLIC_API_BASE_URL + '/api/v1/tasks');
        console.log('Response status:', response.status);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>API Debug Page</h1>
      
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      
      {data && (
        <div>
          <p>Success! Retrieved {data.length} tasks</p>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}