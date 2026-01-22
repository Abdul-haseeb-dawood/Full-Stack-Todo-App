import { ChatMessage } from '@/types/chat';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';

interface MessageBubbleProps {
  message: ChatMessage;
  isOwnMessage: boolean;
  onRetry?: (messageId: string) => void;
}

export const MessageBubble = ({ message, isOwnMessage, onRetry }: MessageBubbleProps) => {
  const isError = message.status === 'error';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isOwnMessage ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 ${
          isOwnMessage
            ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-br-none'
            : 'bg-white text-gray-800 rounded-bl-none border border-gray-200 shadow-sm'
        } ${isError ? 'bg-red-100 text-red-700 border-red-300' : ''}`}
      >
        <div className="whitespace-pre-wrap text-sm">
          {message.role === 'assistant' ? (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          ) : (
            message.content
          )}
        </div>
        <div className={`text-xs mt-1 ${isOwnMessage ? 'text-blue-100' : 'text-gray-500'} flex justify-end`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>

        {isError && onRetry && (
          <div className="mt-2">
            <button
              onClick={() => onRetry(message.id)}
              className="text-sm text-blue-500 hover:underline"
            >
              Retry
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
};