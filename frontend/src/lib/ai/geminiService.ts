// Service for interacting with Google Gemini API
import { availableTools, ToolCall, ToolResult } from '@/lib/tools/taskTools';

const GEMINI_API_KEY = 'AIzaSyAxY93o1NNa-0Yo7HaV7qwR7JTNiDfx7Nc';
const GEMINI_API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`;

// Simple NLP processor to determine intent and extract entities
const processIntent = (message: string): { intent: string | null; entities: Record<string, any> } => {
  const lowerMsg = message.toLowerCase();
  
  // Define patterns for different intents
  const patterns: Array<{ intent: string; regex: RegExp; extract?: (match: RegExpMatchArray) => Record<string, any> }> = [
    {
      intent: 'add_task',
      regex: /(add|create|make|new)\s+(a\s+)?task\s+to\s+(.+)|add\s+(.+)\s+to\s+my\s+todo/,
      extract: (match) => {
        // Extract the task description from the matched groups
        const description = match[3] || match[4] || '';
        return { title: description.trim() };
      }
    },
    {
      intent: 'get_tasks',
      regex: /(show|list|display|see)\s+(all\s+)?(my\s+)?(tasks|todos)/,
      extract: () => ({})
    },
    {
      intent: 'get_pending_tasks',
      regex: /(show|list|display|see)\s+(my\s+)?(pending|incomplete|open)\s+(tasks|todos)/,
      extract: () => ({ status: 'pending' })
    },
    {
      intent: 'get_completed_tasks',
      regex: /(show|list|display|see)\s+(my\s+)?(completed|done|finished)\s+(tasks|todos)/,
      extract: () => ({ status: 'completed' })
    },
    {
      intent: 'get_in_progress_tasks',
      regex: /(show|list|display|see)\s+(my\s+)?(in-progress|working-on|active)\s+(tasks|todos)/,
      extract: () => ({ status: 'in-progress' })
    },
    {
      intent: 'mark_task_complete',
      regex: /(mark|set|complete|finish|done)\s+(the\s+)?(.+?)\s+(as\s+)?(complete|done|finished)/,
      extract: (match) => {
        const taskTitle = match[3] || '';
        return { title: taskTitle.trim() };
      }
    },
    {
      intent: 'set_task_priority',
      regex: /(set|change|update)\s+(the\s+)?(.+?)\s+(to\s+)?(high|medium|low)\s+priority/,
      extract: (match) => {
        const taskTitle = match[3] || '';
        const priority = match[5] as 'high' | 'medium' | 'low';
        return { title: taskTitle.trim(), priority };
      }
    },
    {
      intent: 'update_task',
      regex: /(update|change|modify|edit)\s+(the\s+)?(.+?)\s+(title|description|status|priority)/,
      extract: (match) => {
        const taskTitle = match[3] || '';
        return { title: taskTitle.trim() };
      }
    },
    {
      intent: 'delete_task',
      regex: /(delete|remove|cancel)\s+(the\s+)?(.+?)\s+(task|from|from\s+my\s+todo)/,
      extract: (match) => {
        const taskTitle = match[3] || '';
        return { title: taskTitle.trim() };
      }
    }
  ];

  // Check for matches
  for (const pattern of patterns) {
    const match = lowerMsg.match(pattern.regex);
    if (match) {
      const entities = pattern.extract ? pattern.extract(match) : {};
      return { intent: pattern.intent, entities };
    }
  }

  // If no pattern matches, return null
  return { intent: null, entities: {} };
};

// Find a task by title from the list of tasks
const findTaskByTitle = async (title: string): Promise<{ id: string } | null> => {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/v1/tasks/`);
    if (!response.ok) {
      console.error('Failed to fetch tasks:', response.statusText);
      return null;
    }
    
    const tasks = await response.json();
    const task = tasks.find((t: any) => 
      t.title.toLowerCase().includes(title.toLowerCase()) || 
      title.toLowerCase().includes(t.title.toLowerCase())
    );
    
    return task ? { id: task.id } : null;
  } catch (error) {
    console.error('Error finding task by title:', error);
    return null;
  }
};

// Process a message using Gemini API
export const processMessageWithGemini = async (message: string, conversationHistory: Array<{role: string, content: string}> = []): Promise<{ response: string; toolCalls?: ToolCall[] }> => {
  try {
    // First, try to determine intent locally
    const { intent, entities } = processIntent(message);
    
    if (intent) {
      let toolCalls: ToolCall[] = [];
      let responseText = '';

      switch (intent) {
        case 'add_task':
          // Prepare parameters for adding a task
          let taskTitle = entities.title;
          if (!taskTitle) {
            // Extract task title from the message using the regex pattern
            const addRegex = /(add|create|make|new)\s+(a\s+)?task\s+to\s+(.+)|add\s+(.+)\s+to\s+my\s+todo/i;
            const match = message.match(addRegex);
            if (match) {
              taskTitle = (match[3] || match[4] || '').trim();
            }
          }
          
          const addParams = {
            title: taskTitle || 'Untitled task',
            priority: entities.priority || 'medium'
          };
          
          toolCalls.push({
            type: 'add_task',
            params: addParams
          });
          
          responseText = `I'll add "${addParams.title}" to your todo list.`;
          break;

        case 'get_tasks':
          toolCalls.push({
            type: 'get_tasks',
            params: {}
          });
          
          responseText = "I'll fetch all your tasks.";
          break;

        case 'get_pending_tasks':
          toolCalls.push({
            type: 'get_tasks_by_status',
            params: { status: 'pending' }
          });
          
          responseText = "I'll fetch your pending tasks.";
          break;

        case 'get_completed_tasks':
          toolCalls.push({
            type: 'get_tasks_by_status',
            params: { status: 'completed' }
          });
          
          responseText = "I'll fetch your completed tasks.";
          break;

        case 'get_in_progress_tasks':
          toolCalls.push({
            type: 'get_tasks_by_status',
            params: { status: 'in-progress' }
          });
          
          responseText = "I'll fetch your in-progress tasks.";
          break;

        case 'mark_task_complete':
          // Find the task by title
          const taskToComplete = await findTaskByTitle(entities.title);
          if (taskToComplete) {
            toolCalls.push({
              type: 'mark_task_complete',
              params: { id: taskToComplete.id }
            });
            
            responseText = `I'll mark "${entities.title}" as complete.`;
          } else {
            responseText = `I couldn't find a task titled "${entities.title}". Could you please clarify?`;
          }
          break;

        case 'set_task_priority':
          // Find the task by title
          const taskForPriority = await findTaskByTitle(entities.title);
          if (taskForPriority) {
            toolCalls.push({
              type: 'set_task_priority',
              params: { 
                id: taskForPriority.id,
                priority: entities.priority
              }
            });
            
            responseText = `I'll set the priority of "${entities.title}" to ${entities.priority}.`;
          } else {
            responseText = `I couldn't find a task titled "${entities.title}". Could you please clarify?`;
          }
          break;

        case 'update_task':
          // Find the task by title
          const taskToUpdate = await findTaskByTitle(entities.title);
          if (taskToUpdate) {
            // For now, we'll just acknowledge the update request
            responseText = `What would you like to update about "${entities.title}"?`;
          } else {
            responseText = `I couldn't find a task titled "${entities.title}". Could you please clarify?`;
          }
          break;

        case 'delete_task':
          // Find the task by title
          const taskToDelete = await findTaskByTitle(entities.title);
          if (taskToDelete) {
            toolCalls.push({
              type: 'delete_task',
              params: { id: taskToDelete.id }
            });
            
            responseText = `I'll delete "${entities.title}" from your todo list.`;
          } else {
            responseText = `I couldn't find a task titled "${entities.title}". Could you please clarify?`;
          }
          break;

        default:
          responseText = `I received your request: "${message}". How else can I help with your todos?`;
      }

      return {
        response: responseText,
        toolCalls
      };
    } else {
      // If local processing didn't identify an intent, use Gemini API
      const prompt = `
        You are a helpful AI assistant for managing a todo list. 
        The user sent this message: "${message}"
        
        Based on this message, determine what action they want to take with their todo list.
        Possible actions are: add_task, get_tasks, get_pending_tasks, get_completed_tasks, mark_task_complete, set_task_priority, update_task, delete_task.
        
        Respond in JSON format with the action and any relevant parameters.
      `;
      
      const requestBody = {
        contents: [{
          parts: [{
            text: prompt
          }]
        }]
      };

      const geminiResponse = await fetch(GEMINI_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!geminiResponse.ok) {
        throw new Error(`Gemini API error: ${geminiResponse.status}`);
      }

      const data = await geminiResponse.json();
      const responseText = data.candidates?.[0]?.content?.parts?.[0]?.text || `I received your message: "${message}". How else can I help with your todos?`;
      
      return {
        response: responseText
      };
    }
  } catch (error) {
    console.error('Error processing message with Gemini:', error);
    return {
      response: `Sorry, I encountered an error processing your request: ${(error as Error).message}`
    };
  }
};