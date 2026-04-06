<template>
	<div class="body">
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>

		<div class="main-container" :style="containerStyle">
			<h1 class="logo-text">LunchBox</h1>
			<p class="system-desc">KSHS108-訂餐管理系統</p>
			<button class="login-btn" @click="goToSystem()">進入系統</button>
			<button class="forget-pwd">忘記密碼?</button>
		</div>

		<div class="footer-info">V0.0 Bate</div>
	</div>
</template>

<script setup lang="ts">
	import router from '@/router';
	import { ref, reactive } from 'vue';
	import axios from 'axios';

	const containerStyle = reactive({
		opacity: '1',
		transform: 'scale(1)',
		transition: '0.5s'
	});

	const goToSystem = (): void => {
		containerStyle.opacity = '0';
		containerStyle.transform = 'scale(0.9)';
		
		setTimeout(() => {
			handleLoginFlow();
		}, 150);
	};

	const handleLoginFlow = async () => {
  	try {
			const response = await axios.get('/api/v1/auth/verify', {
				withCredentials: true
			});

			// 200 (Success)
			const user = response.data;
			console.log(`✅ 驗證成功：${user.display_name}`);
			router.push('/stores');
			
		} catch (error: any) {
			if (!error.response) {
				if (error.request) {
						console.error('網路連線失敗，請檢查 API 網址是否正確');
						alert('無法連線至伺服器，請檢查網路');
						return;
				}
				console.error('請求設定錯誤', error.message);
				return;
			}
			const status = error.response.status;
			
			if (status === 401) {
					// 401 Unauthorized: 無憑證或已過期
					console.warn('身分驗證失敗，導向登入頁');
					router.push('/login');
					return;
			}

			if (status === 502) {
					// 502 Bad Gateway: 後端程式沒啟動、Nginx 轉發失敗或崩潰
					alert('伺服器維護中 (502)，請稍後再試');
					return;
			}

		// 其他錯誤碼
			console.error(`發生錯誤：${status}`, error.response.data);
		}
	};

</script>

<style scoped>
	.body {
		min-height: 100vh;
		width: 100%;
		box-sizing: border-box;
		margin: 0;
		background: #ffd9ad;
		background: -webkit-linear-gradient(159deg, #ffd9ad, #d6eaff);
		background: linear-gradient(159deg, #ffd9ad, #d6eaff);
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
		filter: blur(40px);
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
		animation-delay: -2s;
	}

	/* 兩顆球飄動效果 */
	@keyframes float {
		0% { transform: translate(0, 0) rotate(0deg); }
		100% { transform: translate(40px, 60px) rotate(10deg); }
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
		filter: drop-shadow(0 4px 12px rgba(255, 138, 0, 0.2));
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
		letter-spacing: 10px;
		color: white;
		text-decoration: none;
		display: inline-block;
		width: 80%;
		padding: 18px 0;
		border-radius: 30px;
		font-size: 1.2em;
		font-weight: 700;
		box-shadow: 0 10px 25px rgba(255, 138, 0, 0.3);
		cursor: pointer;
		border: none;
		transition: all 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275)
	}

	.login-btn:hover {
		transform: translateY(-3px);
		box-shadow: 0 15px 30px rgba(255, 138, 0, 0.4);
		filter: brightness(1.05);
	}

	.login-btn:active {
		transform: scale(0.95);
	}

	.forget-pwd {
		display: block;
		margin: 25px auto 0;
		color: var(--secondary-blue);
		font-size: 14px;
		text-decoration: none;
		font-weight: 500;
		background-color: transparent;
		border: none;
		transition: all 0.1s ease;
	}

	.forget-pwd:active {
		font-size: small;
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