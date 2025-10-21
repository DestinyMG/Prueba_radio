<template>
    <div>
        <audio v-if="aviso?.activo && aviso?.audio_file" :src="aviso.audio_file" autoplay ref="audioPlayer"></audio>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";

const aviso = ref(null);
const audioPlayer = ref(null);

onMounted(async () => {
    try {
        const response = await fetch("http://localhost:8000/api2/aviso/2/");
        aviso.value = await response.json();

        if (aviso.value.activo && aviso.value.audio_file) {
            // Esperamos a que Vue monte el <audio> en el DOM
            await nextTick();

            if (audioPlayer.value) {
                audioPlayer.value.play().catch((err) => {
                    console.error(
                        "Error reproduciendo el audio (necesita interacción del usuario):",
                        err
                    );
                });
            }
        }
    } catch (error) {
        console.error("Error consultando el aviso:", error);
    }
});
</script>

<style>
audio {
    display: none;
    /* oculto, sin controles */
}
</style>
