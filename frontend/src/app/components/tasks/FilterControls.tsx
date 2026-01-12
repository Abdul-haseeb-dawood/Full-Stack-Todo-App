import React from 'react';
import { useTaskContext } from '@/contexts/TaskContext';
import { useLanguage } from '@/contexts/LanguageContext';

const FilterControls: React.FC = () => {
  const { state, dispatch } = useTaskContext();
  const { t } = useLanguage();

  const handleStatusChange = (status: 'completed' | 'incomplete' | '') => {
    const newFilter = { ...state.filter };
    if (status) {
      newFilter.status = status;
    } else {
      delete newFilter.status;
    }
    dispatch({ type: 'SET_FILTER', payload: newFilter });
  };

  const handlePriorityChange = (priority: 'high' | 'medium' | 'low' | '') => {
    const newFilter = { ...state.filter };
    if (priority) {
      newFilter.priority = priority;
    } else {
      delete newFilter.priority;
    }
    dispatch({ type: 'SET_FILTER', payload: newFilter });
  };

  return (
    <div className="flex flex-wrap gap-4 p-4 bg-white/30 backdrop-blur-sm rounded-xl">
      {/* Status Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">{t('task.filter')}</label>
        <div className="flex space-x-2">
          <button
            onClick={() => handleStatusChange('')}
            className={`px-3 py-1.5 text-sm rounded-full ${
              !state.filter.status
                ? 'bg-indigo-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            All
          </button>
          <button
            onClick={() => handleStatusChange('completed')}
            className={`px-3 py-1.5 text-sm rounded-full ${
              state.filter.status === 'completed'
                ? 'bg-emerald-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {t('task.completed')}
          </button>
          <button
            onClick={() => handleStatusChange('incomplete')}
            className={`px-3 py-1.5 text-sm rounded-full ${
              state.filter.status === 'incomplete'
                ? 'bg-amber-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Active
          </button>
        </div>
      </div>

      {/* Priority Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">{t('task.priority')}</label>
        <div className="flex space-x-2">
          <button
            onClick={() => handlePriorityChange('')}
            className={`px-3 py-1.5 text-sm rounded-full ${
              !state.filter.priority
                ? 'bg-indigo-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            All
          </button>
          <button
            onClick={() => handlePriorityChange('high')}
            className={`px-3 py-1.5 text-sm rounded-full ${
              state.filter.priority === 'high'
                ? 'bg-red-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {t('task.priority.high')}
          </button>
          <button
            onClick={() => handlePriorityChange('medium')}
            className={`px-3 py-1.5 text-sm rounded-full ${
              state.filter.priority === 'medium'
                ? 'bg-yellow-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {t('task.priority.medium')}
          </button>
          <button
            onClick={() => handlePriorityChange('low')}
            className={`px-3 py-1.5 text-sm rounded-full ${
              state.filter.priority === 'low'
                ? 'bg-green-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {t('task.priority.low')}
          </button>
        </div>
      </div>
    </div>
  );
};

export default FilterControls;