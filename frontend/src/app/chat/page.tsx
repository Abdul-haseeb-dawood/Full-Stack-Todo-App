'use client';

import React, { useState, useRef, useEffect } from 'react';
import ChatInterface from './ChatInterface';

const ChatPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100 p-4 sm:p-6 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-800">AI Task Assistant</h1>
          <p className="text-gray-600 mt-2">Chat with your AI assistant to manage your tasks</p>
        </header>
        
        <ChatInterface />
      </div>
    </div>
  );
};

export default ChatPage;