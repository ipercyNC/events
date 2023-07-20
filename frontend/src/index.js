/*
 * index.js
 * 7/19/2023
 * Ian Percy
 * 
 * 
 * Render the application
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
