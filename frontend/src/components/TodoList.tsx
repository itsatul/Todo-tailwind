import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface Todo {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  user: {
    id: number;
    username: string;
    email: string;
  };
}

const TodoList = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const fetchTodos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Fetching todos with token:', token);
      const response = await axios.get('http://localhost:8000/api/todos/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log('Todos response:', response.data);
      
      // Ensure we have an array
      const todosData = Array.isArray(response.data) ? response.data : [];
      console.log('Processed todos data:', todosData);
      setTodos(todosData);
    } catch (error) {
      console.error('Error fetching todos:', error);
      setError('Failed to fetch todos');
      setTodos([]);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    if (token) {
      fetchTodos();
    }
  }, [token, fetchTodos]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(
        'http://localhost:8000/api/todos/',
        { 
          title: newTodo, 
          description: newDescription,
          completed: false 
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      console.log('Added todo response:', response.data);
      setTodos(prevTodos => [...prevTodos, response.data]);
      setNewTodo('');
      setNewDescription('');
    } catch (error) {
      console.error('Error adding todo:', error);
      setError('Failed to add todo');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTodo = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      const todo = todos.find(t => t.id === id);
      if (!todo) return;

      const response = await axios.patch(
        `http://localhost:8000/api/todos/${id}/`,
        { completed: !todo.completed },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      console.log('Updated todo response:', response.data);
      setTodos(prevTodos => prevTodos.map(t => t.id === id ? response.data : t));
    } catch (error) {
      console.error('Error toggling todo:', error);
      setError('Failed to update todo');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      setLoading(true);
      setError(null);
      await axios.delete(`http://localhost:8000/api/todos/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTodos(prevTodos => prevTodos.filter(t => t.id !== id));
    } catch (error) {
      console.error('Error deleting todo:', error);
      setError('Failed to delete todo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Todo List</h1>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
        >
          Logout
        </button>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}
      
      <form onSubmit={handleAddTodo} className="mb-4">
        <div className="space-y-4">
          <div>
            <input
              type="text"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              placeholder="Add a new todo"
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <textarea
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              placeholder="Add description (optional)"
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              rows={3}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {loading ? 'Adding...' : 'Add Todo'}
          </button>
        </div>
      </form>

      {loading && todos.length === 0 ? (
        <div className="text-center py-4">Loading todos...</div>
      ) : todos.length === 0 ? (
        <div className="text-center py-4 text-gray-500">No todos yet. Add one above!</div>
      ) : (
        <ul className="space-y-4">
          {todos.map(todo => (
            <li
              key={todo.id}
              className="p-4 bg-white rounded-md shadow hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={todo.completed}
                      onChange={() => handleToggleTodo(todo.id)}
                      className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <span className={`ml-3 text-lg ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {todo.title}
                    </span>
                  </div>
                  {todo.description && (
                    <p className="ml-7 mt-2 text-gray-600">{todo.description}</p>
                  )}
                  <p className="ml-7 mt-2 text-sm text-gray-400">
                    Created: {new Date(todo.created_at).toLocaleDateString()}
                  </p>
                </div>
                <button
                  onClick={() => handleDeleteTodo(todo.id)}
                  className="ml-4 text-red-600 hover:text-red-800 focus:outline-none"
                  disabled={loading}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TodoList; 