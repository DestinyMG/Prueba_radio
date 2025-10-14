<template>
    <header class="app-header">
        <!-- Menú hamburguesa -->
        <button class="menu-toggle" @click="toggleSidebar">
            <i class="fas fa-bars"></i>
        </button>
        
        <!-- Logo -->
        <div class="logo">
            <img src="../assets/images/Logo color.png" alt="KyeroRadio" class="logo-image">
            <span>KyeroRadio</span>
        </div>

         <!-- Perfil de usuario -->
        <div class="user-profile">
            <div class="profile-container">
                <div class="profile-info">
                    <div class="user-avatar">
                        <img src="../assets/images/avatar.png" alt="Usuario">
                    </div>
                    <div class="user-details">
                        <span class="user-name">Admin</span>
                    </div>
                </div>
                <div class="profile-dropdown">
                    <button class="dropdown-toggle" @click="toggleDropdown">
                        <i class="fas fa-chevron-down"></i>
                    </button>
                    <div class="dropdown-menu" :class="{ active: dropdownOpen }">
                        <div class="dropdown-item logout" @click="logout">
                            <i class="fas fa-sign-out-alt"></i>
                            <span>Cerrar Sesión</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Overlay -->
        <div class="overlay" :class="{ active: sidebarOpen }" @click="closeSidebar"></div>
        
        <!-- Sidebar -->
        <aside class="sidebar" :class="{ open: sidebarOpen }">
            <!-- Header del sidebar -->
            <div class="sidebar-header">
                <div class="sidebar-logo">
                    <img src="../assets/images/Logo color.png" alt="KyeroRadio" class="logo-image">
                    <span>KyeroRadio</span>
                </div>
                <button class="sidebar-close" @click="closeSidebar">
                    <i class="fas fa-times"></i>
                </button>
            </div>

            <!-- Contenido del sidebar -->
            <div class="sidebar-content">
                <nav class="sidebar-nav">
                    <div class="nav-section">
                        <h3 class="nav-title">MENÚ PRINCIPAL</h3>
                        <ul class="nav-list">
                            <li :class="{ active: $route.path.includes('audios') }">
                                <RouterLink to="/audios" class="nav-link" @click="closeSidebar">
                                    <div class="nav-icon">
                                        <i class="fas fa-music"></i>
                                    </div>
                                    <span class="nav-text">Mis Audios</span>
                                </RouterLink>
                            </li>
                            <li>
                                <RouterLink to="/admin/programacion" class="nav-link" @click="closeSidebar">
                                    <div class="nav-icon">
                                        <i class="fas fa-calendar-alt"></i>
                                    </div>
                                    <span class="nav-text">Programación</span>
                                </RouterLink>
                            </li>
                            <li>
                                <router-link to="/admin/news" class="nav-link" @click="closeSidebar">
                                    <div class="nav-icon">
                                        <i class="fas fa-newspaper"></i> <!-- Cambié el icono a newspaper -->
                                    </div>
                                    <span class="nav-text">Noticias</span> <!-- Cambié el texto -->
                                </router-link>
                            </li>
                        </ul>
                    </div>
                </nav>
            </div>
        </aside>
    </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estados reactivos
const mobileSearchActive = ref(false)
const sidebarOpen = ref(false)
const dropdownOpen = ref(false)

// Referencias del DOM
const profileContainer = ref(null)

// Funciones del sidebar
const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
    sidebarOpen.value = false
}

// Funciones del dropdown del perfil
const toggleDropdown = () => {
    dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
    dropdownOpen.value = false
}

const logout = () => {
    closeDropdown()
    // Aquí iría la lógica para cerrar sesión
    console.log('Cerrando sesión...');
    localStorage.removeItem('auth_tokens')
    router.push('/login')
}

// Funciones de búsqueda móvil
const toggleMobileSearch = () => {
    mobileSearchActive.value = !mobileSearchActive.value
}

// Manejar clics fuera del dropdown
const handleClickOutside = (event) => {
    if (profileContainer.value && !profileContainer.value.contains(event.target)) {
        closeDropdown()
    }
}

// Cerrar sidebar con ESC
const handleKeydown = (e) => {
    if (e.key === 'Escape' && sidebarOpen.value) {
        closeSidebar()
    }
    if (e.key === 'Escape' && dropdownOpen.value) {
        closeDropdown()
    }
}

// Cerrar sidebar al redimensionar
const handleResize = () => {
    if (window.innerWidth > 768) {
        closeSidebar()
        mobileSearchActive.value = false
    }
}

// Lifecycle hooks
onMounted(() => {
    window.addEventListener('resize', handleResize)
    window.addEventListener('keydown', handleKeydown)
    document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('keydown', handleKeydown)
    document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.app-header {
    display: flex;
    align-items: center;
    padding: 0 2rem;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    height: 70px;
    flex-shrink: 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    gap: 2rem;
}

/* Logo */
.logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: #0d4fb5;
    flex-shrink: 0;
}

.logo-image {
    width: 50px;
    height: 50px;
    object-fit: contain;
}

.logo i {
    font-size: 1.75rem;
}

/* Perfil de usuario */
.user-profile {
    margin-left: auto;
    margin-right: 150px;
}

.profile-container {
    display: flex;
    align-items: center;
    gap: 10px;
    position: relative;
}

.profile-info {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    padding: 8px 12px;
    border-radius: 8px;
    transition: background-color 0.3s;
}

.profile-info:hover {
    background-color: #f5f5f5;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid #e0e0e0;
}

.user-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.user-details {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.user-name {
    font-weight: 600;
    font-size: 0.9rem;
    color: #333;
}

.user-role {
    font-size: 0.8rem;
    color: #666;
}

/* Dropdown */
.dropdown-toggle {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    padding: 8px;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.dropdown-toggle:hover {
    background-color: #f5f5f5;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    width: 200px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    padding: 8px 0;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.3s ease;
    z-index: 1001;
}

.dropdown-menu.active {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.dropdown-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    cursor: pointer;
    transition: background-color 0.2s;
    color: #333;
}

.dropdown-item:hover {
    background-color: #f5f5f5;
}

.dropdown-item i {
    width: 16px;
    text-align: center;
    color: #666;
}

.dropdown-divider {
    height: 1px;
    background-color: #e0e0e0;
    margin: 8px 0;
}

.dropdown-item.logout {
    color: #e74c3c;
}

.dropdown-item.logout i {
    color: #e74c3c;
}


/* Menú hamburguesa */
.menu-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    border-radius: 12px;
    width: 44px;
    height: 44px;
    color: #0d4fb5;
    font-size: 1.25rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    flex-shrink: 0;
}

.menu-toggle:hover {
    background: rgba(0, 157, 219, 0.1);
    transform: scale(1.05);
}

.mobile-search-toggle {
    display: none;
    background: #0d4fb5;
    border: none;
    border-radius: 12px;
    width: 44px;
    height: 44px;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.mobile-search-toggle:hover {
    background: #0d4fb5;
    transform: scale(1.05);
}

/* Sidebar */
.sidebar {
    position: fixed;
    top: 0;
    left: -320px;
    width: 320px;
    height: 100vh;
    background: white;
    box-shadow: 4px 0 30px rgba(0, 0, 0, 0.15);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1100;
    display: flex;
    flex-direction: column;
}

.sidebar.open {
    left: 0;
}

/* Header del sidebar */
.sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    background: white;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: #0d4fb5;
}

.sidebar-logo i {
    font-size: 1.5rem;
}

.sidebar-close {
    background: transparent;
    border: none;
    border-radius: 10px;
    width: 40px;
    height: 40px;
    color: #666;
    font-size: 1.25rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar-close:hover {
    background: rgba(0, 0, 0, 0.05);
    color: #333;
}

/* Contenido del sidebar */
.sidebar-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.sidebar-nav {
    flex: 1;
    padding: 1rem 0;
    overflow-y: auto;
}

.nav-section {
    margin-bottom: 2rem;
}

.nav-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0 1.5rem 0.75rem;
}

.nav-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.nav-list li {
    margin: 0.25rem 0;
}

.nav-link {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.875rem 1.5rem;
    text-decoration: none;
    color: #333;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 0;
    margin: 0;
    position: relative;
}

.nav-link:hover {
    background: rgba(0, 157, 219, 0.08);
    color: #009DDB;
}

.nav-link.active {
    background: linear-gradient(135deg, #009DDB 0%, #0077B6 100%);
    color: white;
    margin: 0 0.5rem;
    border-radius: 12px;
}

.nav-link.active::before {
    display: none;
}

.nav-icon {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    transition: transform 0.3s ease;
}

.nav-link:hover .nav-icon {
    transform: scale(1.1);
}

.nav-text {
    font-weight: 500;
    font-size: 0.95rem;
}

/* Footer del sidebar */
.sidebar-footer {
    padding: 1.5rem;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    background: white;
}

.logout-btn {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.875rem 1rem;
    background: transparent;
    border: none;
    border-radius: 12px;
    color: #dc2626;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    text-align: left;
}

.logout-btn:hover {
    background: rgba(220, 38, 38, 0.1);
}

/* Overlay */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1050;
    backdrop-filter: blur(2px);
}

.overlay.active {
    opacity: 1;
    visibility: visible;
}

/* Responsive */
@media (max-width: 1024px) {
    .app-header {
        padding: 0 1.5rem;
        gap: 1.5rem;
    }
}

@media (max-width: 768px) {
    .app-header {
        padding: 0 15px;
    }
    
    .menu-toggle {
        display: block; /* Visible en móvil */
    }
    
    .user-details {
        display: none;
    }
    
    .dropdown-menu {
        width: 180px;
    }
    
    .user-profile {
        margin-right: 10px;
    }
    
    /* En móvil, el sidebar se comporta como drawer */
    .sidebar.desktop-sidebar {
        left: -300px;
    }
    
    .sidebar.open {
        left: 0;
    }
    
    .sidebar-close {
        display: block; /* Visible en móvil */
    }
    
    .overlay {
        display: block; /* Visible en móvil */
    }
    
    .main-content.with-sidebar {
        margin-left: 0;
    }
}

@media (max-width: 480px) {
    .app-header {
        padding: 0 0.75rem;
    }

    .logo span {
        display: none;
    }
    
    .dropdown-menu {
        width: 160px;
    }
    
    .profile-info {
        padding: 6px;
    }
    
    .sidebar {
        width: 280px;
    }


    .sidebar-header {
        padding: 1.25rem;
    }

    .nav-link {
        padding: 0.75rem 1.25rem;
    }
}

/* Scrollbar personalizado */
.sidebar-nav::-webkit-scrollbar {
    width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
    background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.3);
}
</style>