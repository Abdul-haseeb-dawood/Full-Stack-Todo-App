'use client';

import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';

// Define available languages
type Language = 'en' | 'ur' | 'es' | 'fr' | 'de' | 'ja' | 'zh';

// Define translation structure
interface Translations {
  [key: string]: {
    [key: string]: string;
  };
}

// Define context type
interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

// Create context
const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Translation data
const translations: Translations = {
  en: {
    'app.title': 'Todo App',
    'app.description': 'Manage your tasks efficiently',
    'task.add': 'Add Task',
    'task.edit': 'Edit Task',
    'task.delete': 'Delete Task',
    'task.title': 'Title',
    'task.description': 'Description',
    'task.priority': 'Priority',
    'task.priority.high': 'High',
    'task.priority.medium': 'Medium',
    'task.priority.low': 'Low',
    'task.dueDate': 'Due Date',
    'task.tags': 'Tags',
    'task.recurrence': 'Recurrence',
    'task.recurrence.daily': 'Daily',
    'task.recurrence.weekly': 'Weekly',
    'task.recurrence.monthly': 'Monthly',
    'task.completed': 'Completed',
    'task.markComplete': 'Mark Complete',
    'task.markIncomplete': 'Mark Incomplete',
    'task.search': 'Search tasks...',
    'task.filter': 'Filter',
    'task.sort': 'Sort',
    'task.save': 'Save',
    'task.cancel': 'Cancel',
    'task.confirmDelete': 'Are you sure you want to delete this task?',
    'task.deleteConfirm': 'Delete',
    'task.noTasks': 'No tasks found',
    'task.addSuccess': 'Task added successfully',
    'task.updateSuccess': 'Task updated successfully',
    'task.deleteSuccess': 'Task deleted successfully',
    'task.error': 'An error occurred',
    'language.toggle': 'Language',
    'history.title': 'Task History',
    'history.description': 'View your task history',
    'history.noEntries': 'No history entries found',
    'history.created': 'Created',
    'history.updated': 'Updated',
    'history.completed': 'Completed',
    'history.deleted': 'Deleted',
    'history.action': 'Action',
    'history.time': 'Time',
    'history.task': 'Task',
  },
  ur: {
    'app.title': 'کام کی فہرست',
    'app.description': 'اپنے کام کو موثر انداز میں مینج کریں',
    'task.add': 'کام شامل کریں',
    'task.edit': 'کام میں ترمیم کریں',
    'task.delete': 'کام حذف کریں',
    'task.title': 'عنوان',
    'task.description': 'تفصیل',
    'task.priority': 'اہمیت',
    'task.priority.high': 'زیادہ',
    'task.priority.medium': 'متوسط',
    'task.priority.low': 'کم',
    'task.dueDate': 'آخری تاریخ',
    'task.tags': 'ٹیگز',
    'task.recurrence': 'دوبارہ',
    'task.recurrence.daily': 'روزانہ',
    'task.recurrence.weekly': 'ہفتہ وار',
    'task.recurrence.monthly': 'ماہانہ',
    'task.completed': 'مکمل',
    'task.markComplete': 'مکمل کریں',
    'task.markIncomplete': 'غیر مکمل کریں',
    'task.search': 'کام تلاش کریں...',
    'task.filter': 'فلٹر',
    'task.sort': 'چھانٹیں',
    'task.save': 'محفوظ کریں',
    'task.cancel': 'منسوخ کریں',
    'task.confirmDelete': 'کیا آپ واقعی یہ کام حذف کرنا چاہتے ہیں؟',
    'task.deleteConfirm': 'حذف کریں',
    'task.noTasks': 'کوئی کام نہیں ملا',
    'task.addSuccess': 'کام کامیابی سے شامل کر دیا گیا',
    'task.updateSuccess': 'کام کامیابی سے اپ ڈیٹ کر دیا گیا',
    'task.deleteSuccess': 'کام کامیابی سے حذف کر دیا گیا',
    'task.error': 'ایک خرابی پیش آ گئی',
    'language.toggle': 'زبان',
    'history.title': 'کام کی تاریخ',
    'history.description': 'اپنے کام کی تاریخ دیکھیں',
    'history.noEntries': 'کوئی تاریخ نہیں ملی',
    'history.created': 'تخلیق کیا گیا',
    'history.updated': 'اپ ڈیٹ کیا گیا',
    'history.completed': 'مکمل کیا گیا',
    'history.deleted': 'حذف کیا گیا',
    'history.action': 'کارروائی',
    'history.time': 'وقت',
    'history.task': 'کام',
  },
  es: {
    'app.title': 'Aplicación de Tareas',
    'app.description': 'Gestiona tus tareas eficientemente',
    'task.add': 'Agregar Tarea',
    'task.edit': 'Editar Tarea',
    'task.delete': 'Eliminar Tarea',
    'task.title': 'Título',
    'task.description': 'Descripción',
    'task.priority': 'Prioridad',
    'task.priority.high': 'Alta',
    'task.priority.medium': 'Media',
    'task.priority.low': 'Baja',
    'task.dueDate': 'Fecha de vencimiento',
    'task.tags': 'Etiquetas',
    'task.recurrence': 'Repetición',
    'task.recurrence.daily': 'Diario',
    'task.recurrence.weekly': 'Semanal',
    'task.recurrence.monthly': 'Mensual',
    'task.completed': 'Completado',
    'task.markComplete': 'Marcar como completado',
    'task.markIncomplete': 'Marcar como incompleto',
    'task.search': 'Buscar tareas...',
    'task.filter': 'Filtrar',
    'task.sort': 'Ordenar',
    'task.save': 'Guardar',
    'task.cancel': 'Cancelar',
    'task.confirmDelete': '¿Estás seguro de que quieres eliminar esta tarea?',
    'task.deleteConfirm': 'Eliminar',
    'task.noTasks': 'No se encontraron tareas',
    'task.addSuccess': 'Tarea agregada exitosamente',
    'task.updateSuccess': 'Tarea actualizada exitosamente',
    'task.deleteSuccess': 'Tarea eliminada exitosamente',
    'task.error': 'Ocurrió un error',
    'language.toggle': 'Idioma',
    'history.title': 'Historial de Tareas',
    'history.description': 'Ver historial de tareas',
    'history.noEntries': 'No se encontraron entradas de historial',
    'history.created': 'Creado',
    'history.updated': 'Actualizado',
    'history.completed': 'Completado',
    'history.deleted': 'Eliminado',
    'history.action': 'Acción',
    'history.time': 'Tiempo',
    'history.task': 'Tarea',
  },
};

// Provider component
export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLanguage] = useState<Language>('en'); // Initialize with default value

  // Initialize language from localStorage after component mounts
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const savedLanguage = localStorage.getItem('language') as Language | null;
      if (savedLanguage) {
        setLanguage(savedLanguage);
      }
    }
  }, []);

  // Save language to localStorage whenever it changes
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('language', language);
    }
  }, [language]);

  // Translation function
  const t = (key: string): string => {
    const translation = translations[language]?.[key];
    if (!translation) {
      // Fallback to English if translation doesn't exist
      return translations.en[key] || key;
    }
    return translation;
  };

  // Function to change language
  const changeLanguage = (lang: Language) => {
    setLanguage(lang);
  };

  const value = {
    language,
    setLanguage: changeLanguage,
    t,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

// Custom hook to use the language context
export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};