import { gql } from '@apollo/client';

export const GET_TODOS = gql`
  query GetTodos {
    todos {
      id
      text
      completed
      created_at
      updated_at
    }
  }
`;

export const CREATE_TODO = gql`
  mutation CreateTodo($text: String!) {
    createTodo(text: $text) {
      todo {
        id
        text
        completed
        created_at
        updated_at
      }
    }
  }
`;

export const UPDATE_TODO = gql`
  mutation UpdateTodo($id: Int!, $text: String, $completed: Boolean) {
    updateTodo(id: $id, text: $text, completed: $completed) {
      todo {
        id
        text
        completed
        created_at
        updated_at
      }
    }
  }
`;

export const DELETE_TODO = gql`
  mutation DeleteTodo($id: Int!) {
    deleteTodo(id: $id) {
      success
    }
  }
`; 