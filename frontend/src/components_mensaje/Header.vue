<template>
  <header class="main-header">
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
          placeholder="Buscar shows, canciones..."
          v-model="searchQuery"
          @focus="handleSearchFocus"
          @blur="handleSearchBlur"
        >
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'

const isSearchActive = ref(false)
const searchQuery = ref('')

const isMobile = computed(() => window.matchMedia('(max-width: 1024px)').matches)

const handleSearchClick = () => {
  if (isMobile.value) {
    isSearchActive.value = true
  }
}

const handleSearchFocus = () => {
  isSearchActive.value = true
}

const handleSearchBlur = () => {
  if (isMobile.value && !searchQuery.value) {
    isSearchActive.value = false
  }
}
</script>

<style scoped>
.main-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  background: #009DDB;
  display: flex;
  align-items: center;
  padding: 0 40px;
  z-index: 200; /* Aumentado a 200 para que esté por encima del sidebar */
  border-bottom: 1px solid #E2E8F0;
  backdrop-filter: blur(5px);
}

.main-header .logo {
  display: flex;
  align-items: center;
  margin-right: 40px;
}

.main-header .logo img {
  height: 70px; /* Aumentado a 70px para logo más grande */
  width: auto;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.main-header .logo:hover img {
  transform: scale(1.05);
}

.search-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #FAFBFD;
  border: 1px solid #E2E8F0;
  border-radius: 25px;
  padding: 10px 20px;
  width: 100%;
  transition: all 0.3s ease;
}

.search-bar:focus-within {
  border-color: #009DDB;
  box-shadow: 0 0 0 3px rgba(0, 157, 219, 0.2);
}

.search-bar input {
  border: none;
  background: transparent;
  padding: 5px 10px;
  width: 100%;
  font-size: 14px;
  outline: none;
  color: #2D3748;
}

.search-bar i {
  color: #5F6C7B;
  margin-right: 10px;
}

@media (max-width: 1024px) {
  .main-header {
    padding: 0 20px;
  }
  
  .main-header .logo {
    margin-right: 20px;
  }
  
  .main-header .logo img {
    height: 60px; /* Logo más grande en tablet también */
  }
  
  .search-container {
    position: relative;
    width: auto;
    margin: 0;
    margin-left: auto;
  }
  
  .search-bar {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    padding: 0;
    justify-content: center;
    overflow: hidden;
    transition: width 0.3s ease;
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
    width: 200px;
    padding: 10px 15px;
  }
  
  .search-bar.active input {
    display: block;
    opacity: 1;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .main-header {
    padding: 0 15px;
    height: 70px;
  }
  
  .main-header .logo {
    margin-right: 15px;
  }
  
  .main-header .logo img {
    height: 50px;
  }
}

@media (max-width: 480px) {
  .main-header {
    height: 60px;
    padding: 0 10px;
  }
  
  .main-header .logo {
    margin-right: 10px;
  }
  
  .main-header .logo img {
    height: 45px;
  }
  
  .search-bar.active {
    width: 150px;
  }
}
</style>