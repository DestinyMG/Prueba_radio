<template>
  <div class="player">
    <!-- Imagen del track o indicador de aviso -->
    <img v-if="!avisoAudio?.activo && !isLiveStreaming" 
         :src="currentTrack?.image || 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?ixlib=rb-1.2.1&auto=format&fit=crop&w=100&q=80'" 
         alt="" class="player-image">
    <div v-else-if="avisoAudio?.activo" class="aviso-indicator">
      ⚠️
    </div>
    <div v-else class="live-indicator">
      🔴 LIVE
    </div>
    
    <div class="player-info">
      <div class="player-title">
        {{ avisoAudio?.activo ? 'Mensaje Importante' : 
             isLiveStreaming ? '🎧 Audio en Vivo HD' : 
             currentTrack?.title || 'Selecciona una canción' }}
      </div>
      <div class="player-channel">
        {{ avisoAudio?.activo ? 'Transmisión Especial' : 
             isLiveStreaming ? 'Transmisión en Directo - Kiero Radio' : 
             currentTrack?.description || 'Kiero Radio' }}
        <span v-if="streamStatus" class="status" :class="statusClass">{{ streamStatus }}</span>
      </div>
    </div>
    
    <!-- Audio para música normal -->
    <audio ref="audioElement" loop v-if="!avisoAudio?.activo && !isLiveStreaming">
      <source :src="currentTrack?.audio || 'https://assets.mixkit.co/sfx/preview/mixkit-synth-pop-808-loop-192.mp3'" type="audio/mpeg">
    </audio>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

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

// Variables para transmisión en vivo
const isLiveStreaming = ref(false)
const streamStatus = ref('')
let ws = null
let audioContext = null
let isPlayingAudio = false
let lastPlayTime = 0

const statusClass = computed(() => {
  if (streamStatus.value.includes('Error')) return 'error';
  if (streamStatus.value.includes('Conectado')) return 'success';
  if (streamStatus.value.includes('Escuchando')) return 'success';
  return 'info';
})

// Iniciar transmisión en vivo automáticamente
const startLiveStream = () => {
  if (isLiveStreaming.value) return;
  
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
      streamStatus.value = '✅ Conectado - Iniciando audio HD...';
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
      isLiveStreaming.value = false;
      
      if (event.code !== 1000) {
        streamStatus.value = 'Conexión perdida - Reconectando...';
        setTimeout(() => {
          if (!isLiveStreaming.value) {
            startLiveStream();
          }
        }, 3000);
      } else {
        streamStatus.value = 'Conexión cerrada';
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      streamStatus.value = 'Error de conexión';
      isLiveStreaming.value = false;
    };

  } catch (error) {
    console.error('Error conectando WebSocket:', error);
    streamStatus.value = 'Error de conexión';
    isLiveStreaming.value = false;
  }
};

const initializeAudioContext = () => {
  try {
    audioContext = new AudioContext({
      sampleRate: 48000
    });
    streamStatus.value = '🎧 Escuchando audio HD...';
    console.log('🔊 AudioContext HD listo');
  } catch (error) {
    console.error('Error inicializando audio:', error);
    streamStatus.value = 'Error en sistema de audio';
    stopLiveStream();
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
      output[i] = (input[i-1] + input[i] + input[i+1]) / 3;
    }
  }
  
  return output;
};

const stopLiveStream = () => {
  console.log('🛑 Deteniendo transmisión en vivo...');
  isLiveStreaming.value = false;
  isPlayingAudio = false;
  lastPlayTime = 0;
  
  if (ws) {
    ws.close(1000, "Usuario detuvo");
    ws = null;
  }
  
  if (audioContext) {
    audioContext.close();
    audioContext = null;
  }
  
  streamStatus.value = '';
};

// Watchers para controlar la reproducción
watch(() => props.isPlaying, (newVal) => {
  if (!audioElement.value || props.avisoAudio?.activo || isLiveStreaming.value) return
  
  if (newVal) {
    audioElement.value.play().catch(() => {})
  } else {
    audioElement.value.pause()
  }
})

watch(() => props.currentTrack, () => {
  if (props.isPlaying && audioElement.value && !props.avisoAudio?.activo && !isLiveStreaming.value) {
    audioElement.value.play().catch(() => {})
  }
})

watch(() => props.avisoAudio, (newAviso) => {
  if (newAviso?.activo && audioElement.value) {
    audioElement.value.pause()
  }
  if (newAviso?.activo && isLiveStreaming.value) {
    stopLiveStream()
  }
})

// Iniciar transmisión en vivo automáticamente al montar el componente
onMounted(() => {
  if (audioElement.value) {
    audioElement.value.volume = volume.value
  }
  // Iniciar transmisión en vivo automáticamente
  startLiveStream()
})

// Limpiar al desmontar
onUnmounted(() => {
  stopLiveStream()
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

.live-indicator {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  background: linear-gradient(135deg, #ff0000, #cc0000);
  color: white;
  font-weight: bold;
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
  display: flex;
  align-items: center;
  gap: 10px;
}

.status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.status.info {
  background-color: #dbeafe;
  color: #1e40af;
}

.status.success {
  background-color: #dcfce7;
  color: #166534;
}

.status.error {
  background-color: #fee2e2;
  color: #991b1b;
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
  
  .player-image, .aviso-indicator, .live-indicator {
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
  
  .status {
    font-size: 9px !important;
    padding: 1px 6px !important;
  }
}
</style>