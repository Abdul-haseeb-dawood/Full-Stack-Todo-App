import { NextRequest } from 'next/server';
import { availableTools, ToolCall, ToolResult } from '@/lib/tools/taskTools';
import { processMessageWithGemini } from '@/lib/ai/geminiService';

// Define the response structure
interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls?: ToolCall[];
  tool_results?: ToolResult[];
  timestamp: string;
}

// Main handler for chat requests
export async function POST(request: NextRequest) {
  try {
    const { conversation_id, message, user_id } = await request.json();

    // Generate or use provided conversation ID
    const conversationId = conversation_id || `conv_${Date.now()}`;

    // Process the user's message using Gemini AI
    const geminiResponse = await processMessageWithGemini(message);
    let responseText = geminiResponse.response;
    const toolCalls = geminiResponse.toolCalls || [];

    let toolResults: ToolResult[] = [];

    // Execute tool calls if any
    let hasErrors = false;
    if (toolCalls.length > 0) {
      for (const toolCall of toolCalls) {
        const toolFunction = availableTools[toolCall.type];
        if (toolFunction) {
          try {
            const result = await toolFunction(toolCall.params);
            toolResults.push(result);

            // Check if there's an error to update the response
            if (!result.success) {
              hasErrors = true;
              responseText = `Error: ${result.message}`;
            }
          } catch (error) {
            console.error(`Error executing tool ${toolCall.type}:`, error);
            toolResults.push({
              success: false,
              message: `Error executing tool: ${(error as Error).message}`
            });
            hasErrors = true;
            responseText = `Error: ${(error as Error).message}`;
          }
        }
      }
    }

    // If no errors occurred and we have successful results, enhance the response
    if (!hasErrors && toolResults.length > 0) {
      const successfulResults = toolResults.filter(result => result.success);
      if (successfulResults.length > 0) {
        const successMessages = successfulResults.map(r => r.message).join('\n');
        responseText += `\n\n${successMessages}`;
      }
    }

    // Construct the response
    const response: ChatResponse = {
      conversation_id: conversationId,
      response: responseText,
      tool_calls: toolCalls,
      tool_results: toolResults,
      timestamp: new Date().toISOString()
    };

    return new Response(JSON.stringify(response), {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Error processing chat request:', error);

    const errorResponse: ChatResponse = {
      conversation_id: '',
      response: `Sorry, I encountered an error processing your request: ${(error as Error).message}`,
      timestamp: new Date().toISOString()
    };

    return new Response(JSON.stringify(errorResponse), {
      status: 500,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
}