import { useRef, useEffect } from 'react';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { WelcomeScreen } from './WelcomeScreen';
import { ChatState } from '@/types/chat';

interface ChatContainerProps {
  chatState: ChatState;
  onSendMessage: (message: string) => void;
  onStartNewConversation: () => void;
  onInputChange: (value: string) => void;
  onErrorDismiss: () => void;
}

export const ChatContainer = ({
  chatState,
  onSendMessage,
  onStartNewConversation,
  onInputChange,
  onErrorDismiss
}: ChatContainerProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatState.currentConversation.messages]);

  const handleRetry = (messageId: string) => {
    const messageToRetry = chatState.currentConversation.messages.find(msg => msg.id === messageId);
    if (messageToRetry && messageToRetry.role === 'user') {
      // Resend the user's message that failed
      onSendMessage(messageToRetry.content);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {chatState.error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded m-2 text-sm">
          <span className="font-bold">Error: </span>
          {chatState.error}
          <button
            className="ml-4 text-blue-500 hover:underline"
            onClick={onErrorDismiss}
          >
            Dismiss
          </button>
        </div>
      )}
      {chatState.currentConversation.messages.length === 0 ? (
        <WelcomeScreen onExamplePromptClick={onSendMessage} />
      ) : (
        <div className="flex-1 overflow-y-auto p-2 space-y-3">
          {chatState.currentConversation.messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              isOwnMessage={message.role === 'user'}
              onRetry={handleRetry}
            />
          ))}
          {chatState.isLoading && (
            <MessageBubble
              message={{
                id: 'loading',
                role: 'assistant',
                content: 'Thinking...',
                timestamp: new Date(),
                status: 'sent'
              }}
              isOwnMessage={false}
              onRetry={handleRetry}
            />
          )}
          <div ref={messagesEndRef} />
        </div>
      )}

      <div className="border-t border-gray-200 p-2 bg-white">
        <InputArea
          value={chatState.inputValue}
          onChange={onInputChange}
          onSend={onSendMessage}
          disabled={chatState.isLoading}
        />
      </div>
    </div>
  );
};