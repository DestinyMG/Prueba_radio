<template>
  <div class="player">
    <!-- Imagen del track o indicador de aviso -->
    <img v-if="!avisoAudio?.activo" 
         :src="currentTrack?.image || 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=80'" 
         alt="" class="player-image">
    <div v-else class="aviso-indicator">
      ⚠️
    </div>
    
    <div class="player-info">
      <div class="player-title">
        {{ avisoAudio?.activo ? 'Mensaje Importante' : currentTrack?.title || 'Selecciona una canción' }}
      </div>
      <div class="player-channel">
        {{ avisoAudio?.activo ? 'Transmisión Especial' : currentTrack?.description || 'Kiero Radio' }}
      </div>
    </div>
    
    
    <!-- Audio para música normal -->
    <audio ref="audioElement" loop v-if="!avisoAudio?.activo">
      <source :src="currentTrack?.audio || 'https://assets.mixkit.co/sfx/preview/mixkit-synth-pop-808-loop-192.mp3'" type="audio/mpeg">
    </audio>
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
  },
  avisoAudio: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['play-pause'])

const audioElement = ref(null)
const volume = ref(0.7)

const volumeIcon = computed(() => {
  if (volume.value === 0) {
    return 'fas fa-volume-mute'
  } else if (volume.value < 0.5) {
    return 'fas fa-volume-down'
  } else {
    return 'fas fa-volume-up'
  }
})

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
  if (!audioElement.value || props.avisoAudio?.activo) return
  
  if (newVal) {
    audioElement.value.play().catch(() => {})
  } else {
    audioElement.value.pause()
  }
})

watch(() => props.currentTrack, () => {
  if (props.isPlaying && audioElement.value && !props.avisoAudio?.activo) {
    audioElement.value.play().catch(() => {})
  }
})

watch(() => props.avisoAudio, (newAviso) => {
  // Si hay un aviso activo, pausar la música normal
  if (newAviso?.activo && audioElement.value) {
    audioElement.value.pause()
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
  height: 110px;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  padding: 0 20px;
  z-index: 100;
  border-top: 1px solid #E2E8F0;
  transition: all 0.3s ease;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(5px);
}

.player-image {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  margin-right: 15px;
  object-fit: cover;
  border: 1px solid #E2E8F0;
}

.aviso-indicator {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
}

.player-info {
  flex: 1;
  min-width: 0;
}

.player-title {
  font-weight: 600;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #2D3748;
}

.player-channel {
  color: #5F6C7B;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-controls {
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 0 20px;
}

.player-btn {
  background: none;
  border: none;
  color: #5F6C7B;
  font-size: 16px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.player-btn:hover {
  color: #009DDB;
  background-color: rgba(0, 157, 219, 0.1);
}

.player-main-btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #009DDB, #007DB8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.player-main-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 157, 219, 0.3);
}

.volume-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: 10px;
}

.volume-icon {
  cursor: pointer;
  font-size: 16px;
  color: #5F6C7B;
  transition: color 0.3s ease;
}

.volume-icon:hover {
  color: #009DDB;
}

.volume-slider {
  width: 80px;
  height: 4px;
  -webkit-appearance: none;
  background: rgba(0, 125, 184, 0.2);
  border-radius: 2px;
  outline: none;
  opacity: 0.7;
  transition: opacity 0.2s, width 0.3s ease;
}

.volume-slider:hover {
  opacity: 1;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #009DDB;
  cursor: pointer;
}

.volume-controls:hover .volume-slider {
  width: 100px;
}

@media (max-width: 1024px) {
  .player {
    left: 0;
    bottom: 80px;
  }
}

@media (max-width: 768px) {
  .player {
    bottom: 70px;
    height: 60px;
  }
}

@media (max-width: 480px) {
  .player {
    bottom: 60px;
  }
  
  .player-image, .aviso-indicator {
    width: 40px !important;
    height: 40px !important;
    margin-right: 8px !important;
  }
  
  .player-info {
    min-width: 0;
    overflow: hidden;
  }
  
  .player-title {
    font-size: 12px !important;
  }
  
  .player-channel {
    font-size: 10px !important;
  }
  
  .player-controls {
    gap: 5px !important;
    margin: 0 5px !important;
  }
  
  .player-btn, .player-main-btn {
    width: 28px !important;
    height: 28px !important;
    font-size: 12px !important;
  }
  
  .volume-controls {
    display: none;
  }
}
</style>