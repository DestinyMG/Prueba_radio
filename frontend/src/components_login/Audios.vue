<template>
    <BaseAdmin>
        <div class="admin-container">
            <!-- Indicador de conflicto -->
            <div v-if="conflictStatus" class="conflict-warning">
                ⚠️ {{ conflictStatus }}
            </div>

            <div class="page-header">
                <h1><i class="fas fa-headphones"></i> Mis Audios</h1>
                <div class="header-actions">
                    <button class="stream-button" @click="showStreamModal = true">
                        <i class="fas fa-microphone"></i>
                        {{ streamingStatus ? 'Transmisión Activa' : 'Transmisión en Vivo' }}
                    </button>
                    <button class="upload-button" @click="showModal = true">
                        <i class="fas fa-plus"></i> Cargar Nuevo Audio
                    </button>
                </div>
            </div>

            <!-- Estadísticas rápidas -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-music"></i></div>
                    <div class="stat-info">
                        <h3>{{ audios.length }}</h3>
                        <p>Audios Totales</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-volume-up"></i></div>
                    <div class="stat-info">
                        <h3>{{ adminActiveAudiosCount }}</h3>
                        <p>En Reproducción</p>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-clock"></i></div>
                    <div class="stat-info">
                        <h3>{{ adminScheduledAudiosCount }}</h3>
                        <p>Programados</p>
                    </div>
                </div>
                <div class="stat-card live-indicator" :class="{ live: streamingStatus }">
                    <div class="stat-icon"><i class="fas fa-broadcast-tower"></i></div>
                    <div class="stat-info">
                        <h3>{{ streamingStatus ? 'EN VIVO' : 'Offline' }}</h3>
                        <p>Transmisión</p>
                    </div>
                </div>
            </div>

            <!-- Grid de audios -->
            <div class="audio-grid" v-if="audios.length > 0">
                <div v-for="audio in audios" :key="audio.id" class="audio-card">
                    <div class="card-main-content">
                        <div class="card-icon"><i class="fas fa-music"></i></div>
                        <div class="card-content">
                            <h3 class="card-title">{{ audio.title }}</h3>
                            <p class="card-date">
                                <span><i class="fas fa-calendar"></i> Programado para:</span>
                                {{ formatDate(audio.play_date) }}
                            </p>
                            <p v-if="isAudioActive(audio.id)" class="active-indicator">
                                <i class="fas fa-volume-up"></i> Reproduciéndose en sistema
                            </p>
                        </div>
                    </div>

                    <div class="card-footer">
                        <div class="card-actions">
                            <button class="action-button edit-button">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                            <button class="action-button delete-button" @click="deleteAudio(audio.id)">
                                <i class="fas fa-trash"></i> Eliminar
                            </button>
                        </div>

                        <!-- Botón play/stop -->
                        <button class="play-button" :class="{ playing: isAudioActive(audio.id) }"
                            @click="toggleAudioActivation(audio)" :disabled="streamingStatus">
                            <i class="fas" :class="isAudioActive(audio.id) ? 'fa-stop' : 'fa-play'"></i>
                            {{ isAudioActive(audio.id) ? 'Detener' : streamingStatus ? 'Streaming Activo' : 'Activar' }}
                        </button>
                    </div>
                </div>
            </div>

            <!-- Estado vacío -->
            <div v-else class="empty-state">
                <div class="empty-icon"><i class="fas fa-music"></i></div>
                <h2>No tienes audios aún</h2>
                <p>Comienza cargando tu primer audio para programarlo en el sistema</p>
                <button class="upload-button" @click="showModal = true">
                    <i class="fas fa-plus"></i> Cargar Primer Audio
                </button>
            </div>

            <!-- Modal para crear audio -->
            <CrearAudio v-if="showModal" @close="showModal = false" @saved="handleSaved" />

            <!-- Modal para transmisión en vivo -->
            <div v-if="showStreamModal" class="modal-overlay" @click="showStreamModal = false">
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h2><i class="fas fa-microphone"></i> Transmisión en Vivo</h2>
                        <button class="close-button" @click="showStreamModal = false">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>

                    <div class="stream-controls">
                        <div class="stream-status" :class="{ live: isStreaming, connecting: isConnecting }">
                            <div class="status-indicator"></div>
                            <span>
                                {{ isConnecting ? 'CONECTANDO...' :
                                    isStreaming ? 'TRANSMITIENDO EN VIVO' : 'LISTO PARA TRANSMITIR' }}
                            </span>
                        </div>

                        <div class="stream-info">
                            <div class="info-item">
                                <label><i class="fas fa-clock"></i> Tiempo de transmisión:</label>
                                <span>{{ streamTime }}</span>
                            </div>
                            <div class="info-item">
                                <label><i class="fas fa-microphone-alt"></i> Estado del micrófono:</label>
                                <span :class="{ active: isStreaming }">
                                    {{ isStreaming ? 'Activo' : isConnecting ? 'Conectando...' : 'Inactivo' }}
                                </span>
                            </div>
                        </div>

                        <button class="stream-toggle-button"
                            :class="{ streaming: isStreaming, connecting: isConnecting }" @click="toggleStreaming"
                            :disabled="isConnecting">
                            <div class="button-content">
                                <i class="fas" :class="isConnecting ? 'fa-spinner fa-spin' :
                                        isStreaming ? 'fa-stop-circle' : 'fa-microphone'
                                    "></i>
                                <span class="button-text">
                                    {{ isConnecting ? 'CONECTANDO...' :
                                        isStreaming ? 'DETENER TRANSMISIÓN' : 'INICIAR TRANSMISIÓN' }}
                                </span>
                            </div>
                            <div v-if="isStreaming" class="button-status">
                                {{ streamTime }}
                            </div>
                        </button>

                        <div v-if="status" class="status-message" :class="{ error: status.includes('Error') }">
                            {{ status }}
                        </div>

                        <!-- Botón de reconexión rápida -->
                        <div v-if="connectionError" class="reconnection-panel">
                            <p>⚠️ Problema de conexión detectado</p>
                            <button class="reconnect-button" @click="forceReconnect">
                                <i class="fas fa-redo"></i> Reintentar Conexión
                            </button>
                        </div>

                        <div class="stream-tips">
                            <h4><i class="fas fa-lightbulb"></i> Consejos para mejor calidad:</h4>
                            <ul>
                                <li><i class="fas fa-comment-dots"></i> Habla claramente y a volumen constante</li>
                                <li><i class="fas fa-arrows-alt-h"></i> Mantén una distancia adecuada del micrófono</li>
                                <li><i class="fas fa-volume-mute"></i> Evita ambientes con ruido de fondo</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </BaseAdmin>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import BaseAdmin from './BaseAdmin.vue';
import CrearAudio from './CrearAudio.vue';
import api from '../axios/axios';
import axios from 'axios';

// Variables existentes
const audios = ref([]);
const activeAudioId = ref(null);
const showModal = ref(false);
let scheduleInterval = null;

// Variables para transmisión en vivo - MEJORADAS
const showStreamModal = ref(false);
const isStreaming = ref(false);
const isConnecting = ref(false);
const streamTime = ref('00:00');
const status = ref('');
const connectionError = ref(false);
let ws;
let audioContext;
let processor;
let stream;
let streamTimer = null;
let streamStartTime = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

// Estado de streaming desde backend
const streamingStatus = ref(false);

// Variables para monitoreo de duración de audio - MEJORADAS
let audioDurationCheckInterval = null;
const audioDurations = ref(new Map());
const lastPlayedAudios = ref(new Set()); // Para evitar repeticiones

// Computed properties
const adminActiveAudiosCount = computed(() => {
    return activeAudioId.value ? 1 : 0;
});

const adminScheduledAudiosCount = computed(() => {
    const now = new Date();
    return audios.value.filter(audio => new Date(audio.play_date) > now).length;
});

// Computed para detectar conflictos
const conflictStatus = computed(() => {
    if (streamingStatus.value && activeAudioId.value) {
        return 'Conflicto: Streaming y Audio activos simultáneamente';
    }
    return null;
});

// 🔥 CORREGIDO: Función mejorada para verificar permisos de micrófono
const checkMicrophonePermission = async () => {
    try {
        // Primero verificar si el navegador soporta getUserMedia
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('Tu navegador no soporta acceso al micrófono');
        }

        // Solicitar permisos de manera más específica
        const testStream = await navigator.mediaDevices.getUserMedia({
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: false
            }
        });

        // Liberar stream de prueba inmediatamente
        testStream.getTracks().forEach(track => track.stop());

        return true;
    } catch (error) {
        console.error('Error verificando permisos:', error);

        if (error.name === 'NotAllowedError') {
            status.value = 'Error: Permisos de micrófono denegados. Por favor permite el acceso al micrófono.';
        } else if (error.name === 'NotFoundError') {
            status.value = 'Error: No se encontró ningún micrófono disponible.';
        } else {
            status.value = `Error de micrófono: ${error.message}`;
        }

        return false;
    }
};

// 🔥 NUEVO: Función mejorada para manejo de reconexión
const forceReconnect = async () => {
    if (isStreaming.value) {
        await stopStreaming();
    }

    connectionError.value = false;
    reconnectAttempts = 0;
    status.value = 'Reconectando...';

    // Pequeña pausa antes de reconectar
    await new Promise(resolve => setTimeout(resolve, 1500));

    await startStreaming();
};

// 🔥 MEJORADO: Función toggleStreaming con mejor manejo de estado
const toggleStreaming = async () => {
    if (isConnecting.value) {
        console.log('Ya se está conectando, ignorando click...');
        return;
    }

    try {
        if (!isStreaming.value) {
            await startStreaming();
        } else {
            await stopStreaming();
        }
    } catch (error) {
        console.error('Error en toggleStreaming:', error);
        status.value = `Error: ${error.message}`;
    }
};

// 🔥 MEJORADO: Función startStreaming con mejor manejo de errores
const startStreaming = async () => {
    if (isStreaming.value || isConnecting.value) {
        console.log('Streaming ya activo o conectando, ignorando...');
        return;
    }

    // Verificar si hay audio activo
    if (activeAudioId.value) {
        const confirmar = confirm(
            '🔊 Hay un audio activo reproduciéndose\n\n' +
            'Al iniciar la transmisión en vivo:\n' +
            '• El audio actual se detendrá\n' +
            '• Los oyentes escucharán tu micrófono\n\n' +
            '¿Deseas continuar?'
        );

        if (!confirmar) return;
        await setAvisoActivo(false);
    }

    isConnecting.value = true;
    connectionError.value = false;
    status.value = 'Solicitando permisos de micrófono...';

    try {
        // Verificar permisos primero
        const hasPermission = await checkMicrophonePermission();
        if (!hasPermission) {
            throw new Error('Permisos de micrófono no concedidos');
        }

        status.value = 'Conectando con el servidor...';

        // 🔥 MEJORADO: WebSocket con mejor manejo de timeout
        ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
        ws.binaryType = "arraybuffer";

        // Timeout de conexión más robusto
        const connectionTimeout = setTimeout(() => {
            if (ws.readyState !== WebSocket.OPEN) {
                ws.close();
                throw new Error('Timeout de conexión: El servidor no respondió en 10 segundos');
            }
        }, 10000);

        await new Promise((resolve, reject) => {
            ws.onopen = () => {
                console.log('✅ WebSocket conectado exitosamente');
                clearTimeout(connectionTimeout);
                resolve();
            };

            ws.onerror = (error) => {
                console.error('❌ Error WebSocket:', error);
                clearTimeout(connectionTimeout);
                reject(new Error('Error de conexión con el servidor de streaming'));
            };

            ws.onclose = (event) => {
                clearTimeout(connectionTimeout);
                if (!event.wasClean && isConnecting.value) {
                    reject(new Error('Conexión cerrada inesperadamente por el servidor'));
                }
            };
        });

        status.value = 'Configurando audio...';

        // Configuración de audio optimizada
        stream = await navigator.mediaDevices.getUserMedia({
            audio: {
                channelCount: 1,
                sampleRate: 48000,
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: false,
                latency: 0.01
            }
        });

        // AudioContext optimizado
        audioContext = new AudioContext({
            sampleRate: 48000,
            latencyHint: 'interactive'
        });

        const source = audioContext.createMediaStreamSource(stream);

        // Processor optimizado
        processor = audioContext.createScriptProcessor(2048, 1, 1);

        processor.onaudioprocess = (event) => {
            if (!isStreaming.value || ws.readyState !== WebSocket.OPEN) return;

            try {
                const inputData = event.inputBuffer.getChannelData(0);
                const int16Data = floatTo16BitPCM(inputData);

                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(int16Data);
                }
            } catch (error) {
                console.debug('Error procesando audio:', error);
            }
        };

        // Conectar
        source.connect(processor);
        processor.connect(audioContext.destination);

        // Actualizar estado en backend
        await updateStreamingStatus(true);

        // Resetear estados de éxito
        isStreaming.value = true;
        isConnecting.value = false;
        connectionError.value = false;
        reconnectAttempts = 0;
        status.value = '🎤 Transmitiendo en vivo...';
        streamStartTime = new Date();
        startStreamTimer();

        console.log('🚀 Transmisión INICIADA exitosamente');

    } catch (error) {
        console.error('❌ Error iniciando streaming:', error);

        // Mejor manejo de errores
        isConnecting.value = false;
        connectionError.value = true;
        reconnectAttempts++;

        let errorMessage = error.message;

        // Mensajes de error más específicos
        if (errorMessage.includes('Timeout')) {
            errorMessage = 'El servidor no respondió. Verifica tu conexión a internet.';
        } else if (errorMessage.includes('permisos')) {
            errorMessage = 'Permisos de micrófono requeridos. Por favor permite el acceso.';
        }

        if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
            status.value = `❌ ${errorMessage}. Reintentos agotados.`;
        } else {
            status.value = `⚠️ ${errorMessage}. Reintentando... (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})`;

            // Reintentar automáticamente después de un tiempo progresivo
            const retryDelay = Math.min(2000 * reconnectAttempts, 10000);
            setTimeout(() => {
                if (!isStreaming.value && !isConnecting.value) {
                    startStreaming();
                }
            }, retryDelay);
        }

        // Limpiar recursos en caso de error
        await cleanupStreamingResources();
    }
};

// 🔥 MEJORADO: Función para limpiar recursos de streaming
const cleanupStreamingResources = async () => {
    try {
        if (processor) {
            processor.disconnect();
            processor.onaudioprocess = null;
            processor = null;
        }
        if (stream) {
            stream.getTracks().forEach(track => {
                track.stop();
                track.enabled = false;
            });
            stream = null;
        }
        if (audioContext && audioContext.state !== 'closed') {
            await audioContext.close();
            audioContext = null;
        }
        if (ws) {
            ws.onopen = null;
            ws.onerror = null;
            ws.onclose = null;
            ws.close();
            ws = null;
        }
    } catch (error) {
        console.debug('Error limpiando recursos:', error);
    }
};

// 🔥 MEJORADO: Función stopStreaming
const stopStreaming = async () => {
    if (!isStreaming.value && !isConnecting.value) return;

    isConnecting.value = false;
    status.value = 'Deteniendo transmisión...';

    try {
        // Actualizar estado en backend primero
        await updateStreamingStatus(false);
    } catch (error) {
        console.debug('Error actualizando estado de streaming:', error);
    }

    // Limpiar recursos
    await cleanupStreamingResources();

    // Resetear estados
    isStreaming.value = false;
    connectionError.value = false;
    reconnectAttempts = 0;
    status.value = 'Transmisión detenida';
    stopStreamTimer();

    console.log('🛑 Transmisión detenida correctamente');
};

// Conversión básica sin alteraciones
const floatTo16BitPCM = (input) => {
    const output = new Int16Array(input.length);
    for (let i = 0; i < input.length; i++) {
        const s = Math.max(-1, Math.min(1, input[i]));
        output[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
    }
    return output.buffer;
};

const startStreamTimer = () => {
    streamTimer = setInterval(() => {
        const now = new Date();
        const diff = Math.floor((now - streamStartTime) / 1000);
        const minutes = Math.floor(diff / 60).toString().padStart(2, '0');
        const seconds = (diff % 60).toString().padStart(2, '0');
        streamTime.value = `${minutes}:${seconds}`;
    }, 1000);
};

const stopStreamTimer = () => {
    if (streamTimer) {
        clearInterval(streamTimer);
        streamTimer = null;
    }
    streamTime.value = '00:00';
};

// 🔥 CORREGIDO: Función mejorada para obtener duración de audio
const getAudioDuration = (audioFile) => {
    return new Promise((resolve) => {
        const audio = new Audio();
        audio.preload = 'metadata';

        // Manejar CORS si es necesario
        audio.crossOrigin = 'anonymous';

        audio.src = audioFile.startsWith('http')
            ? audioFile
            : `https://prueba-radio.onrender.com${audioFile}`;

        const timeout = setTimeout(() => {
            resolve(60); // Fallback a 60 segundos
        }, 5000);

        audio.addEventListener('loadedmetadata', () => {
            clearTimeout(timeout);
            resolve(Math.ceil(audio.duration));
        });

        audio.addEventListener('error', () => {
            clearTimeout(timeout);
            resolve(60); // Fallback a 60 segundos
        });

        // Forzar carga
        audio.load();
    });
};

// 🔥 CORREGIDO: Sistema mejorado de programación de audios
const startAudioDurationCheck = (audioId, duration) => {
    stopAudioDurationCheck();

    let timeElapsed = 0;
    audioDurationCheckInterval = setInterval(async () => {
        timeElapsed += 1;

        // 🔥 MEJORADO: Tolerancia de +5 segundos para evitar cortes prematuros
        if (timeElapsed >= duration + 5) {
            await stopAudioAutomatically(audioId);
        }
    }, 1000);
};

const stopAudioDurationCheck = () => {
    if (audioDurationCheckInterval) {
        clearInterval(audioDurationCheckInterval);
        audioDurationCheckInterval = null;
    }
};

const stopAudioAutomatically = async (audioId) => {
    if (activeAudioId.value === audioId) {
        console.log(`🛑 Deteniendo audio ${audioId} automáticamente (duración completada)`);
        await setAvisoActivo(false);
        stopAudioDurationCheck();

        // 🔥 NUEVO: Marcar como reproducido para evitar repeticiones
        lastPlayedAudios.value.add(audioId);

        // 🔥 NUEVO: Limpiar historial después de 1 hora para permitir repeticiones programadas
        setTimeout(() => {
            lastPlayedAudios.value.delete(audioId);
        }, 3600000); // 1 hora
    }
};

const checkStreamingStatus = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api3/');
        streamingStatus.value = response.data.activate;
    } catch (error) {
        console.debug('Error verificando estado de streaming:', error);
    }
};

// 🔥 CORREGIDO: Función mejorada para activar/desactivar audio
const setAvisoActivo = async (activo, audioId = null, audioFile = null) => {
    try {
        await checkStreamingStatus();

        if (activo && streamingStatus.value) {
            const confirmar = confirm(
                '⚠️ Hay una transmisión en vivo activa.\n\n' +
                'Si activas este audio, la transmisión en vivo se detendrá.\n\n' +
                '¿Deseas continuar?'
            );

            if (!confirmar) {
                return;
            }

            await updateStreamingStatus(false);
        }

        let payload;

        if (activo && audioId) {
            // 🔥 NUEVO: Verificar si ya fue reproducido recientemente
            if (lastPlayedAudios.value.has(audioId)) {
                console.log(`⏭️ Audio ${audioId} ya fue reproducido recientemente, omitiendo...`);
                return;
            }

            payload = {
                activo: true,
                audio_id: audioId
            };

            if (audioFile) {
                const duration = await getAudioDuration(audioFile);
                console.log(`🎵 Audio ${audioId} duración: ${duration} segundos`);
                startAudioDurationCheck(audioId, duration);
            }
        } else {
            payload = {
                activo: false
            };
            stopAudioDurationCheck();
        }

        const response = await axios.put('http://localhost:8000/api2/aviso/2/', payload, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (activo && audioId) {
            activeAudioId.value = audioId;
            console.log(`▶️ Audio ${audioId} activado`);
        } else {
            activeAudioId.value = null;
            console.log('⏹️ Audio desactivado');
        }

        return response.data;

    } catch (error) {
        console.error('Error actualizando el audio:', error);
        alert('Error actualizando el audio');
        throw error;
    }
};

const updateStreamingStatus = async (isActive) => {
    try {
        const response = await axios.put('http://localhost:8000/api3/', {
            activate: isActive
        });

        streamingStatus.value = isActive;
        console.log(`📡 Estado de streaming actualizado: ${isActive}`);
        return response.data;
    } catch (error) {
        console.error('Error actualizando estado de streaming:', error);
        alert('Error actualizando estado de streaming');
        throw error;
    }
};

const isAudioActive = (audioId) => {
    return activeAudioId.value === audioId;
};

const toggleAudioActivation = async (audio) => {
    try {
        if (isAudioActive(audio.id)) {
            await setAvisoActivo(false);
        } else {
            if (streamingStatus.value) {
                const confirmar = confirm(
                    '🎤 Hay una transmisión en vivo activa\n\n' +
                    'Al activar este audio:\n' +
                    '• La transmisión en vivo se detendrá\n' +
                    '• Los oyentes escucharán este audio\n\n' +
                    '¿Deseas continuar?'
                );

                if (!confirmar) return;
                await updateStreamingStatus(false);
            }

            if (activeAudioId.value) {
                await setAvisoActivo(false);
            }

            await setAvisoActivo(true, audio.id, audio.file);
        }
        await fetchAudios();
    } catch (error) {
        alert('Error al controlar el audio');
    }
};

// 🔥 CORREGIDO: Sistema mejorado de programación de audios
const checkScheduledAudios = async () => {
    await checkStreamingStatus();

    // No programar audios si hay streaming activo
    if (streamingStatus.value) {
        return;
    }

    const now = new Date();

    for (const audio of audios.value) {
        const scheduledTime = new Date(audio.play_date);
        const timeDiff = scheduledTime - now;

        // 🔥 MEJORADO: Margen de ±2 segundos para evitar repeticiones
        if (timeDiff >= -2000 && timeDiff <= 2000 && !isAudioActive(audio.id)) {

            // 🔥 NUEVO: Verificar si ya fue reproducido recientemente
            if (lastPlayedAudios.value.has(audio.id)) {
                console.log(`⏭️ Audio programado ${audio.id} omitido (ya reproducido)`);
                continue;
            }

            try {
                console.log(`🕐 Activando audio programado: ${audio.title}`);
                await setAvisoActivo(true, audio.id, audio.file);
                await fetchAudios();

                // 🔥 NUEVO: Marcar como programado para evitar repeticiones
                lastPlayedAudios.value.add(audio.id);

            } catch (error) {
                console.error(`❌ Error activando audio programado ${audio.id}:`, error);
            }
        }
    }
};

const fetchAudios = async () => {
    try {
        const response = await api.get('audios/');
        audios.value = response.data.map(audio => ({
            ...audio,
            file: audio.file.startsWith('http') ? audio.file : `http://localhost:8000${audio.file}`
        }));
    } catch (error) {
        console.error('Error cargando audios:', error);
    }
};

const deleteAudio = async (id) => {
    if (confirm("¿Estás seguro de eliminar este audio?")) {
        try {
            if (activeAudioId.value === id) {
                await setAvisoActivo(false);
            }
            await api.delete(`audios/${id}/`);
            audios.value = audios.value.filter(a => a.id !== id);

            // 🔥 NUEVO: Limpiar de lastPlayedAudios si existe
            lastPlayedAudios.value.delete(id);

        } catch (error) {
            alert('Error al eliminar el audio');
        }
    }
};

const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleString("es-ES", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    });
};

const handleSaved = () => {
    fetchAudios();
    showModal.value = false;
};

// Inicialización
onMounted(() => {
    fetchAudios();
    checkStreamingStatus();

    // 🔥 MEJORADO: Intervalos optimizados
    scheduleInterval = setInterval(checkScheduledAudios, 2000); // Revisar cada 2 segundos
    setInterval(checkStreamingStatus, 5000); // Cada 5 segundos
    setInterval(fetchAudios, 30000); // Cada 30 segundos

    console.log('🎵 Sistema de audio inicializado');
});

onUnmounted(() => {
    if (scheduleInterval) {
        clearInterval(scheduleInterval);
    }

    stopAudioDurationCheck();
    stopStreaming();

    console.log('🛑 Sistema de audio limpiado');
});
</script>

<style scoped>
.admin-container {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

.conflict-warning {
    background: #fef3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 20px;
    color: #856404;
    font-weight: 500;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #e9ecef;
}

.page-header h1 {
    color: #e9ecef;
    font-size: 28px;
    margin: 0;
}

.page-header h1 i {
    margin-right: 10px;
    color: #3498db;
}

.header-actions {
    display: flex;
    gap: 15px;
}

.stream-button,
.upload-button {
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}

.stream-button {
    background: #e74c3c;
    color: white;
}

.stream-button:hover {
    background: #c0392b;
    transform: translateY(-2px);
}

.upload-button {
    background: #3498db;
    color: white;
}

.upload-button:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 15px;
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
}

.stat-card.live-indicator.live {
    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    color: white;
}

.stat-icon {
    font-size: 24px;
    width: 50px;
    height: 50px;
    background: #f8f9fa;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.live-indicator.live .stat-icon {
    background: rgba(255, 255, 255, 0.2);
}

.stat-info h3 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
}

.stat-info p {
    margin: 5px 0 0 0;
    color: #6c757d;
    font-size: 14px;
}

.live-indicator.live .stat-info p {
    color: rgba(255, 255, 255, 0.9);
}

.audio-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
}

.audio-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
}

.audio-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-main-content {
    padding: 20px;
    display: flex;
    align-items: flex-start;
    gap: 15px;
}

.card-icon {
    font-size: 20px;
    color: #3498db;
    margin-top: 2px;
}

.card-content {
    flex: 1;
}

.card-title {
    margin: 0 0 10px 0;
    color: #2c3e50;
    font-size: 18px;
    font-weight: 600;
}

.card-date {
    margin: 0 0 8px 0;
    color: #6c757d;
    font-size: 14px;
}

.card-date span {
    font-weight: 500;
    color: #495057;
}

.active-indicator {
    margin: 0;
    color: #27ae60;
    font-weight: 500;
    font-size: 14px;
}

.card-footer {
    padding: 15px 20px;
    background: #f8f9fa;
    border-top: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
}

.card-actions {
    display: flex;
    gap: 10px;
}

.action-button {
    padding: 6px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background: white;
    color: #6c757d;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.edit-button:hover {
    border-color: #3498db;
    color: #3498db;
}

.delete-button:hover {
    border-color: #e74c3c;
    color: #e74c3c;
}

.play-button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    background: #27ae60;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
    min-width: 120px;
    justify-content: center;
}

.play-button:hover:not(:disabled) {
    background: #219a52;
    transform: translateY(-1px);
}

.play-button.playing {
    background: #e74c3c;
}

.play-button.playing:hover:not(:disabled) {
    background: #c0392b;
}

.play-button:disabled {
    background: #6c757d;
    cursor: not-allowed;
    transform: none;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #6c757d;
}

.empty-icon {
    font-size: 64px;
    color: #bdc3c7;
    margin-bottom: 20px;
}

.empty-state h2 {
    color: #2c3e50;
    margin-bottom: 10px;
}

.empty-state p {
    margin-bottom: 30px;
    font-size: 16px;
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal-content {
    background: white;
    border-radius: 12px;
    width: 100%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
    padding: 20px 24px;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h2 {
    margin: 0;
    color: #2c3e50;
    font-size: 20px;
}

.modal-header h2 i {
    margin-right: 8px;
    color: #3498db;
}

.close-button {
    background: none;
    border: none;
    font-size: 18px;
    color: #6c757d;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
}

.close-button:hover {
    background: #f8f9fa;
    color: #2c3e50;
}

.stream-controls {
    padding: 24px;
}

.stream-status {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    background: #f8f9fa;
    border-radius: 8px;
    margin-bottom: 20px;
    font-weight: 600;
}

.stream-status.live {
    background: #ffeaa7;
    color: #e17055;
}

.status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #6c757d;
    animation: pulse 2s infinite;
}

.stream-status.live .status-indicator {
    background: #e74c3c;
    animation: pulse-live 1s infinite;
}

@keyframes pulse-live {
    0% {
        opacity: 1;
    }

    50% {
        opacity: 0.5;
    }

    100% {
        opacity: 1;
    }
}

.stream-info {
    background: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
}

.info-item:not(:last-child) {
    border-bottom: 1px solid #e9ecef;
}

.info-item label {
    font-weight: 500;
    color: #495057;
}

.info-item label i {
    margin-right: 6px;
    color: #3498db;
}

.info-item span.active {
    color: #27ae60;
    font-weight: 600;
}

.stream-toggle-button {
    width: 100%;
    padding: 16px;
    border: none;
    border-radius: 8px;
    background: #e74c3c;
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.stream-toggle-button:hover:not(:disabled) {
    background: #c0392b;
    transform: translateY(-2px);
}

.stream-toggle-button.streaming {
    background: #2ecc71;
}

.stream-toggle-button.streaming:hover:not(:disabled) {
    background: #27ae60;
}

.stream-toggle-button:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
    transform: none;
}

.button-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 16px;
}

.button-status {
    margin-top: 4px;
    font-size: 12px;
    opacity: 0.9;
}

.status-message {
    padding: 12px 16px;
    border-radius: 6px;
    background-color: #dbeafe;
    color: #1e40af;
    font-weight: 500;
    text-align: center;
    margin-bottom: 20px;
}

.stream-tips {
    background: #e8f4fd;
    padding: 16px;
    border-radius: 8px;
    border-left: 4px solid #3498db;
}

.stream-tips h4 {
    margin: 0 0 12px 0;
    color: #2c3e50;
    font-size: 14px;
}

.stream-tips h4 i {
    margin-right: 6px;
    color: #3498db;
}

.stream-tips ul {
    margin: 0;
    padding-left: 20px;
    color: #495057;
}

.stream-tips li {
    margin-bottom: 6px;
    font-size: 13px;
}

.stream-tips li i {
    margin-right: 6px;
    color: #7f8c8d;
    width: 12px;
}

@media (max-width: 768px) {
    .admin-container {
        padding: 15px;
    }

    .page-header {
        flex-direction: column;
        gap: 15px;
        align-items: flex-start;
    }

    .header-actions {
        width: 100%;
        justify-content: space-between;
    }

    .audio-grid {
        grid-template-columns: 1fr;
    }

    .card-footer {
        flex-direction: column;
        align-items: stretch;
    }

    .card-actions {
        justify-content: center;
    }
}
</style>