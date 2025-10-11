<template>
    <div class="transmitter">
        <button @click="toggleTransmit">
            {{ transmitting ? 'Detener Transmisión' : 'Transmitir' }}
        </button>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const transmitting = ref(false);
let ws;
let mediaRecorder;
let stream;

const toggleTransmit = async () => {
    if (!transmitting.value) {
        ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
        ws.binaryType = "arraybuffer";

        ws.onopen = async () => {
            console.log("Conectado al WebSocket");

            // Capturar audio
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            // Usar MediaRecorder para enviar audio en chunks
            mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm; codecs=opus' });

            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0 && ws.readyState === WebSocket.OPEN) {
                    e.data.arrayBuffer().then(buffer => ws.send(buffer));
                }
            };

            mediaRecorder.start(250); // enviar cada 250ms
            transmitting.value = true;
        };
    } else {
        if (mediaRecorder) mediaRecorder.stop();
        if (stream) stream.getTracks().forEach(track => track.stop());
        if (ws) ws.close();
        transmitting.value = false;
    }
};
</script>


<style scoped>
.transmitter {
    display: flex;
    justify-content: center;
    margin: 20px;
}

button {
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

button:hover {
    background-color: #2563eb;
}
</style>
