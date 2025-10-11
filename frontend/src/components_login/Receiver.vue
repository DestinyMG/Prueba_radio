<template>
    <div class="receiver">
        <h2>Audio en vivo</h2>
        <button @click="startListening">Activar Receptor</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';

let ws;
let audioContext;
let audioQueue = [];
let isPlaying = false;
const listening = ref(false);

const startListening = async () => {
    if (listening.value) return;

    // Crear AudioContext y forzar resume
    audioContext = new AudioContext();
    await audioContext.resume();

    ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
        console.log("Receptor conectado al WebSocket");
        listening.value = true;
    };

    ws.onmessage = (event) => {
        if (event.data.byteLength > 0) {
            audioQueue.push(event.data);
            if (!isPlaying) playQueue();
        }
    };
};

const playQueue = () => {
    if (audioQueue.length === 0) {
        isPlaying = false;
        return;
    }

    isPlaying = true;

    const buffer = audioQueue.shift();
    const int16 = new Int16Array(buffer);
    const float32 = new Float32Array(int16.length);

    // Convertir int16 -> float32
    for (let i = 0; i < int16.length; i++) {
        float32[i] = int16[i] < 0 ? int16[i] / 0x8000 : int16[i] / 0x7fff;
    }

    // Crear AudioBuffer
    const audioBuffer = audioContext.createBuffer(
        1,
        float32.length,
        audioContext.sampleRate
    );
    audioBuffer.getChannelData(0).set(float32);

    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();

    source.onended = () => playQueue();
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
