<template>
    <div class="receiver">
        <h2>Audio en vivo</h2>
        <button @click="activateAudio">
            {{ audioUnlocked ? 'Receptor Activado' : 'Activar Receptor' }}
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let ws;
let audioContext;
let bufferQueue = [];
let isPlaying = false;
const audioUnlocked = ref(false);

onMounted(() => {
    // 1️⃣ Crear contexto de audio suspendido (necesario por políticas del navegador)
    audioContext = new AudioContext();
    audioContext.suspend();

    // 2️⃣ Conectar WebSocket apenas inicia el componente
    ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
    ws.binaryType = "arraybuffer"; // muy importante

    ws.onopen = () => console.log("Receptor conectado al WebSocket ✅");

    ws.onmessage = (event) => {
        try {
            // Asegurarnos de que los datos son ArrayBuffer
            const data =
                event.data instanceof ArrayBuffer
                    ? event.data
                    : event.data.arrayBuffer
                        ? event.data.arrayBuffer()
                        : null;

            if (!data) return;

            // Si viene como promesa (caso raro en algunos navegadores)
            if (data instanceof Promise) {
                data.then((buf) => {
                    bufferQueue.push(buf);
                    if (audioUnlocked.value && !isPlaying) processQueue();
                });
            } else {
                bufferQueue.push(data);
                if (audioUnlocked.value && !isPlaying) processQueue();
            }
        } catch (err) {
            console.error("Error procesando audio:", err);
        }
    };
});

// 🔊 El usuario activa el receptor
const activateAudio = async () => {
    if (!audioUnlocked.value) {
        await audioContext.resume();
        audioUnlocked.value = true;
        console.log("Audio desbloqueado ✅");

        if (bufferQueue.length > 0 && !isPlaying) {
            processQueue();
        }
    }
};

// 🔁 Procesa y reproduce cada chunk de audio recibido
const processQueue = () => {
    if (bufferQueue.length === 0) {
        isPlaying = false;
        return;
    }

    isPlaying = true;
    const arrayBuffer = bufferQueue.shift();

    try {
        const int16Array = new Int16Array(arrayBuffer);
        const float32Array = new Float32Array(int16Array.length);
        for (let i = 0; i < int16Array.length; i++) {
            float32Array[i] = int16Array[i] / 0x7fff;
        }

        const audioBuffer = audioContext.createBuffer(
            1,
            float32Array.length,
            audioContext.sampleRate
        );
        audioBuffer.getChannelData(0).set(float32Array);

        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioContext.destination);
        source.start();

        source.onended = () => processQueue();
    } catch (err) {
        console.error("Error decodificando audio:", err);
        isPlaying = false;
    }
};
</script>



<style scoped>
.receiver {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}
</style>

<style scoped>
.receiver {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}
</style>


<style scoped>
.receiver {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}
</style>


<style scoped>
.receiver {
    margin: 20px;
    text-align: center;
}

audio {
    margin-top: 12px;
    width: 80%;
}
</style>
