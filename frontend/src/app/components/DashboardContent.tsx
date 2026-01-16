'use client';

import React, { useEffect } from 'react';
import { useTaskContext } from '@/contexts/TaskContext';
import { useLanguage } from '@/contexts/LanguageContext';
import { useAuth } from '@/contexts/AuthContext';
import TaskCard from '../components/tasks/TaskCard';
import TaskModal from '../components/tasks/TaskModal';
import GlassCard from '../components/ui/GlassCard';
import Toast from '@/components/ui/Toast';
import { TaskSkeleton } from '../components/ui/Skeleton';
import SearchInput from '../components/ui/SearchInput';
import FilterControls from '../components/tasks/FilterControls';
import SortControls from '../components/tasks/SortControls';
import LanguageToggle from '../components/ui/LanguageToggle';

const DashboardContent = () => {
  const { state, fetchTasks, openModal, closeModal, hideToast } = useTaskContext();
  const { t } = useLanguage();
  const { user, signOut } = useAuth();

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100 p-4 sm:p-6 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8 flex flex-col sm:flex-row justify-between items-center">
          <div className="text-center sm:text-left mb-4 sm:mb-0">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-800">{t('app.title')}</h1>
            <p className="text-gray-600 mt-2">{t('app.description')}</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-600">
              Welcome, {user?.username || user?.email}!
            </div>
            <button
              onClick={handleSignOut}
              className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
            >
              Sign Out
            </button>
            <div className="w-32">
              <LanguageToggle />
            </div>
          </div>
        </header>

        <div className="mb-8">
          <GlassCard>
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold text-gray-800">{t('task.title')}</h2>
              <button
                className="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors"
                onClick={() => openModal('add')}
              >
                {t('task.add')}
              </button>
            </div>
          </GlassCard>
        </div>

        <div className="mb-6 flex flex-wrap gap-4 items-center">
          <SearchInput className="w-full sm:w-64" />
          <FilterControls />
          <SortControls />
        </div>

        {state.loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <TaskSkeleton count={4} />
          </div>
        ) : state.filteredTasks.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-5xl mb-4">📋</div>
            <h3 className="text-xl font-medium text-gray-900">{t('task.noTasks')}</h3>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 transition-all duration-300">
            {state.filteredTasks.map(task => (
              <div
                key={task.id}
                className="transition-all duration-300 ease-in-out transform hover:scale-105"
              >
                <TaskCard task={task} />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Task Modal */}
      <TaskModal
        isOpen={state.modal.isOpen}
        onClose={closeModal}
        type={state.modal.type}
        taskId={state.modal.taskId}
      />

      {/* Toast notification */}
      <Toast toast={state.toast} onClose={hideToast} />
    </div>
  );
};

export default DashboardContent;