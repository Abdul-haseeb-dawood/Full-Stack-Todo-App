import React, { useEffect, useState } from 'react';
import Modal from '../ui/Modal';
import TaskForm from './TaskForm';
import { TaskFormData } from '@/models/task';
import { useTaskContext } from '@/contexts/TaskContext';
import { useLanguage } from '@/contexts/LanguageContext';

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: 'add' | 'edit';
  taskId?: string;
}

const TaskModal: React.FC<TaskModalProps> = ({ isOpen, onClose, type, taskId }) => {
  const { state, addTask, updateTask } = useTaskContext();
  const { t } = useLanguage();
  const [initialData, setInitialData] = useState<TaskFormData | undefined>(undefined);

  // Set initial data when editing a task
  useEffect(() => {
    if (type === 'edit' && taskId && state.tasks.length > 0) {
      const task = state.tasks.find(t => t.id === taskId);
      if (task) {
        setInitialData({
          title: task.title,
          description: task.description || '',
          priority: task.priority,
          completed: task.completed,
          tags: task.tags,
          due_date: task.due_date || '',
          recurrence: task.recurrence || null,
        });
      }
    } else if (type === 'add') {
      setInitialData(undefined);
    }
  }, [type, taskId, state.tasks]);

  const handleSubmit = async (formData: TaskFormData) => {
    if (type === 'add') {
      await addTask(formData);
    } else if (type === 'edit' && taskId) {
      await updateTask(taskId, formData);
    }
    onClose();
  };

  const getTitle = () => {
    if (type === 'add') {
      return t('task.add');
    } else {
      return t('task.edit');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={getTitle()}>
      <TaskForm
        initialData={initialData}
        onSubmit={handleSubmit}
        onCancel={onClose}
      />
    </Modal>
  );
};

export default TaskModal;