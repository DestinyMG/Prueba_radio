<template>
    <div class="receiver">
        <h2>Audio en vivo</h2>
        <button @click="startListening">Activar Receptor</button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

let ws;
const listening = ref(false);
let audioContext;
let queue = [];
let isPlaying = false;

const startListening = async () => {
    if (listening.value) return;

    audioContext = new AudioContext();
    await audioContext.resume();

    ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
        console.log("Receptor conectado al WebSocket");
        listening.value = true;
    };

    ws.onmessage = async (event) => {
        if (event.data.byteLength > 0) {
            queue.push(event.data);
            if (!isPlaying) playQueue();
        }
    };
};

const playQueue = async () => {
    if (queue.length === 0) {
        isPlaying = false;
        return;
    }

    isPlaying = true;
    const buffer = queue.shift();
    try {
        const audioBuffer = await audioContext.decodeAudioData(buffer);
        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioContext.destination);
        source.start();

        source.onended = () => playQueue();
    } catch (err) {
        console.error("Error decodificando audio:", err);
        // Continuar con siguiente chunk
        playQueue();
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
