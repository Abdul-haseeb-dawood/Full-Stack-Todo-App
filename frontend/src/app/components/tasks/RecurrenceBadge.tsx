import React from 'react';
import { useLanguage } from '@/contexts/LanguageContext';

interface RecurrenceBadgeProps {
  recurrence: 'daily' | 'weekly' | 'monthly' | null;
}

const RecurrenceBadge: React.FC<RecurrenceBadgeProps> = ({ recurrence }) => {
  const { t } = useLanguage();

  if (!recurrence) return null;

  const getRecurrenceLabel = () => {
    switch (recurrence) {
      case 'daily':
        return t('task.recurrence.daily');
      case 'weekly':
        return t('task.recurrence.weekly');
      case 'monthly':
        return t('task.recurrence.monthly');
      default:
        return '';
    }
  };

  const getRecurrenceIcon = () => {
    switch (recurrence) {
      case 'daily':
        return '📅';
      case 'weekly':
        return '🗓️';
      case 'monthly':
        return '📅';
      default:
        return '';
    }
  };

  return (
    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
      <span className="mr-1">{getRecurrenceIcon()}</span>
      {getRecurrenceLabel()}
    </span>
  );
};

export default RecurrenceBadge;