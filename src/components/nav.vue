<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container d-flex justify-content-between align-items-center">
      <!-- Left: Logo -->
      <a class="navbar-brand d-flex align-items-center" href="#">
        <img :src="'src/data/face/c1133_l.png'" alt="Hero Image" />
        <span>E7Drafter</span>
      </a>

      <!-- Center: Nav Links -->
      <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="/auth">Login/Signup</a></li>
          <li class="nav-item"><a class="nav-link" href="/selector">Character Selector</a></li>
          <li class="nav-item"><a class="nav-link" href="#">About</a></li>
        </ul>
      </div>

      <!-- Right: Show user email if logged in -->
     <!-- Right: login/signup or user email -->
<div>
  <button
    @click="goToAuth"
    class="btn btn-outline-light d-flex align-items-center gap-2"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      fill="currentColor"
      class="bi bi-person-circle"
      viewBox="0 0 16 16"
    >
      <path
        d="M13.468 12.37C12.758 11.226 11.4 10.5 8 10.5c-3.4 0-4.76.726-5.468 1.87A6.987 6.987 0 0 0 8 15a6.987 6.987 0 0 0 5.468-2.63z"
      />
      <path fill-rule="evenodd" d="M8 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" />
      <path fill-rule="evenodd" d="M8 1a7 7 0 1 1 0 14A7 7 0 0 1 8 1z" />
    </svg>
    <span>{{ isLoggedIn ? userEmail : 'Login / Signup' }}</span>
  </button>
</div>
    </div>
  </nav>
</template>

<script>
import { API_BASE_URL } from './config';
export default {
  data() {
    return {
      userEmail: null,
      isLoggedIn: false,
    };
  },
  mounted() {
    this.checkAuthStatus();
  },
  methods: {
     async checkAuthStatus() {
    try {
      const response = await fetch(API_BASE_URL + '/auth/me', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        this.isLoggedIn = true;
        this.userEmail = data.email || 'Logged in';
      } else {
        this.isLoggedIn = false;
        this.userEmail = null;
      }
    } catch {
      this.isLoggedIn = false;
      this.userEmail = null;
    }
  },
  goToAuth() {
    window.location.href = '/authForm';  // Redirect to login/signup page
  },
  }
};
</script>

<style scoped>
.navbar-brand img {
  height: 40px;
}

.user-email {
  font-weight: 500;
  font-size: 0.9rem;
  white-space: nowrap;
  user-select: none;
}
</style>
