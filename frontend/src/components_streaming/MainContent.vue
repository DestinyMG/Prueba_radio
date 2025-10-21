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

        <!-- Sección de transmisión en vivo -->
        <div class="live-stream-section">
          <div class="stream-controls">
            <!-- Botón azul para iniciar (solo se muestra cuando no está streaming) -->
            <button v-if="!isLiveStreaming" @click="startLiveStream" :disabled="isConnecting" class="live-btn">
              <span class="btn-icon">🔵</span>
              <span class="btn-text">{{ getButtonText }}</span>
            </button>

            <!-- Indicador de streaming cuando está activo -->
            <div v-if="isLiveStreaming" class="live-indicator-display">
              <div class="live-badge-stream">
                <span class="live-pulse"></span>
                <span class="live-text">EN VIVO</span>
              </div>
              <div class="streaming-info">
                <div class="streaming-title">Transmisión en Vivo</div>
                <div class="streaming-desc">Kiero Radio - Streaming 24/7</div>
              </div>
              <div class="streaming-icon">📡</div>
            </div>
          </div>

          <!-- Estado de la conexión -->
          <div v-if="streamStatus" class="stream-status" :class="statusClass">
            {{ streamStatus }}
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
            <span v-for="(news, index) in newsItems" :key="index" class="indicator"
              :class="{ active: currentNewsIndex === index }" @click="setCurrentNews(index)"></span>
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
          <div v-for="programa in programas" :key="programa.id" class="show-card">
            <div class="show-image-container">
              <img :src="programa.imagen_url || '/default-program.jpg'" :alt="programa.nombre" class="show-image"
                @error="handleImageError">
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

// Variables para transmisión en vivo
const isLiveStreaming = ref(false)
const isConnecting = ref(false)
const streamStatus = ref('')
let ws = null
let audioContext = null
let isPlayingAudio = false
let lastPlayTime = 0

// Variables para el panel de noticias
const newsItems = ref([])
const currentNewsIndex = ref(0)
const transitionDirection = ref('slide-next')

// Variables para programas desde BD
const programas = ref([])
const API_BASE_URL = 'https://prueba-radio.onrender.com/api4'

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


// Computed para el botón de transmisión en vivo
const getButtonText = computed(() => {
  if (isConnecting.value) return 'Conectando...';
  return 'Escuchar Live';
})

const statusClass = computed(() => {
  if (streamStatus.value.includes('Error')) return 'error';
  if (streamStatus.value.includes('Conectado')) return 'success';
  if (streamStatus.value.includes('Escuchando')) return 'success';
  return 'info';
})

// Funciones para transmisión en vivo
const startLiveStream = () => {
  if (isLiveStreaming.value || isConnecting.value) return;

  isConnecting.value = true;
  isLiveStreaming.value = true;
  streamStatus.value = 'Conectando...';

  connectWebSocket();
}

const connectWebSocket = () => {
  try {
    ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
      console.log('✅ WebSocket CONECTADO');
      isConnecting.value = false;
      streamStatus.value = '✅ Conectado - Iniciando audio...';
      initializeAudioContext();
    };

    ws.onmessage = (event) => {
      if (!isLiveStreaming.value || !audioContext) return;

      if (event.data instanceof ArrayBuffer && event.data.byteLength > 0) {
        processRawAudio(event.data);
      }
    };

    ws.onclose = (event) => {
      console.log('WebSocket cerrado');
      isConnecting.value = false;

      if (event.code !== 1000) {
        streamStatus.value = 'Conexión perdida - Reconectando...';
        setTimeout(() => {
          if (isLiveStreaming.value) {
            startLiveStream();
          }
        }, 3000);
      } else {
        streamStatus.value = '';
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      streamStatus.value = 'Error de conexión - Reconectando...';
      isConnecting.value = false;

      setTimeout(() => {
        if (isLiveStreaming.value) {
          startLiveStream();
        }
      }, 5000);
    };

  } catch (error) {
    console.error('Error conectando WebSocket:', error);
    streamStatus.value = 'Error de conexión - Reconectando...';
    isConnecting.value = false;

    setTimeout(() => {
      if (isLiveStreaming.value) {
        startLiveStream();
      }
    }, 5000);
  }
};

const initializeAudioContext = () => {
  try {
    audioContext = new AudioContext({
      sampleRate: 48000
    });
    console.log('🔊 AudioContext listo');
  } catch (error) {
    console.error('Error inicializando audio:', error);
    streamStatus.value = 'Error en sistema de audio';
  }
};

const processRawAudio = (rawData) => {
  if (!audioContext) return;

  try {
    const int16Data = new Int16Array(rawData);
    const float32Data = new Float32Array(int16Data.length);

    for (let i = 0; i < int16Data.length; i++) {
      float32Data[i] = int16Data[i] / (int16Data[i] < 0 ? 0x8000 : 0x7FFF);
    }

    const smoothedData = smoothAudio(float32Data);
    const audioBuffer = audioContext.createBuffer(1, smoothedData.length, 48000);
    audioBuffer.getChannelData(0).set(smoothedData);

    const now = audioContext.currentTime;
    const playTime = Math.max(lastPlayTime, now);

    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start(playTime);

    lastPlayTime = playTime + audioBuffer.duration;

    if (!isPlayingAudio) {
      isPlayingAudio = true;
      console.log('🎵 Audio en vivo reproduciéndose');
      // Limpiar mensaje de estado después de empezar a reproducir
      setTimeout(() => {
        streamStatus.value = '';
      }, 2000);
    }

  } catch (error) {
    console.log('Error procesando audio:', error);
  }
};

const smoothAudio = (input) => {
  const output = new Float32Array(input.length);

  for (let i = 0; i < input.length; i++) {
    if (i === 0 || i === input.length - 1) {
      output[i] = input[i];
    } else {
      output[i] = (input[i - 1] + input[i] + input[i + 1]) / 3;
    }
  }

  return output;
};

onUnmounted(() => {
  if (newsInterval) {
    clearInterval(newsInterval)
  }
  if (ws) {
    ws.close();
  }
  if (audioContext) {
    audioContext.close();
  }
})
</script>

<style scoped>
.main-content {
  margin: 0;
  padding: 120px 30px 20px 30px;
  width: 100%;
  min-height: calc(100vh - 140px);
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
  height: 172px;
  /* Altura total exacta del reproductor */
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
  height: 62px;
  /* Altura fija del header */
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

/* Sección de transmisión en vivo */
.live-stream-section {
  height: 110px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 0 0 20px 20px;
  padding: 15px 25px;
  gap: 12px;
}

.stream-controls {
  display: flex;
  align-items: center;
  gap: 20px;
  justify-content: center;
  width: 100%;
}

/* Botón de Live Streaming */
.live-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.8);
}

.live-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.live-btn:disabled {
  background: #6b7280;
  cursor: not-allowed;
  opacity: 0.7;
  transform: none;
}

.btn-icon {
  font-size: 16px;
}

.btn-text {
  white-space: nowrap;
}

/* Display de streaming en vivo */
.live-indicator-display {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 20px;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
  border-radius: 16px;
  border: 2px solid rgba(239, 68, 68, 0.2);
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
}

.live-badge-stream {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.live-pulse {
  width: 10px;
  height: 10px;
  background: #ef4444;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }

  70% {
    transform: scale(1);
    box-shadow: 0 0 0 8px rgba(239, 68, 68, 0);
  }

  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}

.live-text {
  font-size: 13px;
  font-weight: 700;
  color: #ef4444;
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.streaming-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.streaming-title {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
  white-space: nowrap;
}

.streaming-desc {
  font-size: 13px;
  color: #6b7280;
  white-space: nowrap;
}

.streaming-icon {
  font-size: 24px;
  animation: bounce 2s infinite;
}

@keyframes bounce {

  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateY(0);
  }

  40% {
    transform: translateY(-4px);
  }

  60% {
    transform: translateY(-2px);
  }
}

/* Estado de la conexión */
.stream-status {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
  width: 100%;
  max-width: 300px;
}

.stream-status.info {
  background-color: #dbeafe;
  color: #1e40af;
  border: 1px solid #93c5fd;
}

.stream-status.success {
  background-color: #dcfce7;
  color: #166534;
  border: 1px solid #86efac;
}

.stream-status.error {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
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
  height: 172px;
  /* MISMA ALTURA EXACTA QUE EL REPRODUCTOR */
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
  height: 62px;
  /* MISMA ALTURA QUE EL HEADER DEL REPRODUCTOR */
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
  height: 110px;
  /* MISMA ALTURA QUE EL IFRAME DEL REPRODUCTOR */
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
  margin-bottom: 30px;
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
  margin-bottom: 25px;
  padding-bottom: 15px;
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

.time-slot,
.show-host {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2d3748;
  font-size: 14px;
  margin-bottom: 10px;
  font-weight: 500;
}

.time-slot i,
.show-host i {
  color: var(--primary);
  font-size: 16px;
  width: 18px;
  opacity: 0.8;
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
    padding: 110px 25px 15px 25px;
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
    padding: 100px 20px 10px 20px;
  }

  .live-stream-section {
    padding: 15px 20px;
    gap: 10px;
  }

  .stream-controls {
    flex-direction: column;
    gap: 15px;
  }

  .live-indicator-display {
    padding: 10px 15px;
    gap: 12px;
  }

  .streaming-title {
    font-size: 14px;
  }

  .streaming-desc {
    font-size: 12px;
  }

  .streaming-icon {
    font-size: 20px;
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

  .channel-section {
    padding: 25px;
    margin-bottom: 25px;
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
}

@media (max-width: 480px) {
  .main-content {
    padding: 90px 15px 5px 15px;
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

  .channel-section {
    padding: 20px;
    margin-bottom: 20px;
  }

  .section-title-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .section-title-container i {
    align-self: flex-start;
  }

  .live-btn {
    padding: 8px 16px;
    font-size: 12px;
  }

  .live-indicator-display {
    padding: 8px 12px;
    gap: 10px;
  }

  .streaming-title {
    font-size: 13px;
  }

  .streaming-desc {
    font-size: 11px;
  }

  .streaming-icon {
    font-size: 18px;
  }
}
</style>