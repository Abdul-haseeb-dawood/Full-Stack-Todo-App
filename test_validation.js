// Test script to validate the chat functionality

// Test the chat API
async function testChatAPI() {
  try {
    console.log('Testing chat API...');

    const response = await fetch('http://localhost:3000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        conversation_id: null,
        message: 'Add a task to buy groceries',
        user_id: 'test-user'
      }),
    });

    const data = await response.json();
    console.log('Response:', data);

    if (data.response.includes('buy groceries')) {
      console.log('✅ Test passed: Add task functionality works');
    } else {
      console.log('❌ Test failed: Add task functionality not working as expected');
    }
  } catch (error) {
    console.error('❌ Error testing chat API:', error.message);
  }
}

// Test the task tools directly
async function testTaskTools() {
  try {
    console.log('\nTesting task tools...');

    // Import the tools
    const toolsModule = await import('./frontend/src/lib/tools/taskTools.js');
    const { addTaskTool } = toolsModule;

    // Test adding a task
    const result = await addTaskTool({
      title: 'Test task from validation script',
      priority: 'medium'
    });

    console.log('Add task result:', result);

    if (result.success) {
      console.log('✅ Test passed: Task tools are working');
    } else {
      console.log('❌ Test failed: Task tools not working');
    }
  } catch (error) {
    console.error('❌ Error testing task tools:', error.message);
  }
}

// Run tests
console.log('Starting validation tests...\n');
testChatAPI();
testTaskTools();