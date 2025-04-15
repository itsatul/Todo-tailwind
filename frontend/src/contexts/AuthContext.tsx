import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  signup: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Create axios instance with base config
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      // Set the default Authorization header for all requests
      api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
    }
  }, []);

  const login = async (username: string, password: string) => {
    try {
      console.log('Attempting login with:', { username });
      
      // Get JWT tokens - send data as JSON
      const tokenResponse = await api.post('/api/token/', {
        username: username, // This will be the email when logging in with email
        password: password,
      }, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      console.log('Token response:', tokenResponse.data);
      
      const { access, refresh } = tokenResponse.data;
      
      // Set token in state and localStorage
      setToken(access);
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      
      // Set the default Authorization header
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      // Get user profile
      const userResponse = await api.get('/api/auth/me/');
      setUser(userResponse.data);
      localStorage.setItem('user', JSON.stringify(userResponse.data));
      
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('Login failed:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message,
          request: {
            url: error.config?.url,
            method: error.config?.method,
            data: error.config?.data,
          }
        });
      }
      throw error;
    }
  };

  const signup = async (username: string, email: string, password: string) => {
    try {
      const response = await api.post('/api/auth/register/', {
        username,
        email,
        password,
      });
      
      // After successful registration, login the user
      await login(username, password);
      
    } catch (error) {
      console.error('Signup failed:', error);
      throw error;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    delete api.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        signup,
        logout,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 