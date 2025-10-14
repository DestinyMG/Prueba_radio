<template>
  <div class="global-background">
    <div class="home">
      <!-- Audio para el aviso (oculto) -->
      <audio v-if="avisoAudio && avisoAudio.activo && avisoAudio.audio_file" 
             :src="avisoAudio.audio_file" 
             ref="audioPlayer"
             @ended="handleAudioEnded"
             @canplaythrough="handleCanPlay"
             @loadedmetadata="handleLoadedMetadata"
             @play="handleAudioPlay"
             @pause="handleAudioPause">
      </audio>

      <LoadingScreen v-if="isLoading" />
      
      <div v-if="!isLoading" class="app-container">
        <div class="main-content">
          <!-- 🔹 PRIORIDAD 1: Streaming en vivo (controlado por backend) -->
          <template v-if="streamingStatus">
            <StreamingHeader />
            <StreamingMainContent 
              :sections="sections" 
              :current-track="currentTrack"
              :is-playing="isPlaying"
              @play-track="handlePlayTrack"
            />
            <StreamingFooter @toggle-streaming="toggleStreaming" />
          </template>
          
          <!-- 🔹 PRIORIDAD 2: Mensaje importante -->
          <template v-else-if="useMensajeInterface && avisoAudio && avisoAudio.activo">
            <MensajeHeader />
            <MensajeMainContent 
              :sections="sections" 
              :current-track="currentTrack"
              :is-playing="isPlaying"
              @play-track="handlePlayTrack"
            />
            <MensajeFooter />
          </template>
          
          <!-- 🔹 PRIORIDAD 3: Vista normal de usuario -->
          <template v-else>
            <Header @toggle-streaming="toggleStreaming" />
            <MainContent 
              :sections="sections" 
              :current-track="currentTrack"
              :is-playing="isPlaying"
              @play-track="handlePlayTrack"
            />
            <UsuarioFooter @toggle-streaming="toggleStreaming" />
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import axios from 'axios'

// Componentes principales
import LoadingScreen from '../components_usuario/LoadingScreen.vue'
import Header from '../components_usuario/Header.vue'
import MainContent from '../components_usuario/MainContent.vue'
import UsuarioFooter from '../components_usuario/footer.vue'

// Componentes de mensaje
import MensajeHeader from '../components_mensaje/Header.vue'
import MensajeMainContent from '../components_mensaje/MainContent.vue'
import MensajeFooter from '../components_mensaje/footer.vue'

// Componentes de streaming (nuevos)
import StreamingHeader from '../components_streaming/Header.vue'
import StreamingMainContent from '../components_streaming/MainContent.vue'
import StreamingFooter from '../components_streaming/footer.vue'

const isLoading = ref(true)
const isPlaying = ref(false)
const currentTrack = ref(null)
const useMensajeInterface = ref(false)
const avisoAudio = ref(null)
const audioPlayer = ref(null)
const lastAvisoState = ref(null)
const userInteracted = ref(false)

// 🔹 NUEVA: Variable para estado de streaming desde backend
const streamingStatus = ref(false)
const isStreamingActive = ref(false) // Para control interno del WebSocket

// Variables para WebSocket streaming
let ws = null
let audioContext = null
let isPlayingAudio = false
let lastPlayTime = 0

let pollingInterval = null
let streamingPollingInterval = null // 🔹 NUEVO: Polling para estado de streaming

const sections = ref([])

// 🔹 NUEVA: Función para verificar estado de streaming desde backend
const checkStreamingStatus = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api3/')
        const newStatus = response.data.activate  // ← CAMBIADO de "is_active" a "activate"
        
        if (newStatus !== streamingStatus.value) {
            streamingStatus.value = newStatus
            console.log(`📡 Estado de streaming actualizado: ${newStatus}`)
            
            // Si el backend dice que hay streaming, conectar WebSocket automáticamente
            if (newStatus && !isStreamingActive.value) {
                connectWebSocket()
            } else if (!newStatus && isStreamingActive.value) {
                stopStreaming()
            }
        }
    } catch (error) {
        console.error('Error verificando estado de streaming:', error)
    }
}

// 🔹 MODIFICADO: Watcher para cambios en streamingStatus
watch(streamingStatus, (newVal) => {
    if (newVal) {
        // Cuando se activa el streaming desde el admin, conectar WebSocket automáticamente
        if (!isStreamingActive.value) {
            connectWebSocket()
        }
    } else {
        // Cuando se desactiva, desconectar
        if (isStreamingActive.value) {
            stopStreaming()
        }
    }
})

// 🔹 MODIFICADO: Funciones de streaming WebSocket
const toggleStreaming = () => {
    if (isStreamingActive.value) {
        stopStreaming()
    } else {
        // El usuario no puede iniciar streaming, solo el admin
        console.log('🎤 Solo el administrador puede iniciar transmisión en vivo')
        // Podrías mostrar un mensaje al usuario aquí
    }
}

const startStreaming = () => {
    if (isStreamingActive.value) return
    isStreamingActive.value = true
    connectWebSocket()
}

const connectWebSocket = () => {
    try {
        ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/")
        ws.binaryType = "arraybuffer"

        ws.onopen = () => {
            console.log('✅ WebSocket CONECTADO para streaming')
            initializeAudioContext()
        }

        ws.onmessage = (event) => {
            if (!isStreamingActive.value || !audioContext) return

            if (event.data instanceof ArrayBuffer && event.data.byteLength > 0) {
                processRawAudio(event.data)
            }
        }

        ws.onclose = (event) => {
            console.log('WebSocket cerrado')
            isStreamingActive.value = false
            
            if (event.code !== 1000) {
                // Reconectar después de 3 segundos si no fue una desconexión intencional
                setTimeout(() => {
                    if (streamingStatus.value && !isStreamingActive.value) {
                        connectWebSocket()
                    }
                }, 3000)
            }
        }

        ws.onerror = (error) => {
            console.error('WebSocket error:', error)
            isStreamingActive.value = false
        }

    } catch (error) {
        console.error('Error conectando WebSocket:', error)
        isStreamingActive.value = false
    }
}

const initializeAudioContext = () => {
    try {
        audioContext = new AudioContext({ sampleRate: 48000 })
        console.log('🔊 AudioContext HD listo para streaming')
    } catch (error) {
        console.error('Error inicializando audio:', error)
        stopStreaming()
    }
}

const processRawAudio = (rawData) => {
    if (!audioContext) return

    try {
        // Convertir Int16 back to Float32
        const int16Data = new Int16Array(rawData)
        const float32Data = new Float32Array(int16Data.length)
        
        for (let i = 0; i < int16Data.length; i++) {
            float32Data[i] = int16Data[i] / (int16Data[i] < 0 ? 0x8000 : 0x7FFF)
        }

        // Aplicar filtro de suavizado para mejor calidad
        const smoothedData = smoothAudio(float32Data)

        // Crear buffer de audio
        const audioBuffer = audioContext.createBuffer(1, smoothedData.length, 48000)
        audioBuffer.getChannelData(0).set(smoothedData)

        // Controlar timing para evitar solapamiento
        const now = audioContext.currentTime
        const playTime = Math.max(lastPlayTime, now)
        
        // Crear fuente y reproducir
        const source = audioContext.createBufferSource()
        source.buffer = audioBuffer
        source.connect(audioContext.destination)
        source.start(playTime)
        
        lastPlayTime = playTime + audioBuffer.duration

        if (!isPlayingAudio) {
            isPlayingAudio = true
            console.log('🎵 Audio HD streaming reproduciéndose!')
        }

    } catch (error) {
        console.log('Error procesando audio streaming:', error)
    }
}

// Filtro de suavizado para mejor calidad
const smoothAudio = (input) => {
    const output = new Float32Array(input.length)
    
    // Filtro simple para reducir ruido
    for (let i = 0; i < input.length; i++) {
        if (i === 0 || i === input.length - 1) {
            output[i] = input[i]
        } else {
            // Promedio suavizado
            output[i] = (input[i-1] + input[i] + input[i+1]) / 3
        }
    }
    
    return output
}

const stopStreaming = () => {
    console.log('🛑 Deteniendo streaming...')
    isStreamingActive.value = false
    isPlayingAudio = false
    lastPlayTime = 0
    
    if (ws) {
        ws.close(1000, "Usuario detuvo")
        ws = null
    }
    
    if (audioContext) {
        audioContext.close()
        audioContext = null
    }
}

// Watcher para cambios en avisoAudio
watch(avisoAudio, (newAviso, oldAviso) => {
    if (newAviso?.activo && newAviso?.audio_file) {
        useMensajeInterface.value = true
        
        nextTick(() => {
            setTimeout(() => {
                attemptAudioPlayback()
            }, 100)
        })
    } else if (oldAviso?.activo && !newAviso?.activo) {
        if (audioPlayer.value) {
            audioPlayer.value.pause()
            audioPlayer.value.currentTime = 0
        }
        isPlaying.value = false
        useMensajeInterface.value = false
    }
})

// Watcher para cambios en streamingStatus
watch(streamingStatus, (newVal) => {
    if (newVal) {
        // Cuando se activa el streaming, pausar cualquier audio actual
        if (audioPlayer.value) {
            audioPlayer.value.pause()
            audioPlayer.value.currentTime = 0
        }
        isPlaying.value = false
    }
})

// Intentar reproducir el audio
const attemptAudioPlayback = async () => {
    if (!audioPlayer.value || !avisoAudio.value?.activo || streamingStatus.value) return
    
    try {
        audioPlayer.value.load()
        
        await new Promise((resolve) => {
            if (audioPlayer.value.readyState >= 3) {
                resolve()
            } else {
                audioPlayer.value.addEventListener('canplaythrough', resolve, { once: true })
            }
        })
        
        await audioPlayer.value.play()
        isPlaying.value = true
        
    } catch (error) {
        // Autoplay bloqueado, se reproducirá con interacción del usuario
    }
}

// Configurar interacción del usuario
const setupUserInteraction = () => {
    const handleFirstInteraction = () => {
        userInteracted.value = true
        
        if (avisoAudio.value?.activo && audioPlayer.value && !isPlaying.value && !streamingStatus.value) {
            attemptAudioPlayback()
        }
        
        document.removeEventListener('click', handleFirstInteraction)
        document.removeEventListener('touchstart', handleFirstInteraction)
        document.removeEventListener('keydown', handleFirstInteraction)
    }
    
    document.addEventListener('click', handleFirstInteraction, { once: true })
    document.addEventListener('touchstart', handleFirstInteraction, { once: true })
    document.addEventListener('keydown', handleFirstInteraction, { once: true })
}

// Eventos del audio
const handleLoadedMetadata = () => {
    // Metadatos cargados
}

const handleCanPlay = () => {
    // Audio listo
}

const handleAudioPlay = () => {
    isPlaying.value = true
}

const handleAudioPause = () => {
    isPlaying.value = false
}

const handleAudioEnded = () => {
    isPlaying.value = false
    setTimeout(checkAvisoStatus, 100)
}

// Polling para avisos
const clearPolling = () => {
    if (pollingInterval) {
        clearInterval(pollingInterval)
        pollingInterval = null
    }
}

const setupPolling = () => {
    clearPolling()
    
    const intervalTime = avisoAudio.value?.activo ? 2000 : 5000
    pollingInterval = setInterval(checkAvisoStatus, intervalTime)
}

// 🔹 NUEVO: Polling para estado de streaming
const setupStreamingPolling = () => {
    streamingPollingInterval = setInterval(checkStreamingStatus, 2000) // Verificar cada 2 segundos
}

const clearStreamingPolling = () => {
    if (streamingPollingInterval) {
        clearInterval(streamingPollingInterval)
        streamingPollingInterval = null
    }
}

const checkAvisoStatus = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api2/aviso/2/')
        const avisoData = response.data
        
        const currentState = JSON.stringify(avisoData)
        if (currentState !== lastAvisoState.value) {
            lastAvisoState.value = currentState
            avisoAudio.value = avisoData
        }
    } catch (error) {
        // Error en la consulta
    }
}

const handlePlayTrack = (track) => {
    currentTrack.value = track
    isPlaying.value = true
}

onMounted(async () => {
    setupUserInteraction()
    await checkAvisoStatus()
    await checkStreamingStatus() // 🔹 Verificar estado al cargar
    setupPolling()
    setupStreamingPolling() // 🔹 Iniciar polling de streaming
    
    setTimeout(() => {
        isLoading.value = false
    }, 3000)
})

onUnmounted(() => {
    clearPolling()
    clearStreamingPolling() // 🔹 Limpiar polling de streaming
    stopStreaming()
})
</script>

<style scoped>
/* Tus estilos existentes se mantienen igual */
.global-background {
  background: linear-gradient(135deg, #009DDB 0%, #007DB8 50%, #005A87 100%);
  color: var(--text-primary);
  display: flex;
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
  width: 100%;
}

.global-background::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(255,255,255,0.4) 0%, transparent 20%),
    radial-gradient(circle at 90% 80%, rgba(255,255,255,0.4) 0%, transparent 20%),
    radial-gradient(circle at 30% 60%, rgba(255,255,255,0.3) 0%, transparent 25%),
    radial-gradient(circle at 70% 30%, rgba(255,255,255,0.3) 0%, transparent 25%);
  background-size: 200% 200%;
  background-position: 0% 0%;
  z-index: -1;
  opacity: 0.9;
  animation: waveAnimation 15s infinite alternate;
}

@keyframes waveAnimation {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 100% 100%;
  }
}

:root {
  --primary: #009DDB;
  --primary-dark: #007DB8;
  --light-bg: #FAFBFD;
  --dark-bg: #E1F0F7;
  --sidebar-bg: #FFFFFF;
  --card-bg: #FFFFFF;
  --text-primary: #2D3748;
  --text-secondary: #5F6C7B;
  --divider: #E2E8F0;
  --menu-hover: rgba(0, 157, 219, 0.1);
  --shadow: 0 4px 12px rgba(0, 125, 184, 0.1);
  --highlight-bg: rgba(0, 157, 219, 0.05);
  --gradient-primary: linear-gradient(135deg, var(--primary), var(--primary-dark));
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Circular', -apple-system, BlinkMacSystemFont, sans-serif;
}

.home {
  width: 100%;
  min-height: 100vh;
}

.app-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
}

.main-content {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Asegurar que el footer quede pegado abajo */
.main-content > *:not(footer) {
  flex: 1 0 auto;
}

.main-content > footer {
  flex-shrink: 0;
}

audio {
  display: none;
}

/* Responsive */
@media (max-width: 1024px) {
  .main-content {
    min-height: 100vh;
  }
}

@media (max-width: 768px) {
  .main-content {
    min-height: 100vh;
  }
}

@media (max-width: 480px) {
  .main-content {
    min-height: 100vh;
  }
}
</style>