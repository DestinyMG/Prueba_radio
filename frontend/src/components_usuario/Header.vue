<template>
  <header class="main-header" :class="{ 'scrolled': isScrolled }">
    <div class="logo">
      <img src="../assets/images/LogoFinal.png" alt="Moonlight Radio">
    </div>

    <div class="search-container">
      <div 
        class="search-bar" 
        :class="{ 'active': isSearchActive }" 
        @click="handleSearchClick"
      >
        <i class="fas fa-search"></i>
        <input 
          type="text" 
          placeholder="Buscar programas, artistas, géneros..."
          v-model="searchQuery"
          @focus="handleSearchFocus"
          @blur="handleSearchBlur"
          @input="handleSearchInput"
        >
        <div class="search-suggestions" v-if="showSuggestions && searchQuery">
          <div class="suggestion-item">
            <i class="fas fa-music"></i>
            <span>Programa: {{ searchQuery }}</span>
          </div>
          <div class="suggestion-item">
            <i class="fas fa-user"></i>
            <span>Artista: {{ searchQuery }}</span>
          </div>
          <div class="suggestion-item">
            <i class="fas fa-tag"></i>
            <span>Género: {{ searchQuery }}</span>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const isSearchActive = ref(false)
const searchQuery = ref('')
const showSuggestions = ref(false)
const isScrolled = ref(false)

const isMobile = computed(() => window.matchMedia('(max-width: 1024px)').matches)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const handleSearchClick = () => {
  if (isMobile.value) {
    isSearchActive.value = true
  }
}

const handleSearchFocus = () => {
  isSearchActive.value = true
  showSuggestions.value = true
}

const handleSearchBlur = () => {
  // Pequeño delay para permitir hacer clic en las sugerencias
  setTimeout(() => {
    showSuggestions.value = false
    if (isMobile.value && !searchQuery.value) {
      isSearchActive.value = false
    }
  }, 200)
}

const handleSearchInput = () => {
  if (searchQuery.value.length > 0) {
    showSuggestions.value = true
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.main-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between; /* Distribuye logo a izquierda y búsqueda a derecha */
  padding: 0 40px;
  z-index: 200;
  background: transparent;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(0px);
}

.main-header.scrolled {
  background: linear-gradient(135deg, #009DDB 0%, #007DB8 50%, #005A87 100%);
  backdrop-filter: blur(20px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.main-header .logo {
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.main-header .logo:hover {
  transform: scale(1.05);
}

.main-header .logo img {
  height: 80px;
  width: auto;
  object-fit: contain;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.search-container {
  display: flex;
  justify-content: flex-end; /* Alinea la búsqueda a la derecha */
  position: relative;
}

.search-bar {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  border: 2px solid transparent;
  border-radius: 50px;
  padding: 12px 24px;
  width: 400px; /* Ancho fijo para desktop */
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.1),
    inset 0 1px 2px rgba(255, 255, 255, 0.8);
}

.search-bar:focus-within {
  background: rgba(255, 255, 255, 1);
  border-color: #009DDB;
  box-shadow: 
    0 8px 30px rgba(0, 157, 219, 0.3),
    inset 0 1px 2px rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
}

.search-bar input {
  border: none;
  background: transparent;
  padding: 5px 10px;
  width: 100%;
  font-size: 16px;
  outline: none;
  color: #2D3748;
  font-weight: 500;
}

.search-bar input::placeholder {
  color: #718096;
  font-weight: 400;
}

.search-bar i {
  color: #009DDB;
  margin-right: 12px;
  font-size: 18px;
  transition: transform 0.3s ease;
}

.search-bar:focus-within i {
  transform: scale(1.1);
  color: #007DB8;
}

.search-suggestions {
  position: absolute;
  top: 100%;
  right: 0; /* Alineado a la derecha */
  width: 400px; /* Mismo ancho que la barra de búsqueda */
  background: rgba(255, 255, 255, 0.98);
  border-radius: 20px;
  margin-top: 8px;
  padding: 15px 0;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 8px 20px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  z-index: 1000;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.suggestion-item {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #2D3748;
}

.suggestion-item:hover {
  background: rgba(0, 157, 219, 0.1);
  color: #009DDB;
}

.suggestion-item i {
  margin-right: 12px;
  font-size: 14px;
  width: 16px;
  text-align: center;
}

/* Responsive */
@media (max-width: 1024px) {
  .main-header {
    padding: 0 20px;
  }
  
  .main-header .logo img {
    height: 70px;
  }
  
  .search-bar {
    width: 45px; /* Tamaño compacto en tablet */
    height: 45px;
    padding: 0;
    justify-content: center;
    overflow: hidden;
    transition: width 0.4s ease;
  }
  
  .search-bar input {
    display: none;
    opacity: 0;
    width: 0;
    transition: opacity 0.3s ease;
  }
  
  .search-bar i {
    margin-right: 0;
    font-size: 18px;
  }
  
  .search-bar.active {
    width: 280px; /* Se expande cuando está activa */
    padding: 12px 20px;
  }
  
  .search-bar.active input {
    display: block;
    opacity: 1;
    width: 100%;
  }
  
  .search-suggestions {
    width: 300px;
    right: 0;
  }
}

@media (max-width: 768px) {
  .main-header {
    padding: 0 15px;
    height: 70px;
  }
  
  .main-header .logo img {
    height: 60px;
  }
  
  .search-bar.active {
    width: 240px;
  }
  
  .search-suggestions {
    width: 260px;
  }
}

@media (max-width: 480px) {
  .main-header {
    height: 60px;
    padding: 0 10px;
  }
  
  .main-header .logo img {
    height: 50px;
  }
  
  .search-bar.active {
    width: 200px;
  }
  
  .search-suggestions {
    width: 220px;
  }
}
</style>