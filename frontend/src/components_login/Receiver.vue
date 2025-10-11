<template>
    <div class="receiver">
        <h2>Audio en vivo</h2>
        <button @click="startListening">Activar Receptor</button>
    </div>
</template>

<script setup>
let ws;
let audioContext;
let bufferQueue = [];
let isPlaying = false;

const startListening = async () => {
    audioContext = new AudioContext();

    ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
    ws.binaryType = "arraybuffer";

    ws.onopen = () => console.log("Receptor conectado al WebSocket");

    ws.onmessage = (event) => {
        bufferQueue.push(event.data);
        if (!isPlaying) processQueue();
    };
};

const processQueue = () => {
    if (bufferQueue.length === 0) {
        isPlaying = false;
        return;
    }
    isPlaying = true;

    const arrayBuffer = bufferQueue.shift();
    const int16Array = new Int16Array(arrayBuffer);
    const float32Array = new Float32Array(int16Array.length);
    for (let i = 0; i < int16Array.length; i++) {
        float32Array[i] = int16Array[i] / 0x7fff;
    }

    const audioBuffer = audioContext.createBuffer(1, float32Array.length, audioContext.sampleRate);
    audioBuffer.getChannelData(0).set(float32Array);

    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination); // conectar directamente al audio del usuario
    source.start();

    source.onended = () => processQueue();
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
