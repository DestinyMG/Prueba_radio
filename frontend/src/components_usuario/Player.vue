<template>
  <div class="player">
    <div class="iframe-wrapper">
      <iframe 
        src="https://guri.tepuyserver.net/cp/widgets/player/single/?p=8096" 
        height="110" 
        width="100%" 
        scrolling="no" 
        style="border:none;" 
        allow="autoplay"
        class="sonic-player">
      </iframe>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps({
  currentTrack: {
    type: Object,
    default: null
  },
  isPlaying: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['play-pause'])

const audioElement = ref(null)
const volume = ref(0.7)
const defaultImage = 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=80'

const volumeIcon = computed(() => {
  if (volume.value === 0) {
    return 'fas fa-volume-mute'
  } else if (volume.value < 0.5) {
    return 'fas fa-volume-down'
  } else {
    return 'fas fa-volume-up'
  }
})

const handlePlayPause = () => {
  emit('play-pause')
}

const updateVolume = () => {
  if (audioElement.value) {
    audioElement.value.volume = volume.value
  }
}

const toggleMute = () => {
  volume.value = volume.value > 0 ? 0 : 0.7
  updateVolume()
}

watch(() => props.isPlaying, (newVal) => {
  if (!audioElement.value) return
  
  if (newVal) {
    audioElement.value.play().catch(console.error)
  } else {
    audioElement.value.pause()
  }
})

watch(() => props.currentTrack, () => {
  if (props.isPlaying && audioElement.value) {
    audioElement.value.play().catch(console.error)
  }
})

onMounted(() => {
  if (audioElement.value) {
    audioElement.value.volume = volume.value
  }
})
</script>

<style scoped>
.player {
  position: fixed;
  bottom: 0;
  left: 280px;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  z-index: 120; /* Mayor que el menú (110) pero no demasiado alto */
  border-top: 1px solid #E2E8F0;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(5px);
}

/* Contenedor principal que mantiene la altura del iframe */
.iframe-wrapper {
  width: 100%;
  height: 110px; /* Misma altura que el iframe */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* Iframe de Sonic Panel - lo centramos y aseguramos que sea responsive */
.sonic-player {
  height: 110px !important;
  max-width: 100%;
  display: block;
  pointer-events: auto; /* Asegurar que el iframe sea clickeable */
}

/* RESPONSIVE - Mantenemos la altura pero ajustamos el ancho */
@media (max-width: 1024px) {
  .player {
    left: 0;
    z-index: 120;
    /* En tablet, el reproductor va encima del contenido pero DEJA ESPACIO para el menú abajo */
    bottom: 80px; /* Altura del menú en tablet (80px) */
  }
  
  .iframe-wrapper {
    height: 110px; /* Mantenemos la altura */
  }
  
  .sonic-player {
    height: 110px !important;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .player {
    /* El reproductor va ARRIBA del menú pero DEJA ESPACIO para el menú */
    bottom: 70px; /* 70px es la altura del menú en 768px */
    z-index: 120;
  }
  
  .iframe-wrapper {
    height: 110px;
    padding: 0 5px;
  }
  
  .sonic-player {
    height: 110px !important;
    width: 100%;
    min-width: 320px;
  }
}

@media (max-width: 480px) {
  .player {
    /* El reproductor va ARRIBA del menú pero DEJA ESPACIO para el menú */
    bottom: 60px; /* 60px es la altura del menú en 480px */
    z-index: 120;
  }
  
  .iframe-wrapper {
    height: 110px;
    padding: 0 5px;
  }
  
  .sonic-player {
    height: 110px !important;
    width: 100%;
    min-width: 300px;
    transform: scale(0.95);
    transform-origin: center;
  }
}

@media (max-width: 375px) {
  .player {
    bottom: 60px; /* Mantener espacio para el menú */
  }
  
  .sonic-player {
    transform: scale(0.9);
    min-width: 280px;
  }
  
  .iframe-wrapper {
    padding: 0 2px;
  }
}

@media (max-width: 320px) {
  .player {
    bottom: 60px; /* Mantener espacio para el menú */
  }
  
  .sonic-player {
    transform: scale(0.85);
    min-width: 260px;
  }
}
</style>