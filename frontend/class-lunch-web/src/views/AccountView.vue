<template>
	<div class="body">
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>
		<div class="header">
			<BackButton />
			<div class="logo">LunchBox</div>
		</div>
		<div class="user-card">
			
		</div>
		<div class="footer-info">V0.0 Beta</div>
	</div>
</template>

<script setup lang="ts">
import BackButton from '@/components/BackButton.vue'

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

@keyframes float {
	0% { transform: translate(0, 0) rotate(0deg); }
	100% { transform: translate(40px, 60px) rotate(10deg); }
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 10px 20px;
	width: 100%;
	position: absolute;
	top: 0;
	z-index: 200;
}

.logo {
	color: var(--primary-orange);
	font-size: 2rem;
	font-weight: 900;
	margin-top: 20px;
	margin-left: 100px;
	z-index: 101;
	letter-spacing: -1px;
	text-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.footer-info {
	position: absolute;
	font-size: 12px;
	color: #666;
	bottom: 20px;
	left: 50%;
	transform: translateX(-50%);
}

.user-card  {
	background: rgba(255, 255, 255, 0.65);
	backdrop-filter: blur(10px);
	-webkit-backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.8);
	box-shadow: 
		0 4px 15px rgba(0, 0, 0, 0.05),
		inset 0 0 2px rgba(255, 255, 255, 0.5);
	height: 70vh;
	border-radius: 20px;
	z-index: 2;
	width: 85%;
	max-width: 400px;
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-top: 15vh;
	padding: 50px 40px;
}


</style>