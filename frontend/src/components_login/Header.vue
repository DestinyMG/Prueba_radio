<template>
    <header class="app-header">
        <div class="logo">
            🔵 Kiero Radio
        </div>
        <div class="search-bar">
            <span class="search-icon">🔍</span>
            <input type="text" placeholder="Buscar shows, canciones..." />
        </div>
    </header>
</template>

<script setup>
// No se necesita lógica de script para este ejemplo de diseño
</script>

<style scoped>
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    width: 100%;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #0277bd;
}

.search-bar {
    display: flex;
    align-items: center;
    background-color: #ffffff;
    border-radius: 50px;
    padding: 8px 15px;
    width: 400px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.search-icon {
    margin-right: 10px;
    color: #999;
}

.search-bar input {
    border: none;
    outline: none;
    width: 100%;
    background-color: transparent;
    font-size: 1rem;
}
</style>