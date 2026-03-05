import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

const router = createRouter({
  history: createWebHistory('/web/'),
  routes: [
    { path: '/', redirect: '/personas' },
    { path: '/personas', name: 'personas', component: () => import('./views/Personas.vue') },
    { path: '/providers', name: 'providers', component: () => import('./views/Providers.vue') },
    { path: '/napcat', name: 'napcat', component: () => import('./views/NapCat.vue') },
    { path: '/settings', name: 'settings', component: () => import('./views/Settings.vue') },
  ],
})

createApp(App).use(router).mount('#app')
