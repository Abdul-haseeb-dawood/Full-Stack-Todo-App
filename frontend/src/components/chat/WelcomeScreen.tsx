interface WelcomeScreenProps {
  onExamplePromptClick: (prompt: string) => void;
}

export const WelcomeScreen = ({ onExamplePromptClick }: WelcomeScreenProps) => {
  return (
    <div className="flex flex-col items-center justify-center h-full p-4">
      <div className="text-center">
        <div className="bg-gradient-to-r from-indigo-500 to-purple-500 p-3 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h2 className="text-xl font-bold text-gray-800 mb-2">Todo AI Assistant</h2>
        <p className="text-gray-600 text-sm">
          Interact with your todo list using natural language. Ask me to add, update, or find tasks.
        </p>
      </div>
    </div>
  );
};