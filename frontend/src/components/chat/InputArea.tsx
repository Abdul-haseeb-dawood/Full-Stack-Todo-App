import { useState, useRef, KeyboardEvent } from 'react';

interface InputAreaProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (value: string) => void;
  disabled: boolean;
}

export const InputArea = ({ value, onChange, onSend, disabled }: InputAreaProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (value.trim() && !disabled) {
      onSend(value);
      onChange('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;

      // Update expanded state based on height
      setIsExpanded(textareaRef.current.scrollHeight > 100);
    }
  };

  // Adjust height when value changes
  if (textareaRef.current) {
    setTimeout(adjustTextareaHeight, 0);
  }

  return (
    <div className="relative flex-1">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask me to add, update, or manage your tasks..."
        disabled={disabled}
        className={`w-full resize-none rounded-lg border border-gray-200 px-3 py-2 pr-10 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-transparent bg-white shadow-sm text-sm ${
          isExpanded ? 'max-h-32' : 'max-h-16'
        }`}
      />
      <button
        onClick={handleSubmit}
        disabled={!value.trim() || disabled}
        className={`absolute right-2 bottom-2 rounded-full p-1.5 ${
          value.trim() && !disabled
            ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600'
            : 'bg-gray-200 text-gray-400 cursor-not-allowed'
        }`}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="h-3.5 w-3.5"
        >
          <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
        </svg>
      </button>
    </div>
  );
};