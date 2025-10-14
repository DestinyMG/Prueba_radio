<template>
   <div class="sidebar">
    <div class="sidebar-content">
      <div class="menu-section">
        <div class="menu-title">Menú</div>
        <a 
          href="#" 
          class="menu-item" 
          :class="{ 'active': activeMenu === 'inicio' }" 
          @click.prevent="setActiveMenu('inicio')"
        >
          <i class="fas fa-home"></i>
          <span>Inicio</span>
        </a>
        <a 
          href="#" 
          class="menu-item" 
          :class="{ 'active': activeMenu === 'explorar' }" 
          @click.prevent="setActiveMenu('explorar')"
        >
          <i class="fas fa-search"></i>
          <span>Explorar</span>
        </a>
        <a 
          href="#" 
          class="menu-item" 
          :class="{ 'active': activeMenu === 'radio' }" 
          @click.prevent="setActiveMenu('radio')"
        >
          <i class="fas fa-broadcast-tower"></i>
          <span>Radio</span>
        </a>
        <a 
          href="#" 
          class="menu-item" 
          :class="{ 'active': activeMenu === 'programacion' }" 
          @click.prevent="setActiveMenu('programacion')"
        >
          <i class="fas fa-calendar-alt"></i>
          <span>Streaming</span>
        </a>
      </div>
       </div>
  </div>
</template>

<script setup>
const props = defineProps({
  activeMenu: {
    type: String,
    default: 'inicio'
  }
})

const emit = defineEmits(['set-active-menu'])

const setActiveMenu = (menu) => {
  emit('set-active-menu', menu)
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  background-color: rgba(255, 255, 255, 0.95);
  height: calc(100vh - 80px); /* Altura completa menos el header */
  position: fixed;
  left: 0;
  top: 80px; /* Comienza debajo del header */
  display: flex;
  flex-direction: column;
  z-index: 150; /* Menor que el header pero mayor que el contenido */
  border-right: 1px solid #E2E8F0;
  backdrop-filter: blur(5px);
  overflow: hidden;
}

.sidebar-content {
  padding: 20px 20px 70px;
  overflow-y: auto;
  height: 100%;
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 157, 219, 0.3) transparent;
  box-sizing: border-box;
}

.sidebar-content::-webkit-scrollbar {
  width: 6px;
  display: none;
}

.sidebar-content:hover::-webkit-scrollbar {
  display: block;
}

.sidebar-content::-webkit-scrollbar-track {
  background: transparent;
  margin: 10px 0;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background: rgba(0, 157, 219, 0.3);
  border-radius: 3px;
  transition: all 0.3s ease;
}

.sidebar-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 157, 219, 0.5);
}

.menu-section {
  margin-bottom: 20px;
}

.menu-section:last-child {
  margin-bottom: 0;
}

.menu-title {
  color: #5F6C7B;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 15px;
  padding-left: 8px;
  font-weight: 600;
}

.menu-item {
  color: #5F6C7B;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  text-decoration: none;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin: 6px 0;
  position: relative;
  overflow: hidden;
}

.menu-item:hover {
  color: #009DDB;
  background-color: rgba(0, 157, 219, 0.1);
}

.menu-item.active {
  color: #009DDB;
  background-color: rgba(0, 157, 219, 0.05);
  border-left: 3px solid #009DDB;
}

.menu-item i {
  margin-right: 12px;
  font-size: 18px;
  width: 24px;
  text-align: center;
  color: #009DDB;
}

.divider {
  border: none;
  height: 1px;
  background-color: #E2E8F0;
  margin: 24px 0;
}

@media (max-width: 1024px) {
  .sidebar {
    width: 100%;
    height: 80px;
    position: fixed;
    bottom: 0;
    left: 0;
    top: auto; /* En móvil va abajo */
    padding: 10px 15px;
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    z-index: 110;
    border-top: 1px solid #E2E8F0;
    border-right: none;
    border-radius: 0;
  }
  
  .sidebar-content {
    display: flex;
    flex-direction: row;
    padding: 0;
    width: 100%;
    height: 100%;
    align-items: center;
    overflow-y: hidden !important;
  }
  
  .menu-section {
    display: flex;
    margin-bottom: 0;
    margin-right: 15px;
    align-items: center;
  }
  
  .menu-title {
    display: none;
  }
  
  .divider {
    display: none;
  }
  
  .menu-item {
    flex: 0 0 auto;
    padding: 10px 15px;
    margin: 0 5px;
    height: auto;
    width: auto;
    border-radius: 8px;
    flex-direction: column;
    text-align: center;
  }
  
  .menu-item span {
    display: block !important;
    font-size: 11px;
    margin-top: 5px;
    white-space: nowrap;
  }
  
  .menu-item i {
    margin-right: 0;
    font-size: 18px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    height: 70px;
    padding: 8px 10px;
  }
  
  .menu-item {
    padding: 8px 10px;
    min-width: 60px;
  }
  
  .menu-item i {
    font-size: 16px;
  }
  
  .menu-item span {
    font-size: 10px;
  }
}

@media (max-width: 480px) {
  .sidebar {
    height: 60px;
  }
  
  .menu-item {
    padding: 6px 8px;
    min-width: 50px;
  }
  
  .menu-item i {
    font-size: 14px;
  }
  
  .menu-item span {
    font-size: 9px;
  }
}
</style>