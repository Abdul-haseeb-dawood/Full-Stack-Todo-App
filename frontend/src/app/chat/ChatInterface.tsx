'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useTaskContext } from '@/contexts/TaskContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolCalls?: Array<{
    type: string;
    params: Record<string, any>;
  }>;
}

const ChatInterface = () => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { fetchTasks } = useTaskContext(); // Access task context to refresh tasks after operations

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Generate a user ID (in a real app, this would come from auth)
      const userId = 'default-user'; // For demo purposes

      // Prepare request payload
      const requestBody = {
        message: inputValue,
        user_id: userId,
        ...(conversationId && { conversation_id: conversationId }),
      };

      // Call the backend chat API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_BACKEND_URL}/api/chat/${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if this is a new conversation
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant message to the chat
      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        toolCalls: data.tool_calls || [],
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Refresh tasks if any tool calls were made
      if (data.tool_calls && data.tool_calls.length > 0) {
        fetchTasks(); // Refresh the task list after operations
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col h-[70vh]">
      {/* Chat Header */}
      <div className="bg-indigo-600 text-white p-4">
        <h2 className="text-xl font-semibold">AI Task Assistant</h2>
        <p className="text-indigo-200 text-sm">Ask me to add, list, complete, or update tasks</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
            <div className="mb-4 text-5xl">🤖</div>
            <h3 className="text-xl font-medium text-gray-800 mb-2">Welcome to your AI Task Assistant!</h3>
            <p className="max-w-md">I can help you manage your tasks. Try saying:</p>
            <ul className="mt-2 text-left list-disc list-inside max-w-md space-y-1">
              <li>"Add a task to buy groceries"</li>
              <li>"Show my pending tasks"</li>
              <li>"Complete task 1"</li>
              <li>"Update task 2 to 'Buy milk'"</li>
            </ul>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-xl p-4 ${
                  message.role === 'user'
                    ? 'bg-indigo-500 text-white rounded-br-none'
                    : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                {message.toolCalls && message.toolCalls.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-200 text-xs opacity-75">
                    <span>Used tools:</span>
                    <ul className="list-disc list-inside mt-1">
                      {message.toolCalls.map((toolCall, idx) => (
                        <li key={idx}>
                          {toolCall.type}({Object.entries(toolCall.params).map(([key, value]) => `${key}: ${value}`).join(', ')})
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'}`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="border-t border-gray-200 p-4 bg-white">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Message the AI assistant..."
            className="flex-1 border border-gray-300 rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="bg-indigo-600 text-white rounded-full px-6 py-3 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Sending...
              </span>
            ) : (
              'Send'
            )}
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500 text-center">
          Examples: "Add task: Buy groceries", "Show my tasks", "Complete task 1"
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;