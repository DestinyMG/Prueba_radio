<template>
    <div class="receiver">
        <h2>Audio en vivo</h2>
        <button @click="startListening">Activar Receptor</button>
        <audio ref="audio" autoplay></audio>
    </div>
</template>

<script setup>
import { ref } from 'vue';

let ws;
const listening = ref(false);
const audioRef = ref(null);

const startListening = async () => {
    if (listening.value) return;

    ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
        console.log("Receptor conectado al WebSocket");
        listening.value = true;
    };

    ws.onmessage = (event) => {
        const blob = new Blob([event.data], { type: 'audio/webm; codecs=opus' });
        const url = URL.createObjectURL(blob);

        // Reproducir audio directamente
        const audio = audioRef.value;
        audio.src = url;
        audio.play().catch(err => console.warn("Error al reproducir:", err));
    };
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
