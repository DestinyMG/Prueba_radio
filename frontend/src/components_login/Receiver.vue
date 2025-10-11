<template>
    <div class="receiver">
        <h2>Audio en vivo</h2>
        <button @click="startListening">Activar Receptor</button>
        <audio ref="audioEl" autoplay></audio>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const audioEl = ref(null);
let ws;
let audioContext;
let source;
let queue = [];
let isPlaying = false;
let processing = false;
const listening = ref(false);

const startListening = async () => {
    if (listening.value) return;

    // Crear contexto de audio Web
    audioContext = new (window.AudioContext || window.webkitAudioContext)();

    // Conectar WebSocket al servidor
    ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
        console.log("🎧 Receptor conectado al WebSocket");
        listening.value = true;
    };

    ws.onmessage = async (event) => {
        // Guardar los datos recibidos
        queue.push(event.data);
        if (!processing) processQueue();
    };

    ws.onclose = () => {
        console.log("❌ WebSocket cerrado");
        listening.value = false;
    };

    ws.onerror = (err) => console.error("WebSocket error:", err);
};

// Procesar los chunks de audio que llegan
const processQueue = async () => {
    if (processing) return;
    processing = true;

    while (queue.length > 0 && audioContext.state !== "closed") {
        const chunk = queue.shift();
        try {
            const audioBuffer = await audioContext.decodeAudioData(await chunk.slice(0).arrayBuffer());
            const bufferSource = audioContext.createBufferSource();
            bufferSource.buffer = audioBuffer;
            bufferSource.connect(audioContext.destination);
            bufferSource.start();
        } catch (err) {
            console.error("Error procesando audio:", err);
        }
    }

    processing = false;
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
