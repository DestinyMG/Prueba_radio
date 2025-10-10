<template>
  <div class="show-card" @click="handleClick">
    <img :src="show.image" :alt="show.title" class="show-image">
    <div class="show-content">
      <h3 class="show-name">{{ show.title }}</h3>
      <p class="show-description">{{ show.description }}</p>
      <div class="play-btn" @click.stop="playShow">
        <i :class="isPlaying ? 'fas fa-pause' : 'fas fa-play'"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: {
    type: Object,
    required: true
  },
  isPlaying: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['play'])

const playShow = () => {
  emit('play', props.show)
}

const handleClick = () => {
  playShow()
}
</script>

<style scoped>
.show-card {
  flex: 0 0 220px;
  scroll-snap-align: start;
  background-color: rgba(255, 255, 255, 0.98);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  border: 1px solid #E2E8F0;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 125, 184, 0.1);
}

.show-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 125, 184, 0.15);
  border-color: #009DDB;
}

.show-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.show-card:hover .show-image {
  transform: scale(1.03);
}

.show-content {
  padding: 15px;
}

.show-name {
  font-weight: 600;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #2D3748;
}

.show-description {
  color: #5F6C7B;
  font-size: 13px;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.play-btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #009DDB, #007DB8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: auto;
  opacity: 1;
  transform: translateY(10px);
  color: white;
}

.show-card:hover .play-btn {
  opacity: 1;
  transform: translateY(0);
}

.play-btn:hover {
  transform: scale(1.05) translateY(0) !important;
  box-shadow: 0 0 15px rgba(0, 157, 219, 0.3);
}

@media (max-width: 1024px) {
  .show-card {
    flex: 0 0 180px;
  }
}

@media (max-width: 768px) {
  .show-card {
    flex: 0 0 150px;
  }
}

@media (max-width: 480px) {
  .show-card {
    flex: 0 0 130px;
  }
}
</style>