<template>
  <div class="channel-section">
    <div class="section-header">
      <h2 class="section-title">{{ section.title }}</h2>
      <div class="view-all">Ver todo</div>
    </div>
    
    <div class="carousel-container">
      <div 
        class="carousel-nav left" 
        @click="scrollLeft" 
        @touchstart.prevent="scrollLeft"
      >
        <i class="fas fa-chevron-left"></i>
      </div>
      
      <div class="shows-container" ref="carouselRef">
        <ShowCard 
          v-for="show in section.shows"
          :key="show.id"
          :show="show"
          :is-playing="isPlaying && currentTrack?.id === show.id"
          @play="handlePlay"
        />
      </div>
      
      <div 
        class="carousel-nav right" 
        @click="scrollRight" 
        @touchstart.prevent="scrollRight"
      >
        <i class="fas fa-chevron-right"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ShowCard from './ShowCard.vue'

const props = defineProps({
  section: {
    type: Object,
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

const carouselRef = ref(null)

const scrollAmount = computed(() => window.innerWidth <= 768 ? 150 : 220)

const scrollLeft = () => {
  if (!carouselRef.value) return
  carouselRef.value.scrollBy({
    left: -scrollAmount.value,
    behavior: 'smooth'
  })
}

const scrollRight = () => {
  if (!carouselRef.value) return
  carouselRef.value.scrollBy({
    left: scrollAmount.value,
    behavior: 'smooth'
  })
}

const handlePlay = (show) => {
  emit('play-track', show)
}
</script>

<style scoped>
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

@media (max-width: 768px) {
  .channel-section {
    padding: 20px;
    margin-bottom: 30px;
  }
  
  .section-title {
    font-size: 20px;
  }
}
</style>