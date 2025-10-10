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
        <template v-if="useMensajeInterface && avisoAudio && avisoAudio.activo">
          <MensajeHeader />
          <MensajeSidebar :active-menu="activeMenu" @set-active-menu="setActiveMenu" />
          <MensajeMainContent 
            :sections="sections" 
            :current-track="currentTrack"
            :is-playing="isPlaying"
            @play-track="handlePlayTrack"
          />
          <MensajePlayer 
            :current-track="currentTrack"
            :is-playing="isPlaying"
            :aviso-audio="avisoAudio"
            @play-pause="togglePlay"
          />
        </template>
        <template v-else>
          <Header />
          <Sidebar :active-menu="activeMenu" @set-active-menu="setActiveMenu" />
          <MainContent 
            :sections="sections" 
            :current-track="currentTrack"
            :is-playing="isPlaying"
            @play-track="handlePlayTrack"
          />
          <Player 
            :current-track="currentTrack"
            :is-playing="isPlaying"
            :aviso-audio="avisoAudio"
            @play-pause="togglePlay"
          />
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

// Componentes de mensaje (interfaz alternativa)
import MensajeHeader from '../components_mensaje/Header.vue'
import MensajeSidebar from '../components_mensaje/Sidebar.vue'
import MensajeMainContent from '../components_mensaje/MainContent.vue'
import MensajePlayer from '../components_mensaje/Player.vue'

const isLoading = ref(true)
const isPlaying = ref(false)
const activeMenu = ref('inicio')
const currentTrack = ref(null)
const useMensajeInterface = ref(false)
const avisoAudio = ref(null)
const audioFiles = ref([])
const currentAudioIndex = ref(0)
const audioPlayer = ref(null)
const lastAudioState = ref(null)
const userInteracted = ref(false)
const isInMensajeCycle = ref(false)
const cycleTimer = ref(null)
const hasStartedFirstCycle = ref(false) // Control para primer ciclo

let pollingInterval = null

const sections = ref([])

// Watcher para cambios en avisoAudio
watch(avisoAudio, (newAviso, oldAviso) => {
  console.log('AvisoAudio cambiado:', newAviso)
  
  if (newAviso?.activo && newAviso?.file) {
    useMensajeInterface.value = true
    isInMensajeCycle.value = true
    
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
    isInMensajeCycle.value = false
  }
})

// Watcher para cambios en audioFiles - SOLO para nuevos audios después del primer ciclo
watch(audioFiles, (newAudioFiles, oldAudioFiles) => {
  console.log('Audio files cambiaron:', newAudioFiles)
  
  const currentState = JSON.stringify(newAudioFiles)
  const oldState = JSON.stringify(oldAudioFiles)
  
  // Solo procesar si realmente hay cambios y no estamos en ciclo Y ya pasó el primer ciclo
  if (newAudioFiles && newAudioFiles.length > 0 && currentState !== oldState && !isInMensajeCycle.value && hasStartedFirstCycle.value) {
    console.log('Nuevos audios detectados después del primer ciclo, reiniciando ciclo...')
    
    // Limpiar timer anterior si existe
    if (cycleTimer.value) {
      clearTimeout(cycleTimer.value)
    }
    
    // Programar nuevo ciclo en 15 segundos
    cycleTimer.value = setTimeout(() => {
      startMensajeCycle()
    }, 15000)
  }
})

// Iniciar ciclo de mensaje
const startMensajeCycle = () => {
  if (audioFiles.value && audioFiles.value.length > 0) {
    console.log('🚀 INICIANDO CICLO DE MENSAJE...')
    hasStartedFirstCycle.value = true
    
    // Actualizar avisoAudio con el primer audio
    avisoAudio.value = {
      activo: true,
      audio_file: audioFiles.value[0]?.file || audioFiles.value[0]?.url || null,
      file: audioFiles.value[0]?.file || audioFiles.value[0]?.url || null,
      ...audioFiles.value[0]
    }
    
    currentAudioIndex.value = 0
    console.log('AvisoAudio configurado para ciclo:', avisoAudio.value)
  }
}

// Finalizar ciclo de mensaje y programar próximo
const finishMensajeCycle = () => {
  console.log('✅ FINALIZANDO CICLO DE MENSAJE, volviendo a interfaz normal')
  
  if (audioPlayer.value) {
    audioPlayer.value.pause()
    audioPlayer.value.currentTime = 0
  }
  
  isPlaying.value = false
  useMensajeInterface.value = false
  isInMensajeCycle.value = false
  currentAudioIndex.value = 0
  
  avisoAudio.value = {
    activo: false,
    audio_file: null,
    file: null
  }
  
  // Limpiar timer anterior si existe
  if (cycleTimer.value) {
    clearTimeout(cycleTimer.value)
  }
  
  // Programar próximo ciclo en 15 segundos EXACTOS SOLO si hay audios
  if (audioFiles.value && audioFiles.value.length > 0) {
    console.log('🔄 Programando próximo ciclo en 15 segundos EXACTOS...')
    const startTime = Date.now()
    cycleTimer.value = setTimeout(() => {
      const elapsed = Date.now() - startTime
      console.log(`⏰ Timer ejecutado después de: ${elapsed}ms`)
      startMensajeCycle()
    }, 15000) // 15 segundos exactos
  }
}

// Intentar reproducir el audio actual
const attemptAudioPlayback = async () => {
  if (!audioPlayer.value || !avisoAudio.value?.activo) {
    console.log('No se puede reproducir: audioPlayer no disponible o aviso no activo')
    return
  }

  const audioUrl = avisoAudio.value.file || avisoAudio.value.audio_file
  if (!audioUrl) {
    console.log('No hay URL de audio disponible')
    finishMensajeCycle()
    return
  }

  console.log('▶️ Intentando reproducir audio desde:', audioUrl)
  
  try {
    // Limpiar eventos anteriores para evitar duplicados
    audioPlayer.value.oncanplaythrough = null
    audioPlayer.value.onerror = null
    
    audioPlayer.value.src = audioUrl
    audioPlayer.value.load()
    
    await new Promise((resolve, reject) => {
      const onCanPlay = () => {
        audioPlayer.value.removeEventListener('error', onError)
        resolve()
      }
      
      const onError = (error) => {
        audioPlayer.value.removeEventListener('canplaythrough', onCanPlay)
        reject(error)
      }
      
      if (audioPlayer.value.readyState >= 3) {
        resolve()
      } else {
        audioPlayer.value.addEventListener('canplaythrough', onCanPlay, { once: true })
        audioPlayer.value.addEventListener('error', onError, { once: true })
      }
    })
    
    console.log('🎵 Reproduciendo audio...')
    await audioPlayer.value.play()
    isPlaying.value = true
    
  } catch (error) {
    console.error('❌ Error al reproducir audio:', error)
    finishMensajeCycle()
  }
}

// Reproducir el siguiente audio en la lista
const playNextAudio = () => {
  console.log('⏭️ Reproduciendo siguiente audio...')
  
  if (!audioFiles.value || audioFiles.value.length === 0) {
    console.log('No hay audios disponibles')
    finishMensajeCycle()
    return
  }
  
  const nextIndex = currentAudioIndex.value + 1
  console.log(`Audio actual: ${currentAudioIndex.value}, Siguiente: ${nextIndex}, Total: ${audioFiles.value.length}`)
  
  if (nextIndex < audioFiles.value.length) {
    currentAudioIndex.value = nextIndex
    
    const nextAudio = audioFiles.value[nextIndex]
    avisoAudio.value = {
      activo: true,
      audio_file: nextAudio?.file || nextAudio?.url || null,
      file: nextAudio?.file || nextAudio?.url || null,
      ...nextAudio
    }
    
    console.log('Siguiente audio configurado:', avisoAudio.value)
    
    setTimeout(() => {
      attemptAudioPlayback()
    }, 500)
  } else {
    console.log('🎯 Todos los audios reproducidos')
    finishMensajeCycle()
  }
}

// Configurar interacción del usuario
const setupUserInteraction = () => {
  const handleFirstInteraction = () => {
    userInteracted.value = true
    console.log('Usuario interactuó, intentando reproducir audio si está disponible')
    
    if (avisoAudio.value?.activo && audioPlayer.value && !isPlaying.value) {
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
  console.log('📊 Metadatos del audio cargados')
}

const handleCanPlay = () => {
  console.log('✅ Audio listo para reproducir')
}

const handleAudioPlay = () => {
  console.log('▶️ Audio empezó a reproducirse')
  isPlaying.value = true
}

const handleAudioPause = () => {
  console.log('⏸️ Audio pausado')
  isPlaying.value = false
}

const handleAudioEnded = () => {
  console.log('⏹️ Audio terminado')
  isPlaying.value = false
  
  playNextAudio()
}

const handleAudioError = (e) => {
  console.error('❌ Error en el audio:', e)
  setTimeout(() => {
    playNextAudio()
  }, 1000)
}

// Polling para obtener audios
const clearPolling = () => {
  if (pollingInterval) {
    console.log('Limpiando intervalo de polling')
    clearInterval(pollingInterval)
    pollingInterval = null
  }
}

const setupPolling = () => {
  clearPolling()
  
  console.log('Configurando polling cada 30 segundos')
  pollingInterval = setInterval(checkAudioStatus, 30000)
}

const checkAudioStatus = async () => {
  console.log('🔍 Consultando API de audios...')
  try {
    const response = await axios.get('https://api.kyeroradio.com/api/audios/')
    const audioData = response.data
    console.log('Datos recibidos de la API:', audioData)
    
    const currentState = JSON.stringify(audioData)
    if (currentState !== lastAudioState.value) {
      console.log('🆕 Nuevos datos de audio detectados')
      lastAudioState.value = currentState
      audioFiles.value = audioData
    } else {
      console.log('📝 No hay cambios en los datos de audio')
    }
  } catch (error) {
    console.error('❌ Error al obtener audios:', error)
    audioFiles.value = []
  }
}

// Limpiar todos los timers
const clearAllTimers = () => {
  if (cycleTimer.value) {
    clearTimeout(cycleTimer.value)
    cycleTimer.value = null
  }
  clearPolling()
}

const setActiveMenu = (menu) => {
  activeMenu.value = menu
}

const handlePlayTrack = (track) => {
  currentTrack.value = track
  isPlaying.value = true
}

const togglePlay = () => {
  console.log('Toggle play clicked')
  if (audioPlayer.value && avisoAudio.value?.activo) {
    if (isPlaying.value) {
      audioPlayer.value.pause()
    } else {
      audioPlayer.value.play().catch((error) => {
        console.error('Error al reproducir:', error)
      })
    }
  }
}

onMounted(async () => {
  console.log('🏠 Componente montado - INICIANDO CON REPRODUCTOR NORMAL')
  setupUserInteraction()
  await checkAudioStatus()
  setupPolling()
  
  // Solo cargar, iniciar primer ciclo después de loading
  setTimeout(() => {
    isLoading.value = false
    console.log('✅ Loading completado - REPRODUCTOR NORMAL ACTIVO')
    
    // Programar PRIMER Y ÚNICO ciclo en 15 segundos si hay audios
    if (audioFiles.value && audioFiles.value.length > 0 && !hasStartedFirstCycle.value) {
      console.log('🕒 Primer ciclo programado en 15 segundos EXACTOS...')
      const startTime = Date.now()
      cycleTimer.value = setTimeout(() => {
        const elapsed = Date.now() - startTime
        console.log(`⏰ Primer timer ejecutado después de: ${elapsed}ms`)
        startMensajeCycle()
      }, 15000) // 15 segundos exactos
    }
  }, 3000)
})

onUnmounted(() => {
  console.log('🔚 Componente desmontado')
  clearAllTimers()
})
</script>

<style scoped>
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
  padding-bottom: 130px;
}

.main-content {
  min-height: calc(100vh - 130px);
}

/* El resto de tus estilos se mantienen igual */
.demo-content {
  padding: 20px;
  color: white;
  text-align: center;
}

.demo-box {
  background: rgba(255, 255, 255, 0.2);
  padding: 20px;
  border-radius: 10px;
  margin: 10px;
  backdrop-filter: blur(10px);
}

audio {
  display: none;
}

/* Responsive */
@media (max-width: 1024px) {
  .app-container {
    padding-bottom: 100px;
  }
  .main-content {
    min-height: calc(100vh - 100px);
  }
}

@media (max-width: 768px) {
  .app-container {
    padding-bottom: 80px;
  }
  .main-content {
    min-height: calc(100vh - 80px);
  }
}

@media (max-width: 480px) {
  .app-container {
    padding-bottom: 70px;
  }
  .main-content {
    min-height: calc(100vh - 70px);
  }
}
</style>