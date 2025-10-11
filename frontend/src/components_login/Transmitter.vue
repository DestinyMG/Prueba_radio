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
let audioContext;
let processor;
let source;
let stream;

const toggleTransmit = async () => {
    if (!transmitting.value) {
        ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
        ws.binaryType = "arraybuffer";

        ws.onopen = () => console.log("Conectado al WebSocket");

        // Capturar audio
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new AudioContext();
        source = audioContext.createMediaStreamSource(stream);

        // ScriptProcessorNode para enviar audio en chunks
        processor = audioContext.createScriptProcessor(4096, 1, 1);
        processor.onaudioprocess = (e) => {
            const input = e.inputBuffer.getChannelData(0);
            const buffer = new ArrayBuffer(input.length * 2);
            const view = new DataView(buffer);
            for (let i = 0; i < input.length; i++) {
                let s = Math.max(-1, Math.min(1, input[i]));
                view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
            }
            if (ws.readyState === WebSocket.OPEN) ws.send(buffer);
        };

        source.connect(processor);
        // No conectar processor a audioContext.destination para evitar reproducción local
        transmitting.value = true;
    } else {
        processor.disconnect();
        source.disconnect();
        stream.getTracks().forEach(track => track.stop());
        ws.close();
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
