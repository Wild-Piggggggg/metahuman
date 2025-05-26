<template>
    <footer class="app-footer">
      © 2025 Your Application Name. All rights reserved. |
      <a href="#" target="_blank" rel="noopener noreferrer">备案号: 京ICP备XXXXXXXX号-X</a>
    </footer>
  </template>
  
  <script>
  export default {
    name: 'AppFooter'
  }
  </script>
  
  <style scoped>
  .app-footer {
    background-color: #f8f9fa;
    color: #6c757d;
    text-align: center;
    padding: 15px;
    font-size: 14px;
    border-top: 1px solid #ddd; /* Use var(--border-color) if preferred */
    margin-top: auto; /* Pushes footer to bottom */
    width: 100%;
  }
  
  .app-footer a {
      color: #6c757d;
      text-decoration: none;
  }
  .app-footer a:hover {
      text-decoration: underline;
  }
  </style>