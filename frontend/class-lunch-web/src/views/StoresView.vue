<template>
	<div class="body">
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>

		<div class="top-box">
			<div class="logo">LunchBox</div>
		</div>
		
		<div class="main-box">
			<div class="outside-list">
				<div 
					v-for="item in lunchItems" 
					:key="item.id" 
					class="card"
				>
					<h3>{{ item.name }}</h3>
				</div>
			</div>
			<div class="inside-list">
				<div class="inside-item"></div>
			</div>
		</div>

	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const lunchItems = ref([
  { id: 1, name: '排骨便當', price: 100, description: '經典台式風味' },
  { id: 2, name: '雞腿便當', price: 120, description: '酥脆大雞腿' },
  { id: 3, name: '鯖魚便當', price: 110, description: '新鮮現烤鯖魚' }
]);
</script>

<style scoped>
.body {
	min-height: 100vh;
	width: 100%;
	box-sizing: border-box;
	margin: 0;
	background: #ffd9ad;
	background: -webkit-linear-gradient(159deg, #c4e0ff, #ffe3c3);
	background: linear-gradient(159deg, #c4e0ff,  #ffe3c3);
	display: flex;
	justify-content: center;
	align-items: flex-start;
	padding-top: 20vh;
	overflow: hidden;
	position: relative;
}

/* 裝飾品區 */
.decoration {
	position: absolute;
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

.top-box {
	position: absolute;
	top: 0px;
	display: flex;
	align-items: center;
	width: 100%;
	height: 10vh;
	z-index: 101;
}


.logo {
	color: var(--primary-orange);
	font-size: 2.6rem;
	font-weight: 900;
	margin-left: 30px;
	margin-top: 20px;
	letter-spacing: -1px;
	text-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}



</style>