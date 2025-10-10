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
        :class="{ 'hidden': !canScrollLeft }"
      >
        <i class="fas fa-chevron-left"></i>
      </div>
      
      <div class="shows-wrapper">
        <div class="shows-container" ref="carouselRef">
          <ShowCard 
            v-for="show in section.shows"
            :key="show.id"
            :show="show"
            :is-playing="isPlaying && currentTrack?.id === show.id"
            @play="handlePlay"
          />
        </div>
      </div>
      
      <div 
        class="carousel-nav right" 
        @click="scrollRight" 
        :class="{ 'hidden': !canScrollRight }"
      >
        <i class="fas fa-chevron-right"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
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
const canScrollLeft = ref(false)
const canScrollRight = ref(false)

// Calcular cuántas tarjetas caben en la vista
const getVisibleCardsCount = () => {
  if (typeof window === 'undefined') return 3
  if (window.innerWidth <= 768) return 2
  if (window.innerWidth <= 1024) return 3
  return 4
}

const scrollAmount = () => {
  const visibleCards = getVisibleCardsCount()
  const cardWidth = window.innerWidth <= 768 ? 150 : 220
  return cardWidth * visibleCards
}

const updateNavigation = () => {
  if (!carouselRef.value) return
  
  const { scrollLeft, scrollWidth, clientWidth } = carouselRef.value
  canScrollLeft.value = scrollLeft > 10
  canScrollRight.value = scrollLeft < scrollWidth - clientWidth - 10
}

const scrollLeft = () => {
  if (!carouselRef.value || !canScrollLeft.value) return
  carouselRef.value.scrollBy({
    left: -scrollAmount(),
    behavior: 'smooth'
  })
}

const scrollRight = () => {
  if (!carouselRef.value || !canScrollRight.value) return
  carouselRef.value.scrollBy({
    left: scrollAmount(),
    behavior: 'smooth'
  })
}

const handlePlay = (show) => {
  emit('play-track', show)
}

const handleScroll = () => {
  updateNavigation()
}

onMounted(() => {
  if (carouselRef.value) {
    carouselRef.value.addEventListener('scroll', handleScroll)
    setTimeout(updateNavigation, 100)
  }
})

onUnmounted(() => {
  if (carouselRef.value) {
    carouselRef.value.removeEventListener('scroll', handleScroll)
  }
})
</script>

<style scoped>
.channel-section {
  margin-bottom: 40px;
  background-color: rgba(255, 255, 255, 0.95);
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 125, 184, 0.08);
  border: 1px solid rgba(226, 232, 240, 0.8);
  backdrop-filter: blur(10px);
  max-width: 100%;
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.view-all {
  color: #009DDB;
  font-size: 0.875rem;
  cursor: pointer;
  transition: color 0.3s ease;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 5px;
}

.view-all:hover {
  color: #007DB8;
}

.carousel-container {
  position: relative;
  width: 100%;
}

.shows-wrapper {
  overflow: hidden;
  width: 100%;
  border-radius: 12px;
  mask-image: linear-gradient(
    to right,
    transparent 0%,
    black 20px,
    black calc(100% - 20px),
    transparent 100%
  );
}

.shows-container {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none;
  padding: 10px 20px;
  scroll-padding: 0 20px;
}

.shows-container::-webkit-scrollbar {
  display: none;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(226, 232, 240, 0.8);
  transition: all 0.3s ease;
  opacity: 1;
}

.carousel-nav.right {
  right: 10px;
}

.carousel-nav.left {
  left: 10px;
}

.carousel-nav.hidden {
  opacity: 0;
  pointer-events: none;
  transform: translateY(-50%) scale(0.8);
}

.carousel-nav:not(.hidden):hover {
  background: #009DDB;
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 157, 219, 0.3);
}

.carousel-nav i {
  font-size: 16px;
  color: #009DDB;
  transition: color 0.3s ease;
}

.carousel-nav:not(.hidden):hover i {
  color: white;
}

/* Responsive */
@media (max-width: 1024px) {
  .channel-section {
    padding: 20px;
    margin-bottom: 30px;
  }
  
  .section-title {
    font-size: 1.3rem;
  }
  
  .shows-container {
    gap: 15px;
    padding: 10px 15px;
  }
  
  .carousel-nav {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 768px) {
  .channel-section {
    padding: 16px;
    margin-bottom: 25px;
  }
  
  .section-header {
    margin-bottom: 20px;
  }
  
  .section-title {
    font-size: 1.2rem;
  }
  
  .shows-container {
    gap: 12px;
    padding: 8px 12px;
  }
  
  .carousel-nav {
    width: 36px;
    height: 36px;
  }
  
  .carousel-nav.right {
    right: 5px;
  }
  
  .carousel-nav.left {
    left: 5px;
  }
}

@media (max-width: 480px) {
  .channel-section {
    padding: 12px;
    margin-bottom: 20px;
  }
  
  .section-title {
    font-size: 1.1rem;
  }
  
  .shows-container {
    gap: 10px;
    padding: 6px 10px;
  }
}
</style>