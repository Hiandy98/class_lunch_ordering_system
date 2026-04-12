<template>
	<BackButton />
	<div class="body">
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>
	</div>
</template>

<script setup lang="ts">
import BackButton from '@/components/BackButton.vue'
import { useRoute } from 'vue-router';
const route = useRoute();

const store_id = route.query.id;
console.log(route.query.name);
console.log(store_id);
</script>

<style scoped>
.body {
	min-height: 100%;
	width: 100%;
	margin: 0;
	background: linear-gradient(159deg, #c4e0ff, #ffe3c3);
	display: flex;
	flex-direction: column;
	align-items: center;
	overflow-y: auto;
	overflow-x: hidden;
	position: relative;
}



/* 裝飾品區 */
.decoration {
	position: fixed;
	pointer-events: none;
	border-radius: 50%;
	z-index: 1;
	filter: blur(50px);
	opacity: 0.4;
	animation: float 8s infinite alternate ease-in-out;
}

.decor-1 {
	width: 350px;
	height: 350px;
	background: var(--secondary-blue);
	top: -100px;
	left: -50px;
}

.decor-2 {
	width: 300px;
	height: 300px;
	background: var(--primary-orange);
	bottom: -50px;
	right: -50px;
	animation-delay: -2s;
}

/* 兩顆球飄動效果 */
@keyframes float {
	0% { transform: translate(0, 0) rotate(0deg); }
	100% { transform: translate(40px, 60px) rotate(10deg); }
}
</style>