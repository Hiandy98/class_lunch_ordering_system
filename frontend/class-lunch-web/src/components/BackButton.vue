<template>
  <button class="back-pill-btn" @click="handleBack" type="button">
    <svg class="back-icon" viewBox="0 0 24 24" fill="none" 
      stroke="currentColor" 
      stroke-width="3" 
      stroke-linecap="round" 
      stroke-linejoin="round"
    >
      <path d="M15 18l-6-6 6-6" />
    </svg>
    <span class="back-text">返回</span>
  </button>
</template>

<script setup lang="ts">
  import { useRouter } from 'vue-router'
  const props = defineProps({
    fallback: { type: String, default: '/' }
  })
  const router = useRouter()
  const handleBack = () => {
    if (window.history.state && window.history.state.back) {
      router.back()
    } else {
      router.push(props.fallback)
    }
  }
</script>

<style scoped>
  .back-pill-btn {
    position: fixed;
    top: 40px;
    left: 30px;
    z-index: 100;
    display: flex;
    align-items: center;
    padding: 6px 12px 6px 8px;
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 20px;
    color: #4b5563;
    cursor: pointer;
    transition: transform 0.1s ease, background 0.2s ease;
    -webkit-tap-highlight-color: transparent;
  }

  .back-icon {
    width: 20px;
    height: 20px;
  }

  .back-text {
    font-size: 14px;
    font-weight: 600;
    margin-left: 2px;
  }

  .back-pill-btn:active {
    transform: scale(0.9);
    background: rgba(255, 255, 255, 0.4);
  }

  .back-pill-btn:hover {
    color: #1f2937;
  }
</style>
