<template>
    <div class="base-layout">
        <Sidebar />

        <div class="main-content-wrapper">
            <Header />

            <main class="content-area">
                <slot></slot>
            </main>
        </div>
    </div>
</template>

<script setup>
import Sidebar from '../components_login/Sidebar.vue';
import Header from '../components_login/Header.vue';
</script>

<style scoped>
.base-layout {
    display: flex;
    min-height: 100vh;
    background-color: #e3f2fd;
    /* Color de fondo azul claro general */
}

.main-content-wrapper {
    flex-grow: 1;
    /* Ocupa el espacio restante */
    display: flex;
    flex-direction: column;
    padding: 0 30px;
}

.content-area {
    flex-grow: 1;
    /* Ocupa el espacio vertical restante */
    width: 100%;
}
</style>