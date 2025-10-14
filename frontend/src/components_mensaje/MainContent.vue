<template>
  <div class="main-content">
    <!-- Reproductor y Noticias en la parte superior -->
    <div class="player-news-section">
      <div class="player-container">
        <div class="player-header">
          <div class="player-info">
            <i class="fas fa-broadcast-tower"></i>
            <span>En vivo ahora</span>
          </div>
          <div class="player-title">Nuestra Programación</div>
        </div>
        <!-- APARTADO INFORMATIVO EN LUGAR DEL IFRAME -->
        <div class="info-section">
          <div class="info-content">
            <div class="info-icon-container">
              <i class="fas fa-envelope"></i>
            </div>
            <div class="info-text">
              <h3 class="info-title">Mensaje importante</h3>
              <p class="info-description">Transmisión especial</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Panel de Noticias - MISMA ALTURA QUE EL REPRODUCTOR -->
      <div class="news-panel">
        <div class="news-header">
          <div class="news-title-container">
            <i class="fas fa-bullhorn"></i>
            <h3 class="news-title">Noticias Importantes</h3>
          </div>
          <div class="news-indicators">
            <span 
              v-for="(news, index) in newsItems" 
              :key="index"
              class="indicator"
              :class="{ active: currentNewsIndex === index }"
              @click="setCurrentNews(index)"
            ></span>
          </div>
        </div>
        
        <div class="news-content">
          <transition :name="transitionDirection" mode="out-in">
            <div class="news-item" :key="currentNewsIndex" v-if="currentNews">
              <div class="news-badge">{{ currentNews.label }}</div>
              <h4 class="news-message">{{ currentNews.message }}</h4>
              <div class="news-time">
                <a :href="currentNews.url" target="_blank" class="news-url">{{ currentNews.shortUrl }}</a>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
    
    <!-- Sección de Programación -->
    <div class="channel-section">
      <div class="section-header">
        <div class="section-title-container">
          <i class="fas fa-calendar-alt"></i>
          <h2 class="section-title">Programación Diaria</h2>
        </div>
      </div>
      
      <div class="carousel-container">
        <div class="carousel-nav left" @click="scrollLeft">
          <i class="fas fa-chevron-left"></i>
        </div>
        
        <div class="shows-container" ref="programmingCarousel">
          <!-- Programas Dinámicos desde BD -->
          <div 
            v-for="programa in programas" 
            :key="programa.id" 
            class="show-card"
          >
            <div class="show-image-container">
              <img 
                :src="programa.imagen_url || '/default-program.jpg'" 
                :alt="programa.nombre" 
                class="show-image"
                @error="handleImageError"
              >
              <div class="show-overlay"></div>
            </div>
            <div class="show-content">
              <div class="show-category">{{ programa.label }}</div>
              <h3 class="show-name">{{ programa.nombre }}</h3>
              <p class="show-description">{{ programa.descripcion }}</p>
              <div class="time-slot">
                <i class="far fa-clock"></i>
                <span>{{ formatTime(programa.hora_inicio) }} - {{ formatTime(programa.hora_fin) }}</span>
              </div>
              <!-- ELIMINADO: show-host section -->
            </div>
          </div>
        </div>
        
        <div class="carousel-nav right" @click="scrollRight">
          <i class="fas fa-chevron-right"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const programmingCarousel = ref(null)
const transitionDirection = ref('slide-next')

// Variables para el panel de noticias
const newsItems = ref([])
const currentNewsIndex = ref(0)

// Variables para programas desde BD
const programas = ref([])
const API_BASE_URL = 'http://localhost:8000/api4'

// Función para formatear hora de 24h a 12h (AM/PM)
const formatTime = (timeString) => {
  if (!timeString) return ''
  
  // Si ya está en formato AM/PM, retornar tal cual
  if (timeString.includes('AM') || timeString.includes('PM')) {
    return timeString
  }
  
  // Convertir de formato 24h a 12h
  const [hours, minutes] = timeString.split(':')
  let hour = parseInt(hours)
  const ampm = hour >= 12 ? 'PM' : 'AM'
  
  // Convertir a formato 12h
  hour = hour % 12
  hour = hour === 0 ? 12 : hour // 0 se convierte en 12
  
  return `${hour}:${minutes} ${ampm}`
}

// Cargar programas desde la API
const fetchProgramas = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/programas/`)
    if (response.ok) {
      const data = await response.json()
      // Filtrar solo programas activos
      programas.value = data.filter(programa => programa.is_active)
      console.log('Programas cargados:', programas.value) // Para debug
    }
  } catch (error) {
    console.error('Error cargando programas:', error)
  }
}

// Cargar noticias desde la API
const fetchNews = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/news/`)
    if (response.ok) {
      const data = await response.json()
      // Filtrar solo noticias activas
      newsItems.value = data.filter(news => news.is_active)
      console.log('Noticias cargadas:', newsItems.value) // Para debug
    }
  } catch (error) {
    console.error('Error cargando noticias:', error)
  }
}

// Noticia actual
const currentNews = computed(() => {
  if (newsItems.value.length === 0) return null
  return newsItems.value[currentNewsIndex.value]
})

// Manejo de errores de imagen
const handleImageError = (event) => {
  event.target.src = '/default-program.jpg'
}

// Funciones para el carrusel de noticias
const nextNews = () => {
  if (newsItems.value.length > 0) {
    transitionDirection.value = 'slide-next'
    currentNewsIndex.value = (currentNewsIndex.value + 1) % newsItems.value.length
  }
}

const setCurrentNews = (index) => {
  if (newsItems.value.length > 0) {
    transitionDirection.value = index > currentNewsIndex.value ? 'slide-next' : 'slide-prev'
    currentNewsIndex.value = index
  }
}

// Funciones para el carrusel de programas
const scrollLeft = () => {
  if (programmingCarousel.value) {
    const scrollAmount = window.innerWidth <= 768 ? 150 : 220
    programmingCarousel.value.scrollBy({
      left: -scrollAmount,
      behavior: 'smooth'
    })
  }
}

const scrollRight = () => {
  if (programmingCarousel.value) {
    const scrollAmount = window.innerWidth <= 768 ? 150 : 220
    programmingCarousel.value.scrollBy({
      left: scrollAmount,
      behavior: 'smooth'
    })
  }
}

// Auto-avance de noticias
let newsInterval

onMounted(async () => {
  // CARGAR DATOS AL INICIAR
  await fetchProgramas()
  await fetchNews()
  
  // Iniciar rotación solo si hay noticias
  if (newsItems.value.length > 0) {
    newsInterval = setInterval(nextNews, 5000) // Cambia cada 5 segundos
  }
  
  // Recargar datos cada 30 segundos
  setInterval(async () => {
    await fetchProgramas()
    await fetchNews()
  }, 30000)
})

onUnmounted(() => {
  if (newsInterval) {
    clearInterval(newsInterval)
  }
})

onUnmounted(() => {
  if (newsInterval) {
    clearInterval(newsInterval)
  }
})
</script>

<style scoped>
.main-content {
  margin: 0;
  padding: 120px 30px 20px 30px; /* Aumentado padding-top y reducido padding-bottom */
  width: 100%;
  min-height: calc(100vh - 140px); /* Ajuste para evitar espacio excesivo */
  position: relative;
}

/* Asegurar que el gradiente cubra todo el contenido */
.main-content::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
}

/* Sección de Reproductor y Noticias */
.player-news-section {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 25px;
  margin-bottom: 2rem;
  align-items: start;
}

/* Estilos del reproductor - ALTURA EXACTA */
.player-container {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 8px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  height: 172px; /* Altura total exacta del reproductor */
}

.player-container:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.2),
    0 10px 25px rgba(0, 0, 0, 0.15);
}

.player-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  background: rgba(255, 255, 255, 0.95);
  color: #1a202c;
  position: relative;
  overflow: hidden;
  border-bottom: 2px solid rgba(0, 157, 219, 0.2);
  height: 62px; /* Altura fija del header */
  box-sizing: border-box;
}

.player-info {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  font-weight: 600;
  color: #1a202c;
}

.player-info i {
  font-size: 20px;
  color: var(--primary);
}

.player-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a202c;
}

.sonic-player {
  border-radius: 0 0 20px 20px;
  background: rgba(255, 255, 255, 0.98);
  height: 110px; /* Altura fija del iframe */
}

.info-section {
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 0 0 20px 20px;
  padding: 0 25px;
}

.info-content {
  display: flex;
  align-items: center;
  gap: 20px;
  width: 100%;
  justify-content: center;
}

.info-icon-container {
  width: 60px;
  height: 60px;
  border-radius: 15px;
  background: linear-gradient(135deg, #009DDB 0%, #007DB8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0, 157, 219, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.8);
}

.info-icon-container i {
  font-size: 24px;
  color: white;
}

.info-text {
  text-align: left;
}

.info-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 5px 0;
}

.info-description {
  font-size: 14px;
  color: #718096;
  margin: 0;
  font-weight: 500;
}


/* Panel de Noticias - MISMA ALTURA EXACTA QUE EL REPRODUCTOR */
.news-panel {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 20px;
  padding: 0;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 8px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  height: 172px; /* MISMA ALTURA EXACTA QUE EL REPRODUCTOR */
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.news-panel:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.2),
    0 10px 25px rgba(0, 0, 0, 0.15);
}

.news-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  background: linear-gradient(135deg, #009DDB 0%, #007DB8 100%);
  color: white;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
  height: 62px; /* MISMA ALTURA QUE EL HEADER DEL REPRODUCTOR */
  box-sizing: border-box;
  flex-shrink: 0;
}

.news-title-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.news-title-container i {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
}

.news-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: white;
}

.news-indicators {
  display: flex;
  gap: 8px;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  background: rgba(255, 255, 255, 1);
  transform: scale(1.2);
}

.indicator:hover {
  background: rgba(255, 255, 255, 0.8);
}

.news-content {
  padding: 20px 25px;
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  height: 110px; /* MISMA ALTURA QUE EL IFRAME DEL REPRODUCTOR */
  box-sizing: border-box;
}

.news-item {
  width: 100%;
  text-align: center;
}

.news-badge {
  display: inline-block;
  background: linear-gradient(135deg, #E53E3E 0%, #C53030 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.news-message {
  font-size: 16px;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 8px;
  line-height: 1.3;
}

.news-time {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #718096;
  font-size: 13px;
  margin-bottom: 0;
  font-weight: 500;
}

.news-time i {
  color: var(--primary);
  font-size: 13px;
}

/* Transiciones para las noticias */
.slide-next-enter-active,
.slide-next-leave-active,
.slide-prev-enter-active,
.slide-prev-leave-active {
  transition: all 0.5s ease;
}

.slide-next-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-next-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-prev-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-prev-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* Estilos para la sección de canal */
.channel-section {
  margin-bottom: 30px; /* Reducido para menos espacio entre secciones */
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.1),
    0 5px 15px rgba(0, 0, 0, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  position: relative;
}

.channel-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: var(--gradient-primary);
  border-radius: 20px 20px 0 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px; /* Reducido para menos espacio */
  padding-bottom: 15px; /* Reducido para menos espacio */
  border-bottom: 2px solid rgba(0, 157, 219, 0.2);
}

.section-title-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.section-title-container i {
  color: var(--primary);
  font-size: 24px;
  background: rgba(0, 157, 219, 0.1);
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 157, 219, 0.2);
  border: 1px solid rgba(0, 157, 219, 0.2);
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.view-all {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--primary);
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  padding: 10px 16px;
  border-radius: 12px;
  background: rgba(0, 157, 219, 0.1);
  border: 1px solid rgba(0, 157, 219, 0.2);
}

.view-all:hover {
  background: var(--primary);
  color: white;
  transform: translateX(5px);
  box-shadow: 0 8px 25px rgba(0, 157, 219, 0.4);
}

/* Estilos del carrusel */
.carousel-container {
  position: relative;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  box-shadow: 
    0 10px 25px rgba(0, 0, 0, 0.15),
    0 4px 10px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.carousel-nav.right {
  right: -25px;
}

.carousel-nav.left {
  left: -25px;
}

.carousel-nav:hover {
  background: var(--primary);
  transform: translateY(-50%) scale(1.15);
  box-shadow: 0 15px 35px rgba(0, 157, 219, 0.5);
}

.carousel-nav:hover i {
  color: white;
  transform: scale(1.1);
}

.carousel-nav i {
  font-size: 18px;
  color: var(--primary);
  transition: all 0.3s ease;
}

.shows-container {
  display: flex;
  gap: 25px;
  overflow-x: auto;
  scroll-behavior: smooth;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  padding: 15px 5px;
  position: relative;
}

.shows-container::-webkit-scrollbar {
  display: none;
}

/* Estilos de las tarjetas de show */
.show-card {
  flex: 0 0 300px;
  scroll-snap-align: start;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.4s ease;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.8);
  cursor: pointer;
  box-shadow: 
    0 10px 25px rgba(0, 0, 0, 0.08),
    0 4px 8px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
}

.show-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.15),
    0 12px 25px rgba(0, 0, 0, 0.1);
  border-color: var(--primary);
}

.show-badge {
  position: absolute;
  top: 15px;
  left: 15px;
  background: var(--gradient-primary);
  color: white;
  padding: 6px 15px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  z-index: 5;
  box-shadow: 0 6px 20px rgba(0, 157, 219, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.show-image-container {
  position: relative;
  overflow: hidden;
  height: 180px;
}

.show-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.4s ease;
}

.show-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.2) 100%);
  transition: all 0.3s ease;
}

.show-card:hover .show-image {
  transform: scale(1.1);
}

.show-card:hover .show-overlay {
  background: linear-gradient(to bottom, transparent 0%, rgba(0, 157, 219, 0.15) 100%);
}

.show-content {
  padding: 25px;
}

.show-category {
  display: inline-block;
  background: rgba(0, 157, 219, 0.1);
  color: var(--primary);
  padding: 6px 14px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  border: 1px solid rgba(0, 157, 219, 0.2);
}

.show-name {
  font-weight: 800;
  margin-bottom: 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #1a202c;
  font-size: 20px;
  line-height: 1.3;
}

.show-description {
  color: #2d3748;
  font-size: 14px;
  margin-bottom: 20px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 42px;
}

.time-slot, .show-host {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2d3748;
  font-size: 14px;
  margin-bottom: 10px;
  font-weight: 500;
}

.time-slot i, .show-host i {
  color: var(--primary);
  font-size: 16px;
  width: 18px;
  opacity: 0.8;
}

/* Sección de próximos programas */
.upcoming-section {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.1),
    0 5px 15px rgba(0, 0, 0, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  position: relative;
  margin-bottom: 0; /* Eliminado margen inferior para evitar espacio excesivo */
}

.upcoming-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: var(--gradient-primary);
  border-radius: 20px 20px 0 0;
}

.upcoming-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.upcoming-item {
  display: flex;
  align-items: center;
  padding: 20px 25px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.upcoming-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.upcoming-item:hover {
  background: rgba(255, 255, 255, 1);
  border-color: var(--primary);
  transform: translateX(8px);
  box-shadow: 0 8px 25px rgba(0, 157, 219, 0.15);
}

.upcoming-item:hover::before {
  opacity: 1;
}

.upcoming-time {
  flex: 0 0 120px;
}

.upcoming-time .time {
  font-weight: 700;
  color: #1a202c;
  font-size: 16px;
  background: rgba(0, 157, 219, 0.1);
  padding: 8px 16px;
  border-radius: 12px;
  border: 1px solid rgba(0, 157, 219, 0.2);
}

.upcoming-info {
  flex: 1;
}

.upcoming-title {
  font-weight: 700;
  margin-bottom: 6px;
  color: #1a202c;
  font-size: 17px;
}

.upcoming-description {
  color: #2d3748;
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
}

.upcoming-category {
  flex: 0 0 90px;
  text-align: right;
}

.upcoming-category span {
  background: rgba(0, 157, 219, 0.1);
  color: var(--primary);
  padding: 6px 14px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  border: 1px solid rgba(0, 157, 219, 0.2);
}

/* Responsive */
@media (max-width: 1024px) {
  .player-news-section {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .news-panel {
    max-width: 100%;
  }
  
  .main-content {
    padding: 110px 25px 15px 25px; /* Ajustado para móviles */
  }
  
  .show-card {
    flex: 0 0 260px;
  }
  
  .carousel-nav {
    display: none;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 100px 20px 10px 20px; /* Ajustado para móviles */
  }

  .info-section {
    padding: 0 20px;
  }
  
  .info-content {
    gap: 15px;
  }
  
  .info-icon-container {
    width: 50px;
    height: 50px;
  }
  
  .info-icon-container i {
    font-size: 20px;
  }
  
  .info-title {
    font-size: 16px;
  }
  
  .info-description {
    font-size: 13px;
  }
  
  .player-news-section {
    gap: 15px;
  }
  
  .news-header {
    padding: 15px 20px;
  }
  
  .news-content {
    padding: 15px 20px;
  }
  
  .news-message {
    font-size: 15px;
  }
  
  .show-card {
    flex: 0 0 220px;
  }
  
  .channel-section, .upcoming-section {
    padding: 25px;
    margin-bottom: 25px; /* Reducido para móviles */
  }
  
  .section-title {
    font-size: 24px;
  }
  
  .section-title-container i {
    width: 45px;
    height: 45px;
    font-size: 20px;
  }
  
  .player-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
    padding: 5px 20px;
  }
  
  .upcoming-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
    padding: 18px 20px;
  }
  
  .upcoming-time, .upcoming-category {
    flex: none;
    width: 100%;
  }
  
  .upcoming-category {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 90px 15px 5px 15px; /* Ajustado para móviles pequeños */
  }
  
  .news-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .news-indicators {
    align-self: flex-end;
  }
  
  .show-card {
    flex: 0 0 200px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 18px;
  }
  
  .view-all {
    align-self: flex-start;
  }
  
  .channel-section, .upcoming-section {
    padding: 20px;
    margin-bottom: 20px; /* Reducido para móviles pequeños */
  }
  
  .section-title-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .section-title-container i {
    align-self: flex-start;
  }
}
</style>