<template>
  <div class="auth-container">
    <div class="auth-form" v-if="!isLoggedIn">
      <h2>{{ isLogin ? 'Login' : 'Register' }}</h2>
      <form @submit.prevent="handleSubmit">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">{{ isLogin ? 'Login' : 'Register' }}</button>
      </form>
      <p @click="toggleMode">
        {{ toggleText }}
      </p>
    </div>

    <div v-else>
      <p style="color: #ddd; font-weight: 600;">
  You are logged in as {{ username }}
</p>
      <button @click="handleLogout">Sign Out</button>
    </div>
  </div>
</template>

<script>
import { API_BASE_URL } from './config';

export default {
  data() {
    return {
      username: '',
      password: '',
      isLogin: true,
      isLoggedIn: false,
    };
  },
  computed: {
    toggleText() {
      return this.isLogin
        ? "Don't have an account? Register"
        : "Already have an account? Login";
    }
  },
  mounted() {
    this.checkAuthStatus();
  },
  methods: {
    toggleMode() {
      this.isLogin = !this.isLogin;
    },

    async checkAuthStatus() {
      try {
        const response = await fetch(API_BASE_URL + '/auth/me', {
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          this.isLoggedIn = true;
          this.username = data.email || 'User';
        } else {
          this.isLoggedIn = false;
        }
      } catch (error) {
        this.isLoggedIn = false;
      }
    },

async handleSubmit() {
  const endpoint = this.isLogin ? '/auth/jwt/login' : '/auth/register';

  try {
    let response;

    if (this.isLogin) {
      // Login request
      const formData = new URLSearchParams();
      formData.append('username', this.username);
      formData.append('password', this.password);

      response = await fetch(API_BASE_URL + endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
        credentials: 'include',
      });

    } else {
      // Registration: Validate password first
      const password = this.password;
      const minLength = 8;
      const hasNumberOrSpecial = /[\d\W]/.test(password);

      if (password.length < minLength) {
        alert('Password must be at least 8 characters long.');
        return;
      }

      if (!hasNumberOrSpecial) {
        alert('Password must include at least one number or special character.');
        return;
      }

      // Registration request
      const payload = { email: this.username, password: this.password };
      response = await fetch(API_BASE_URL + endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        credentials: 'include',
      });

      if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.message || response.statusText}`);
        return;
      }

      // After successful registration, immediately log in
      const loginFormData = new URLSearchParams();
      loginFormData.append('username', this.username);
      loginFormData.append('password', this.password);

      response = await fetch(API_BASE_URL + '/auth/jwt/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: loginFormData,
        credentials: 'include',
      });
    }

    if (!response.ok) {
      const error = await response.json();
      alert(`Error: Incorrect username or password`);
      return;
    }

    // Success - update UI and reset password field
    this.isLoggedIn = true;
    this.password = '';
    if (!this.isLogin) this.isLogin = true;

  } catch (err) {
    alert('Network or server error: ' + err.message);
  }
},


    async handleLogout() {
      try {
        const response = await fetch(API_BASE_URL + '/auth/logout', {
          method: 'POST',
          credentials: 'include',
        });
        if (response.ok) {
          this.isLoggedIn = false;
          this.username = '';
          this.password = '';
          this.isLogin = true;
        } else {
          alert('Logout failed');
        }
      } catch (error) {
        console.error(error);
        alert('Failed to connect to server');
      }
    },
  },
};
</script>



<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #1e1e1e;
}

.auth-form {
  background: #2c2c2c;
  padding: 30px 40px;
  border-radius: 10px;
  box-shadow: 0 0 10px #000;
  width: 300px;
  color: #fff;
  text-align: center;
}

.auth-form h2 {
  margin-bottom: 20px;
  font-weight: normal;
}

.auth-form input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: none;
  border-radius: 5px;
  background: #444;
  color: white;
}

.auth-form input:focus {
  outline: none;
  background: #555;
}

.auth-form button {
  width: 100%;
  padding: 10px;
  background: #007bff;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
}

.auth-form button:hover {
  background: #0056b3;
}

.auth-form p {
  margin-top: 15px;
  font-size: 14px;
  cursor: pointer;
  color: #aaa;
}

.auth-form p:hover {
  color: #fff;
}
</style>
