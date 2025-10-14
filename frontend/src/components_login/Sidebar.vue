<template>
    <div>
        <!-- Botón hamburguesa para móviles -->
        <button class="menu-toggle" @click="toggleSidebar">
            ☰
        </button>
        
        <!-- Overlay para móviles -->
        <div class="overlay" :class="{ active: sidebarOpen }" @click="closeSidebar"></div>
        
        <aside class="sidebar" :class="{ open: sidebarOpen }">
            <div class="menu-section">
                <span class="menu-title">MENÚ</span>
                <ul>
                    <li class="active">
                        <RouterLink to="audios" class="menu-link" @click="closeSidebar">
                            <i class="icon">🏠</i> <span>Audios</span>
                        </RouterLink>
                    </li>
                    <li>
                        <a href="#" @click="closeSidebar">
                            <i class="icon">🔍</i>
                            <span>Explorar</span>
                        </a>
                    </li>
                    <li>
                        <a href="#" @click="closeSidebar">
                            <i class="icon">📻</i>
                            <span>Radio</span>
                        </a>
                    </li>
                    <li>
                        <a href="#" @click="closeSidebar">
                            <i class="icon">📅</i>
                            <span>Programación</span>
                        </a>
                    </li>
                </ul>
            </div>
            <div class="library-section">
                <span class="menu-title">TU BIBLIOTECA</span>
                <ul>
                    <li>
                        <RouterLink to="/" class="menu-link" @click="closeSidebar">
                            <i class="icon">❤️</i>
                            <span>Streaming</span>
                        </RouterLink>
                    </li>
                    <li>
                        <a href="#" @click="closeSidebar">
                            <i class="icon">🕒</i>
                            <span>Recientes</span>
                        </a>
                    </li>
                    <li>
                        <a href="#" @click="closeSidebar">
                            <i class="icon">📄</i>
                            <span>Listas</span>
                        </a>
                    </li>
                </ul>
            </div>
            <div class="logout-section">
                <a href="#" class="logout-btn" @click.prevent="logout">
                    <i class="icon">➡️</i>
                    <span>Cerrar Sesión</span>
                </a>
            </div>
        </aside>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const sidebarOpen = ref(false)

const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
    if (window.innerWidth <= 768) {
        sidebarOpen.value = false
    }
}

const logout = () => {
    // Borrar tokens
    localStorage.removeItem('auth_tokens')
    // Redirigir al login
    router.push('/login')
}

// Cerrar sidebar al redimensionar a pantalla grande
const handleResize = () => {
    if (window.innerWidth > 768) {
        sidebarOpen.value = false
    }
}

onMounted(() => {
    window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.sidebar {
    width: 240px;
    background-color: #ffffff;
    padding: 24px;
    display: flex;
    flex-direction: column;
    height: 100vh;
    flex-shrink: 0;
    transition: transform 0.3s ease;
}

.menu-section,
.library-section {
    margin-bottom: 30px;
}

.menu-title {
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 15px;
    display: block;
    font-weight: bold;
}

ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

li a {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px 15px;
    border-radius: 8px;
    text-decoration: none;
    color: #555;
    font-weight: 500;
    transition: background-color 0.2s, color 0.2s;
}

li.active a {
    background-color: #e3f2fd;
    color: #03a9f4;
}

li a:hover {
    background-color: #f0f0f0;
}

.icon {
    font-style: normal;
}

.logout-section {
    margin-top: auto;
    padding-top: 24px;
}

.logout-btn {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px 15px;
    border-radius: 8px;
    text-decoration: none;
    color: #d32f2f;
    font-weight: 500;
    transition: background-color 0.2s, color 0.2s;
    width: 100%;
}

.logout-btn:hover {
    background-color: #ffebee;
    color: #b71c1c;
}

/* Elementos responsive */
.menu-toggle {
    display: none;
    position: fixed;
    top: 15px;
    left: 15px;
    z-index: 1001;
    background: #03a9f4;
    color: white;
    border: none;
    border-radius: 4px;
    width: 40px;
    height: 40px;
    font-size: 20px;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 998;
}

.overlay.active {
    display: block;
}

/* Responsive para móviles */
@media (max-width: 768px) {
    .menu-toggle {
        display: block;
    }
    
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        transform: translateX(-100%);
        z-index: 999;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    .sidebar.open {
        transform: translateX(0);
    }
}

/* Responsive para tablets */
@media (min-width: 769px) and (max-width: 1024px) {
    .sidebar {
        width: 70px;
        padding: 24px 10px;
        align-items: center;
    }
    
    .sidebar .menu-title,
    .sidebar span:not(.icon) {
        display: none;
    }
    
    .sidebar li a {
        justify-content: center;
        padding: 10px;
    }
    
    .sidebar .icon {
        margin: 0;
    }
}
</style>