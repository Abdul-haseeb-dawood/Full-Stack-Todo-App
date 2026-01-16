import React from 'react';
import { Task } from '@/models/task';
import GlassCard from '../ui/GlassCard';
import { useTaskContext } from '@/contexts/TaskContext';
import { useLanguage } from '@/contexts/LanguageContext';

interface TaskCardProps {
  task: Task;
}

const TaskCard: React.FC<TaskCardProps> = ({ task }) => {
  const { toggleTaskCompletion, openModal, deleteTask } = useTaskContext();
  const { t } = useLanguage();

  // Format the due date if it exists
  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  // Get priority color based on priority level
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'low':
        return 'bg-green-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <GlassCard
      className={`${task.completed ? 'opacity-60' : ''} hover:scale-105 hover:shadow-md transition-all duration-300 ease-in-out`}
    >
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleTaskCompletion(task.id)}
              className="h-5 w-5 rounded-full border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer opacity-0 absolute"
            />
            <div
              className={`w-5 h-5 rounded-full border-2 flex items-center justify-center cursor-pointer ${
                task.completed
                  ? 'bg-emerald-500 border-emerald-500'
                  : 'border-gray-300 hover:border-indigo-400'
              }`}
              onClick={() => toggleTaskCompletion(task.id)}
            >
              {task.completed && (
                <svg
                  className="w-3 h-3 text-white animate-checkmark"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path>
                </svg>
              )}
            </div>
          </div>
          <div>
            <h3 className={`font-semibold ${task.completed ? 'line-through' : ''}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`text-sm mt-1 ${task.completed ? 'line-through' : ''}`}>
                {task.description}
              </p>
            )}
          </div>
        </div>

        <div className="flex space-x-2">
          {/* Edit button */}
          <button
            onClick={() => openModal('edit', task.id)}
            className="text-gray-500 hover:text-indigo-600 transition-all duration-300 ease-in-out"
            aria-label={t('task.edit')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>

          {/* Delete button */}
          <button
            onClick={() => {
              if (window.confirm(t('task.confirmDelete'))) {
                deleteTask(task.id);
              }
            }}
            className="text-gray-500 hover:text-red-600 transition-all duration-300 ease-in-out"
            aria-label={t('task.delete')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>

          {/* Priority indicator */}
          <span className={`inline-block w-3 h-3 rounded-full ${getPriorityColor(task.priority || 'medium')}`}
                title={`${t('task.priority')} ${task.priority ? t(`task.priority.${task.priority}`) : 'N/A'}`}>
          </span>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {/* Tags */}
        {task.tags && task.tags.map((tag, index) => (
          <span
            key={index}
            className="px-2 py-1 text-xs rounded-full bg-indigo-100 text-indigo-800 transition-all duration-300 ease-in-out"
          >
            {tag}
          </span>
        ))}

        {/* Recurrence badge */}
        {task.recurrence && (
          <span className="px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800 transition-all duration-300 ease-in-out">
            {t(`task.recurrence.${task.recurrence}`)}
          </span>
        )}
      </div>

      {/* Due date */}
      {task.due_date && (
        <div className="mt-3 text-sm text-gray-600 transition-all duration-300 ease-in-out">
          <span className="font-medium">{t('task.dueDate')}:</span> {formatDate(task.due_date)}
        </div>
      )}
    </GlassCard>
  );
};

export default TaskCard;