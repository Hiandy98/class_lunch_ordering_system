<template>
  <div class="body">
		<BackButton />
    <div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>
		
		<div class="main-box">
			<div class="login-header">
				<h1 class="title">LunchBox</h1>
				<span class="subtitle">Login Sys</span>
			</div>

			<p class="user">使用者名稱或ID:</p>
			<el-input
				v-model="user_input"
				placeholder="Username or ID"
				class="user-input"
				clearable
			/>
			<p class="pwd">密碼:</p>
			<el-input
				v-model="pwd_input"
				type="password"
				placeholder="password"
				class="pwd-input"
				show-password
			/>
			<div class="options-row">
				<el-checkbox v-model="remember_me" class="custom-checkbox">
					保持登入
				</el-checkbox>
			</div>
			<p :style="{ color: textColor }" class="err-msg">{{ err_message }}</p>
			<el-button :loading="loading" type="primary" round class="login-btn" @click="handle_login()">Login</el-button>
		</div>
  </div>

	<div class="footer-info">V0.0 Bate</div>

</template>

<script setup lang="ts">
	import BackButton from '@/components/BackButton.vue'
	import { ref } from 'vue'
	import router from '@/router';
	import axios from 'axios';

	const user_input = ref('');
	const pwd_input = ref('');
	const loading = ref(false)
	const err_message = ref<string>('');
	const textColor = ref<string>('red');
	const remember_me = ref(true);
	const can_use = ref<boolean>(true);

	function err_msg(msg: string): void {
		setTimeout(() => {
			err_message.value = "";
		}, 5000);
		textColor.value = 'red';
		err_message.value = msg;
	};

	const handle_login = async () => {
		if (!can_use.value) {
			err_msg("請求過於頻繁，請稍後再試");
			return;
		}

  	can_use.value = false;
		err_message.value = "";

		setTimeout(() => {
        can_use.value = true;
    }, 5000);

		if (!user_input.value || !pwd_input.value) {
			err_msg("請輸入帳號與密碼!");
			return;
		};

		loading.value = true;
		textColor.value = 'green';
		err_message.value = "登入中..."

		try {
			const response = await axios.post(
				'/api/v1/auth/login',
				null,
				{
					params: {
						user: user_input.value,
						password: pwd_input.value,
						remember_me: remember_me.value,
					},
					withCredentials: true
				}
			);


			if (response.data.state === '登入成功') {
				
				const isIOSDevice = /iPad|iPhone|iPod/.test(navigator.userAgent) || 
						(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
				
				if (isIOSDevice && response.data.token) {
					localStorage.setItem('ios_token', response.data.token)
				}

				router.push('/stores');
			}

		} catch (error) {
			if (!axios.isAxiosError(error)) {
				return
			}
			if (!error.response) {
				if (error.request) {
					err_msg('無法連線至伺服器');
				} else {
					console.error('請求設定錯誤', error.message);
				}
				
				return;
			}

			const status = error.response.status;
			const detail = error.response.data?.detail;

			switch (status) {
				case 401:
					err_msg(detail || '帳號或密碼錯誤');
					break;
				case 502:
					err_msg('伺服器維護中 (502)，請稍後再試');
					break;
				default:
					err_msg(`系統錯誤 (${status})`);
			}
		} finally {
			loading.value = false;
		}
	}
</script>


<style scoped>
.body {
	min-height: 100vh;
	width: 100%;
	box-sizing: border-box;
	margin: 0;
	background: #ffd9ad;
	background: -webkit-linear-gradient(159deg, #d6eaff, #ffd9ad);
	background: linear-gradient(159deg, #d6eaff,  #ffd9ad);
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

.main-box {
	background: rgba(255, 255, 255, 0.65);
	backdrop-filter: blur(10px);
	-webkit-backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.8);
	box-shadow: 
		0 4px 15px rgba(0, 0, 0, 0.05),
		inset 0 0 2px rgba(255, 255, 255, 0.5);
	height: auto;
	border-radius: 20px;
	z-index: 100;
	width: 85%;
	max-width: 400px;
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 50px 40px;
	margin-top: -8vh;
}

.login-header {
	margin-bottom: 30px;
	text-align: center;
}

.title {
	color: var(--primary-orange);
		font-size: 2.2rem;
	font-weight: 800;
	margin: 0;
	letter-spacing: -1px;
}

.subtitle {
	font-size: 0.9rem;
	color: #888;
	font-weight: 500;
	display: block;
	margin-top: -5px;
	letter-spacing: 3px;
}


.user, .pwd {
	font-size: 0.95rem;
	color: #555;
	font-weight: 600;
	text-align: left;
	align-self: flex-start;
	padding-left: 10px;
	letter-spacing: 2px;
	margin: 15px 0 8px 0;
}

.user-input, .pwd-input {
	width: 240px;
	height: 40px;
}

.el-input {
		--el-input-border-radius: 10px;
		margin-bottom: 5px;
}

.login-btn {
	margin-top: 10px;
	background: linear-gradient(135deg, #ff9d2f, #ff6b00);
	box-shadow: 0 8px 20px rgba(255, 107, 0, 0.3);
	margin-bottom: 15px;
	border: none;
	width: 140px;
	height: 35px;
	font-weight: bold;
	font-size: 1.1em;
	cursor: pointer;
	transition: transform 0.1s;
}

.login-btn:active {
		transform: scale(0.95);
}

.footer-info {
	position: absolute;
	font-size: 12px;
	color: #666;
	bottom: 20px;
	left: 50%;
	transform: translateX(-50%);
}

.err-msg {
	margin-top: 30px;
	height: 30px;
}

</style>
