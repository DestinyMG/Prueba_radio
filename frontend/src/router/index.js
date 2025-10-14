import { createRouter, createWebHistory } from 'vue-router'
// import HelloWorld from '../components_login/HelloWorld.vue'
import Home from '../pages/Home.vue'
import Prueba from '../components_login/Prueba.vue'
import Audios from '../components_login/Audios.vue'
import Login from '../components_login/Login.vue'
import Prueba_audio from '../components_login/Prueba_audio.vue'
import Transmitter from '../components_login/Transmitter.vue'
import newsAdmin from '../components_login/newsAdmin.vue'
import programacionAdmin from '../components_login/programacionAdmin.vue' // ← Agregar esta línea

const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/prueba', component: Prueba },
    { path: '/audios', component: Audios, name: 'audios', meta: { requiresAuth: true } },
    { path: '/login', component: Login },
    { path: '/reproducir', component: Prueba_audio },
    { path: '/transmitter', component: Transmitter },
    { path: '/admin/news', component: newsAdmin, name: 'news-admin', meta: { requiresAuth: true } },
    { path: '/admin/programacion', component: programacionAdmin, name: 'programacion-admin', meta: { requiresAuth: true } }, // ← Agregar esta ruta
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Navigation Guard global usando localStorage
router.beforeEach((to, from, next) => {
    const storedTokens = localStorage.getItem('auth_tokens')
    const token = storedTokens ? JSON.parse(storedTokens).access : null

    if (to.meta.requiresAuth && !token) {
        // Ruta protegida y no hay token, redirigir a login
        next({ path: '/login' })
    } else {
        // Token presente o ruta pública, permitir acceso
        next()
    }
})

export default router