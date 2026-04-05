<template>
	<div class="decoration decor-1"></div>
	<div class="decoration decor-2"></div>

	<div class="main-container">
		<h1 class="logo-text">LunchBox</h1>
		<p class="system-desc">KSHS108-訂餐管理系統</p>
		<button class="login-btn" @click="goToSystem()">登 入 系 統</button>
		<a href="#" class="sub-link">忘記密碼？</a>
	</div>

	<div class="footer-info">
		V0.0 Bate
	</div>
</template>

<script setup lang="ts">
	import { ref, reactive } from 'vue';

	const containerStyle = reactive({
		opacity: '1',
		transform: 'scale(1)',
		transition: '0.5s'
	});

	const goToSystem = (): void => {
		containerStyle.opacity = '0';
		containerStyle.transform = 'scale(0.9)';
		
		setTimeout(() => {
			alert('正在進入系統...');
		}, 500);
	};
</script>

<style>
	:root {
		--primary-orange: #FF8A00;
		--secondary-blue: #4A90E2;
		--bg-light: #F9FAFC;
	}

	body {
		background: #ffd9ad; 
		background: -webkit-linear-gradient(159deg, #ffd9ad, #d6eaff); 
		background: linear-gradient(159deg, #ffd9ad, #d6eaff);
		display: flex;
		justify-content: center;
		align-items: center;
		overflow: hidden;
		position: relative;
	}

	/* 裝飾品區 */
	.decoration {
		position: absolute;
		border-radius: 50%;
		z-index: 1;
		filter: blur(60px);
		opacity: 0.4;
		animation: float 8s infinite alternate ease-in-out;
	}

	.decor-1 {
		width: 350px;
		height: 350px;
		background: var(--primary-orange);
		top: -100px;
		left: -50px;
	}

	.decor-2 {
		width: 300px;
		height: 300px;
		background: var(--secondary-blue);
		bottom: -50px;
		right: -50px;
		animation-delay: 2s;
	}

	/* 兩顆球飄動效果 */
	@keyframes float {
		from { transform: translate(0, 0); }
		to { transform: translate(30px, 50px); }
	}

	.main-container {
		position: relative;
		z-index: 10;
		text-align: center;
		padding: 20px;
		width: 100%;
		max-width: 400px;
	}

	.logo-text {
		font-size: 48px;
		font-weight: 800;
		color: var(--primary-orange);
		letter-spacing: -1px;
		margin-bottom: 10px;
		text-shadow: 0 5px 20px rgba(255, 138, 0, 0.2);
	}

	.system-desc {
		color: #666;
		font-size: 16px;
		margin-top: 30px;
		margin-bottom: 40px;
		letter-spacing: 2px;
	}

	.login-btn {
		background: var(--primary-orange);
		color: white;
		text-decoration: none;
		display: inline-block;
		width: 100%;
		padding: 18px 0;
		border-radius: 25px;
		font-size: 1.2em;
		font-weight: 700;
		box-shadow: 0 10px 25px rgba(255, 138, 0, 0.3);
		cursor: pointer;
		border: none;
		transition: all 0.3s ease;
	}

	.login-btn:hover {
		transform: translateY(-3px);
		box-shadow: 0 15px 30px rgba(255, 138, 0, 0.4);
		filter: brightness(1.05);
	}

	.login-btn:active {
		transform: scale(0.95);
	}

	.sub-link {
		display: block;
		margin-top: 25px;
		color: var(--secondary-blue);
		font-size: 14px;
		text-decoration: none;
		font-weight: 500;
	}

	.footer-info {
		position: absolute;
		font-size: 12px;
		color: #666;
  	bottom: 20px;
  	left: 50%;
  	transform: translateX(-50%);
	}
	
</style>