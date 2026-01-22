import { useState, useCallback } from 'react';
import { ChatState, ChatMessage } from '@/types/chat';
import { chatApi } from '@/lib/api/chatClient';

export const useChat = (setChatState: (state: ChatState) => void) => {
  const [isConnected, setIsConnected] = useState(false);

  const connect = useCallback(() => {
    // Initialize connection to chat service
    setIsConnected(true);
    console.log('Connected to chat service');
  }, []);

  const disconnect = useCallback(() => {
    // Cleanup connection to chat service
    setIsConnected(false);
    console.log('Disconnected from chat service');
  }, []);

  const startNewConversation = useCallback(() => {
    setChatState((prev: ChatState) => {
      const newState: ChatState = {
        ...prev,
        currentConversation: {
          id: '',
          title: 'New Conversation',
          messages: [],
          createdAt: new Date(),
          updatedAt: new Date(),
          isActive: true,
        },
        inputValue: '',
        isLoading: false,
        error: null,
        isConnected: prev.isConnected
      };
      return newState;
    });
  }, [setChatState]);

  const sendMessage = useCallback(async (message: string) => {
    // Update UI to show loading state
    setChatState(prev => ({
      ...prev,
      isLoading: true,
      error: null
    }));

    try {
      // Add user message to UI immediately
      const userMessage: ChatMessage = {
        id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        role: 'user',
        content: message,
        timestamp: new Date(),
        status: 'sent'
      };

      // Update state and get the conversation ID
      let conversationId: string;
      setChatState(prev => {
        const newState = {
          ...prev,
          currentConversation: {
            ...prev.currentConversation,
            messages: [...prev.currentConversation.messages, userMessage],
            updatedAt: new Date()
          },
          inputValue: ''
        };
        conversationId = newState.currentConversation.id;
        return newState;
      });

      // Call API to get AI response
      const response = await chatApi.sendMessage(
        message,
        conversationId!
      );

      // Format the response content based on tool results
      let responseContent = response.response;

      // If there are tool results, format them appropriately
      if (response.tool_results && response.tool_results.length > 0) {
        const successfulResults = response.tool_results.filter(result => result.success);
        const failedResults = response.tool_results.filter(result => !result.success);

        if (successfulResults.length > 0) {
          responseContent += `\n\n${successfulResults.map(r => r.message).join('\n')}`;
        }

        if (failedResults.length > 0) {
          responseContent += `\n\n⚠️ Errors:\n${failedResults.map(r => `- ${r.message}`).join('\n')}`;
        }
      }

      // Add AI response to UI
      const aiMessage: ChatMessage = {
        id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        role: 'assistant',
        content: responseContent,
        timestamp: new Date(),
        status: 'sent'
      };

      setChatState(prev => ({
        ...prev,
        currentConversation: {
          ...prev.currentConversation,
          id: response.conversation_id,
          messages: [...prev.currentConversation.messages, aiMessage],
          updatedAt: new Date()
        },
        isLoading: false
      }));
    } catch (error) {
      console.error('Error sending message:', error);
      // Update the last message status to error
      setChatState(prev => {
        const updatedMessages = [...prev.currentConversation.messages];
        if (updatedMessages.length > 0) {
          const lastMessage = updatedMessages[updatedMessages.length - 1];
          lastMessage.status = 'error';
        }
        return {
          ...prev,
          currentConversation: {
            ...prev.currentConversation,
            messages: updatedMessages
          },
          error: 'Failed to send message. Please try again.',
          isLoading: false
        };
      });
    }
  }, [setChatState]);

  return {
    sendMessage,
    startNewConversation,
    connect,
    disconnect,
    isConnected
  };
};