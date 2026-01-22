// API client for chat functionality
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const chatApi = {
  sendMessage: async (message: string, conversationId?: string) => {
    // Get user ID from token or storage
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    let userId = 'mock-user-id'; // Default fallback

    if (token) {
      try {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        userId = tokenPayload.userId || tokenPayload.sub || 'mock-user-id';
      } catch (error) {
        console.error('Error parsing token:', error);
      }
    }

    const url = conversationId
      ? `${API_BASE_URL}/chat/${userId}`
      : `${API_BASE_URL}/chat/${userId}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        conversation_id: conversationId,
        message,
        user_id: userId
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch (e) {
        errorData = { detail: errorText };
      }
      throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  }
};