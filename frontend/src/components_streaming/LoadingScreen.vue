<template>
  <div class="loading-screen">
    <div class="loading-animation">
      <div class="loading-circle"></div>
      <div class="loading-logo">
        <img src="../assets/images/PORTADA.png" alt="Moonlight Radio">
      </div>
    </div>
  </div>
</template>

<script setup>
// No reactive data needed for this component
</script>

<style scoped>
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #009DDB;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  transition: opacity 0.5s ease;
}

.loading-screen.hidden {
  opacity: 0;
  pointer-events: none;
}

.loading-animation {
  position: relative;
  width: 300px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-circle {
  position: absolute;
  width: 280px;
  height: 280px;
  border: 6px solid rgba(255, 255, 255, 0.2);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
}

.loading-logo img {
  width: 250px;
  height: auto;
  animation: pulse 1.5s ease-in-out infinite alternate;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  from { transform: scale(1); }
  to { transform: scale(1.1); }
}
</style>