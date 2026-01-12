// Example unit test for Task model
import { Task } from '@/src/models/task';

describe('Task Model', () => {
  it('should create a task with required properties', () => {
    const task: Task = {
      id: 1,
      title: 'Test Task',
      description: 'Test Description',
      priority: 'high',
      tags: ['work', 'important'],
      completed: false,
      due_date: '2026-12-31T23:59:59Z',
      recurrence: 'weekly',
      created_at: '2026-01-01T10:00:00Z',
      updated_at: '2026-01-01T10:00:00Z',
    };

    expect(task.id).toBe(1);
    expect(task.title).toBe('Test Task');
    expect(task.priority).toBe('high');
    expect(task.tags).toContain('work');
    expect(task.completed).toBe(false);
  });

  it('should handle optional properties correctly', () => {
    const task: Task = {
      id: 2,
      title: 'Simple Task',
      priority: 'medium',
      tags: [],
      completed: true,
      created_at: '2026-01-01T10:00:00Z',
      updated_at: '2026-01-01T10:00:00Z',
    };

    expect(task.description).toBeUndefined();
    expect(task.due_date).toBeUndefined();
    expect(task.recurrence).toBeNull();
  });
});