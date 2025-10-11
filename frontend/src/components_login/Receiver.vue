<template>
    <div class="receiver">
        <h2>Audio en vivo</h2>
        <button @click="startListening">Activar Receptor</button>
        <audio ref="audioEl" autoplay></audio>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const audioEl = ref(null);
let ws;
let mediaSource;
let sourceBuffer;
let queue = [];
let isAppending = false;
const listening = ref(false);

const startListening = async () => {
    if (listening.value) return;

    mediaSource = new MediaSource();
    audioEl.value.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', () => {
        sourceBuffer = mediaSource.addSourceBuffer('audio/webm; codecs="opus"');
        sourceBuffer.mode = 'sequence';

        sourceBuffer.addEventListener('updateend', () => {
            isAppending = false;
            appendNextChunk();
        });
    });

    // Conectar WebSocket
    ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
        console.log("Receptor conectado al WebSocket");
        listening.value = true;
    };

    ws.onmessage = (event) => {
        queue.push(event.data);
        appendNextChunk();
    };

    ws.onclose = () => console.log("WebSocket cerrado");
    ws.onerror = (err) => console.error("WebSocket error:", err);
};

// Función para reproducir chunks de audio en MediaSource
const appendNextChunk = () => {
    if (!sourceBuffer || isAppending || queue.length === 0) return;

    isAppending = true;
    const chunk = queue.shift();
    try {
        sourceBuffer.appendBuffer(new Uint8Array(chunk));
    } catch (err) {
        console.error("Error appending buffer:", err);
        isAppending = false;
        queue.unshift(chunk); // reintentar
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
