'use client';

import { useState, useEffect } from 'react';
import { ChatContainer } from './chat/ChatContainer';
import { useChat } from '@/hooks/useChat';
import { ChatState } from '@/types/chat';

export const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [chatState, setChatState] = useState<ChatState>({
    currentConversation: {
      id: '',
      title: 'New Conversation',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
      isActive: true,
    },
    isLoading: false,
    inputValue: '',
    error: null,
    isConnected: false,
  });

  const { sendMessage, startNewConversation, connect, disconnect, isConnected } = useChat(setChatState);

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, []);

  return (
    <>
      {/* Floating chat button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-full shadow-lg hover:from-indigo-700 hover:to-purple-700 transition-all transform hover:scale-105"
        aria-label="Open chat"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </button>

      {/* Chat widget overlay */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-40 w-80 h-[500px] bg-white rounded-xl shadow-2xl overflow-hidden flex flex-col border border-gray-200">
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-3 flex justify-between items-center">
            <h2 className="font-semibold">Todo AI Assistant</h2>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>

          <div className="flex-1 overflow-hidden">
            <ChatContainer
              chatState={chatState}
              onSendMessage={sendMessage}
              onStartNewConversation={startNewConversation}
              onInputChange={(value) => setChatState(prev => ({...prev, inputValue: value}))}
              onErrorDismiss={() => setChatState(prev => ({...prev, error: null}))}
            />
          </div>
        </div>
      )}
    </>
  );
};