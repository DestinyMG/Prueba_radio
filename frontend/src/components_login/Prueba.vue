<template>
    <BaseAdmin>
        <div class="mi-contenido">
            <h1>¡Hola, este es mi contenido!</h1>
            <p>Aquí puedo agregar la lógica de mi página, como la sección de música que se ve en la imagen.</p>
        </div>
    </BaseAdmin>
</template>

<script setup>
import BaseAdmin from './BaseAdmin.vue';
</script>

<style>
/* Estilos globales si son necesarios */
body {
    margin: 0;
    font-family: sans-serif;
}

.mi-contenido {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
}
</style>