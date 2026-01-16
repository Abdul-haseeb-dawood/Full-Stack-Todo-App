// Simple test to verify the API connection
const API_BASE_URL = 'https://abdul-haseeb14-full-stack-todo.hf.space';

async function testConnection() {
  try {
    console.log('Testing connection to:', `${API_BASE_URL}/health`);
    
    const response = await fetch(`${API_BASE_URL}/health`);
    console.log('Health check response status:', response.status);
    
    if (response.ok) {
      const data = await response.json();
      console.log('Health check response data:', data);
    } else {
      console.error('Health check failed:', response.status, response.statusText);
    }
    
    console.log('\nTesting tasks endpoint...');
    const tasksResponse = await fetch(`${API_BASE_URL}/api/v1/tasks`);
    console.log('Tasks endpoint response status:', tasksResponse.status);
    
    if (tasksResponse.ok) {
      const tasksData = await tasksResponse.json();
      console.log('Tasks endpoint response data length:', tasksData.length);
    } else {
      console.error('Tasks endpoint failed:', tasksResponse.status, tasksResponse.statusText);
    }
  } catch (error) {
    console.error('Network error:', error.message);
  }
}

testConnection();