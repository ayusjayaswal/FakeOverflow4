const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE;

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = null;
  }

  setToken(token) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  getToken() {
    if (this.token) return this.token;
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
    return this.token;
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = this.getToken();
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers,
      },
      ...options,
    };

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      return await response.text();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async register(userData) {
    return this.request('/api/v1/auth/register', {
      method: 'POST',
      body: userData,
    });
  }

  async login(credentials) {
    return this.request('/api/v1/auth/login', {
      method: 'POST',
      body: credentials,
    });
  }

  async getCurrentUser() {
    return this.request('/api/v1/users/me');
  }

  async getUser(userId) {
    return this.request(`/api/v1/users/${userId}`);
  }

  async getDiscussions(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/v1/discussions/${queryString ? '?' + queryString : ''}`);
  }

  async getDiscussion(discussionId) {
    return this.request(`/api/v1/discussions/${discussionId}`);
  }

  async createDiscussion(discussionData) {
    return this.request('/api/v1/discussions/', {
      method: 'POST',
      body: discussionData,
    });
  }

  async updateDiscussion(discussionId, discussionData) {
    return this.request(`/api/v1/discussions/${discussionId}`, {
      method: 'PUT',
      body: discussionData,
    });
  }

  async deleteDiscussion(discussionId) {
    return this.request(`/api/v1/discussions/${discussionId}`, {
      method: 'DELETE',
    });
  }

  async getUserDiscussions(userId) {
    return this.request(`/api/v1/discussions/user/${userId}`);
  }

  async getDiscussionComments(discussionId, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/api/v1/comments/discussion/${discussionId}${queryString ? '?' + queryString : ''}`);
  }

  async createComment(commentData) {
    return this.request('/api/v1/comments/', {
      method: 'POST',
      body: commentData,
    });
  }

  async getComment(commentId) {
    return this.request(`/api/v1/comments/${commentId}`);
  }

  async updateComment(commentId, commentData) {
    return this.request(`/api/v1/comments/${commentId}`, {
      method: 'PUT',
      body: commentData,
    });
  }

  async deleteComment(commentId) {
    return this.request(`/api/v1/comments/${commentId}`, {
      method: 'DELETE',
    });
  }

  async search(query, params = {}) {
    const queryParams = new URLSearchParams({ q: query, ...params }).toString();
    return this.request(`/api/v1/search/?${queryParams}`);
  }

  async getSearchSuggestions(query, limit = 10) {
    const queryParams = new URLSearchParams({ q: query, limit }).toString();
    return this.request(`/api/v1/search/suggestions?${queryParams}`);
  }
}

export const apiClient = new ApiClient();
