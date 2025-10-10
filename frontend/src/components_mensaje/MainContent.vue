<template>
  <div class="main-content">
   
      <!-- Sección de Noticias -->
    <div class="news-section">
      <div class="news-container">
        <div class="news-image">
          <img src="../assets/images/chapte.jpg" 
               alt="Nueva función de la aplicación">
        </div>
        <div class="news-content">
          <div class="news-meta">
            <span class="news-time">10:30 AM</span>
            <span class="news-date">15 Nov 2023</span>
          </div>
          <h2 class="news-title">Nuevo Mensaje</h2>
        </div>
      </div>
    </div>

   
    <!-- Sección de Música -->
    <div class="channel-section">
      <div class="section-header">
        <h2 class="section-title">Música</h2>
        <div class="view-all">Ver todo</div>
      </div>
      
      <div class="carousel-container">
        <div class="carousel-nav left" @click="scrollLeft">
          <i class="fas fa-chevron-left"></i>
        </div>
        
        <div class="shows-container" ref="musicCarousel">
          <!-- Canal 1 -->
          <div class="show-card" @click="playChannel('chill-hits', 'Música Relajante', 'Ritmos suaves para tu día', 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80')">
            <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80" 
                 alt="Música Relajante" class="show-image">
            <div class="show-content">
              <h3 class="show-name">Música Relajante</h3>
              <p class="show-description">Ritmos suaves para tu día</p>
              <div class="play-btn" @click.stop="playChannel('chill-hits', 'Música Relajante', 'Ritmos suaves para tu día', 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80')">
                <i class="fas fa-play"></i>
              </div>
            </div>
          </div>
          
          <!-- Canal 2 -->
          <div class="show-card" @click="playChannel('top-hits', 'Éxitos del Momento', 'Lo más popular ahora', 'https://images.unsplash.com/photo-1496293455970-f8581aae0e3b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80')">
            <img src="https://images.unsplash.com/photo-1496293455970-f8581aae0e3b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80" 
                 alt="Éxitos del Momento" class="show-image">
            <div class="show-content">
              <h3 class="show-name">Éxitos del Momento</h3>
              <p class="show-description">Lo más popular ahora</p>
              <div class="play-btn" @click.stop="playChannel('top-hits', 'Éxitos del Momento', 'Lo más popular ahora', 'https://images.unsplash.com/photo-1496293455970-f8581aae0e3b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80')">
                <i class="fas fa-play"></i>
              </div>
            </div>
          </div>
          
          <!-- Canal 3 -->
          <div class="show-card" @click="playChannel('jazz-vibes', 'Vibraciones Jazz', 'Melodías suaves de jazz', 'https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80')">
            <img src="https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80" 
                 alt="Vibraciones Jazz" class="show-image">
            <div class="show-content">
              <h3 class="show-name">Vibraciones Jazz</h3>
              <p class="show-description">Melodías suaves de jazz</p>
              <div class="play-btn" @click.stop="playChannel('jazz-vibes', 'Vibraciones Jazz', 'Melodías suaves de jazz', 'https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80')">
                <i class="fas fa-play"></i>
              </div>
            </div>
          </div>
          
          <!-- Canal 4 -->
          <div class="show-card" @click="playChannel('rock-nation', 'Nación Rock', 'Lo mejor del rock', 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80')">
            <img src="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80" 
                 alt="Nación Rock" class="show-image">
            <div class="show-content">
              <h3 class="show-name">Nación Rock</h3>
              <p class="show-description">Lo mejor del rock</p>
              <div class="play-btn" @click.stop="playChannel('rock-nation', 'Nación Rock', 'Lo mejor del rock', 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80')">
                <i class="fas fa-play"></i>
              </div>
            </div>
          </div>
        </div>
        
        <div class="carousel-nav right" @click="scrollRight">
          <i class="fas fa-chevron-right"></i>
        </div>
      </div>
    </div>

    

    <!-- Otras secciones dinámicas -->
    <ChannelSection 
      v-for="section in sections"
      :key="section.id"
      :section="section"
      :current-track="currentTrack"
      :is-playing="isPlaying"
      @play-track="handlePlayTrack"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChannelSection from './ChannelSection.vue'

const props = defineProps({
  sections: {
    type: Array,
    required: true
  },
  currentTrack: {
    type: Object,
    default: null
  },
  isPlaying: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['play-track'])

const musicCarousel = ref(null)

// Función para reproducir canal
const playChannel = (channelId, title, description, image) => {
  const track = {
    id: channelId,
    title: title,
    description: description,
    image: image,
    audio: 'https://assets.mixkit.co/sfx/preview/mixkit-synth-pop-808-loop-192.mp3'
  }
  emit('play-track', track)
}

// Funciones para el carrusel
const scrollLeft = () => {
  if (musicCarousel.value) {
    const scrollAmount = window.innerWidth <= 768 ? 150 : 220
    musicCarousel.value.scrollBy({
      left: -scrollAmount,
      behavior: 'smooth'
    })
  }
}

const scrollRight = () => {
  if (musicCarousel.value) {
    const scrollAmount = window.innerWidth <= 768 ? 150 : 220
    musicCarousel.value.scrollBy({
      left: scrollAmount,
      behavior: 'smooth'
    })
  }
}

const handlePlayTrack = (track) => {
  emit('play-track', track)
}
</script>

<style scoped>
.main-content {
  margin-left: 280px;
  margin-top: 80px;
  padding: 40px;
  width: calc(100% - 280px);
  min-height: calc(100vh - 80px);
  transition: margin-left 0.3s ease;
}

.news-section {
  margin-bottom: 2rem;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.news-container {
  display: flex;
  align-items: center;
  padding: 0;
}

.news-image {
  flex: 0 0 40%;
  max-width: 40%;
}

.news-image img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  display: block;
}

.news-content {
  flex: 1;
  padding: 1.5rem 2rem;
  color: white;
}

.news-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.75rem;
  font-size: 0.85rem;
  opacity: 0.8;
}

.news-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
  line-height: 1.3;
}

.news-description {
  line-height: 1.6;
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

.news-button {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.news-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* Estilos para la sección de canal */
.channel-section {
  margin-bottom: 50px;
  background-color: rgba(255, 255, 255, 0.95);
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 125, 184, 0.1);
  border: 1px solid #E2E8F0;
  backdrop-filter: blur(3px);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #E2E8F0;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #2D3748;
}

.view-all {
  color: #009DDB;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.3s ease;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.view-all:hover {
  color: #007DB8;
}

.view-all i {
  margin-left: 5px;
  font-size: 12px;
}

/* Estilos del carrusel */
.carousel-container {
  position: relative;
}

.carousel-nav {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.3s ease;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 100%);
}

.carousel-nav.right {
  right: 0;
  background: linear-gradient(270deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 100%);
}

.carousel-nav.left {
  left: 0;
}

.carousel-nav:hover {
  opacity: 1;
}

.carousel-nav i {
  font-size: 20px;
  color: #009DDB;
  background-color: #FAFBFD;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 125, 184, 0.1);
  border: 1px solid #E2E8F0;
}

.carousel-nav:hover i {
  background-color: #009DDB;
  color: #FAFBFD;
  transform: scale(1.1);
}

.shows-container {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  scroll-behavior: smooth;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  padding: 10px 0;
  position: relative;
}

.shows-container::-webkit-scrollbar {
  display: none;
}

/* Estilos de las tarjetas de show */
.show-card {
  flex: 0 0 220px;
  scroll-snap-align: start;
  background-color: rgba(255, 255, 255, 0.98);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  border: 1px solid #E2E8F0;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 125, 184, 0.1);
}

.show-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 125, 184, 0.15);
  border-color: #009DDB;
}

.show-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.show-card:hover .show-image {
  transform: scale(1.03);
}

.show-content {
  padding: 15px;
}

.show-name {
  font-weight: 600;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #2D3748;
}

.show-description {
  color: #5F6C7B;
  font-size: 13px;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.play-btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #009DDB, #007DB8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: auto;
  opacity: 1;
  transform: translateY(10px);
  color: white;
}

.show-card:hover .play-btn {
  opacity: 1;
  transform: translateY(0);
}

.play-btn:hover {
  transform: scale(1.05) translateY(0) !important;
  box-shadow: 0 0 15px rgba(0, 157, 219, 0.3);
}

/* Responsive */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
    margin-bottom: 140px;
    padding: 90px 20px 30px;
    width: 100%;
    margin-top: 80px;
  }
  
  .show-card {
    flex: 0 0 180px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-bottom: 100px;
    padding: 80px 15px 20px;
  }
  
  .show-card {
    flex: 0 0 150px;
  }
  
  .channel-section {
    padding: 20px;
    margin-bottom: 30px;
  }
  
  .section-title {
    font-size: 20px;
  }

  .news-container {
    flex-direction: column;
  }
  
  .news-image {
    flex: 0 0 100%;
    max-width: 100%;
  }
  
  .news-image img {
    height: 200px;
  }
  
  .news-content {
    padding: 1.5rem;
  }
  
  .news-title {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-bottom: 90px;
  }
  
  .show-card {
    flex: 0 0 130px;
  }
}
</style>