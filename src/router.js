import { createRouter, createWebHistory } from 'vue-router';
import CharacterGrid from '../src/components/CharacterGrid.vue'; // Example view
import AuthForm from '../src/components/AuthForm.vue';
import selector from '../src/components/selector.vue';
const routes = [

  {
    path: '/',
    name: 'CharacterGrid',
    component: CharacterGrid,
  },
 {
    path: '/auth',
    name: 'AuthForm',
    component: AuthForm,
  },
   {
    path: '/selector',
    name: 'selector',
    component: selector,
  }
  // Add other routes here
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
