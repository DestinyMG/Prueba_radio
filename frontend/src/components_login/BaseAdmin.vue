<template>
    <div class="base-layout">
        <div class="main-content-wrapper">
            <Header />
            
            <div class="scrollable-content">
                <main class="content-area">
                    <slot></slot>
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import Header from '../components_login/Header.vue';
</script>

<style scoped>
.base-layout {
    display: flex;
    min-height: 100vh;
    background: linear-gradient(135deg, #1466e1 0%, #0d4fb5 100%);
    overflow-x: hidden; /* ← Elimina espacio blanco lateral */
    width: 100%;
}

.main-content-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    background: linear-gradient(135deg, #1466e1 0%, #0d4fb5 100%);
    width: 100%;
    overflow-x: hidden; /* ← Elimina espacio blanco lateral */
}

/* Contenido desplazable */
.scrollable-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden; /* ← IMPORTANTE: Elimina scroll horizontal */
    padding: 0 30px;
    background: linear-gradient(135deg, #1466e1 0%, #0d4fb5 100%);
    width: 100%;
    max-width: 100%; /* ← Previene desbordamiento */
    box-sizing: border-box; /* ← Incluye padding en el ancho total */
}

.content-area {
    width: 100%;
    min-height: 100%;
    max-width: 100%; /* ← Previene desbordamiento */
}

/* Responsive - MANTIENE MARGENES */
@media (max-width: 1024px) {
    .scrollable-content {
        padding: 0 25px;
    }
}

@media (max-width: 768px) {
    .scrollable-content {
        padding: 0 20px; /* Mantiene margen, no queda pegado */
    }
}

@media (max-width: 480px) {
    .scrollable-content {
        padding: 0 16px; /* Mantiene margen, no queda pegado */
    }
}

@media (max-width: 375px) {
    .scrollable-content {
        padding: 0 14px; /* Mantiene margen mínimo */
    }
}

@media (max-width: 320px) {
    .scrollable-content {
        padding: 0 12px; /* Mantiene margen mínimo */
    }
}
</style>