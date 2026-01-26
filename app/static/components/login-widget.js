const loginTemplate = document.createElement('template');

loginTemplate.innerHTML = `
  <style>
    :host {
      display: block;
      font-family: sans-serif;
    }
    .login-container {
      border: 1px solid #ccc;
      padding: 20px;
      border-radius: 8px;
      max-width: 300px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      margin: 10px 0px;
    }
    h3 {
      margin-top: 0;
    }
    .form-group {
      margin-bottom: 15px;
    }
    label {
      display: block;
      margin-bottom: 5px;
    }
    input {
      width: 100%;
      padding: 8px;
      box-sizing: border-box;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    button {
      width: 100%;
      padding: 10px;
      border: none;
      background-color: #007bff;
      color: white;
      border-radius: 4px;
      cursor: pointer;
    }
    button:hover {
      background-color: #0056b3;
    }
  </style>
  <div class="login-container" part="container">
    <h3>Login</h3>
    <form>
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
      </div>
      <button type="submit">Sign In</button>
    </form>
  </div>
`;

class LoginWidget extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.appendChild(loginTemplate.content.cloneNode(true));
  }
}

window.customElements.define('login-widget', LoginWidget);