import React from 'react';
import { useTaskContext } from '@/contexts/TaskContext';
import { useLanguage } from '@/contexts/LanguageContext';

const SortControls: React.FC = () => {
  const { state, dispatch } = useTaskContext();
  const { t } = useLanguage();

  const handleSortChange = (sort: 'due_date' | 'priority' | 'alphabetical') => {
    dispatch({ type: 'SET_SORT', payload: sort });
  };

  return (
    <div className="flex items-center space-x-2 p-4 bg-white/30 backdrop-blur-sm rounded-xl">
      <label className="text-sm font-medium text-gray-700">{t('task.sort')}:</label>
      <select
        value={state.sort}
        onChange={(e) => handleSortChange(e.target.value as 'due_date' | 'priority' | 'alphabetical')}
        className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
      >
        <option value="due_date">{t('task.dueDate')}</option>
        <option value="priority">{t('task.priority')}</option>
        <option value="alphabetical">{t('task.title')}</option>
      </select>
    </div>
  );
};

export default SortControls;