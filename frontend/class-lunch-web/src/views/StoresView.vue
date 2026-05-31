<template>
	<div class="body">
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>

		<div class="top-box">
			<div class="logo">LunchBox</div>
			<div class="user-config-tag" @click="goToAccount()">
				<div class="user-meta" v-if="userInfo">
					<span class="greeting">ACCOUNT</span>
					<span class="nickname">{{ userInfo.display_name }}</span>
				</div>
				<div class="user-meta" v-else>
					<span class="nickname">load...</span>
				</div>
				<div class="config-icon-box">
					<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
						<path d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
						<path d="M19.4 15
							a1.65 1.65 0 00.33 1.82
							l.06.06
							a2 2 0 010 2.83 2 2 0 01-2.83 0
							l-.06-.06
							a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51
							V21
							a2 2 0 01-2 2 2 2 0 01-2-2
							v-.09
							A1.65 1.65 0 009 19.4
							a1.65 1.65 0 00-1.82.33
							l-.06.06
							a2 2 0 01-2.83 0 2 2 0 010-2.83
							l.06-.06
							a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1
							H3
							a2 2 0 01-2-2 2 2 0 012-2
							h.09
							A1.65 1.65 0 004.6 9
							a1.65 1.65 0 00-.33-1.82
							l-.06-.06
							a2 2 0 010-2.83 2 2 0 012.83 0
							l.06.06
							a1.65 1.65 0 001.82.33
							H9
							a1.65 1.65 0 001-1.51
							V3
							a2 2 0 012-2 2 2 0 012 2
							v.09
							a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33
							l.06-.06
							a2 2 0 012.83 0 2 2 0 010 2.83
							l-.06.06
							a1.65 1.65 0 00-.33 1.82
							V9
							a1.65 1.65 0 001.51 1
							H21
							a2 2 0 012 2 2 2 0 01-2 2
							h-.09
							a1.65 1.65 0 00-1.51 1z" />
					</svg>
				</div>
			</div>
		</div>
		
		<div class="main-box">
			<div class="store-list">
				<button
					v-for="item in todayStore"
					:key="item.id"
					class="card"
					:class="{ 'inactive': !item.is_active }"
					@click="goToMenu(item)"
				>
					<div class="card-content">
						<div class="info-section">
							<div class="card-header">
								<h3 :class="item.is_active ? 'status-open' : 'status-closed'">
									{{ item.name }}
								</h3>
							</div>
						
							<div class="card-body">
								<p class="deadline">
									截止時間：
									{{ item.deadline ? new Date(item.deadline).toLocaleTimeString('zh-TW', { hour12: false, hour: '2-digit', minute: '2-digit' }) : '未設定' }}
								</p>
							</div>
						</div>
						<div class="arrow-icon">
							<svg viewBox="0 0 24 24">
								<path d="M8.5 5L15.5 12L8.5 19" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none" />
							</svg>
						</div>
        	</div>
				</button>
			<div v-if="isLoading && todayStore.length === 0" class="empty-state">載入中...</div>
			<div v-else-if="!isLoading && todayStore.length === 0" class="empty-state">目前沒有開放中的餐廳</div>
			</div>
		</div>
		<button class="fab-btn" @click="goToCreateStore()">
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
				<line x1="12" y1="5" x2="12" y2="19"></line>
				<line x1="5" y1="12" x2="19" y2="12"></line>
			</svg>
    </button>

		<div class="footer-info">V0.0 Beta</div>
	</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue';
	import axios from 'axios';
	import router from '@/router';

	interface Store {
		id: string;
		name: string;
		is_today_store: boolean;
		is_active: boolean;
		deadline?: string | null;
	}
	
	interface UserInfo {
		user_id: string;
		display_name: string;
		role: string;
	}

	const cachedUser = localStorage.getItem('lunchbox_user');
	const cachedStores = localStorage.getItem('lunchbox_today_stores');

	const userInfo = ref<UserInfo | null>(cachedUser ? JSON.parse(cachedUser) : null);
	const todayStore = ref<Store[]>(cachedStores ? JSON.parse(cachedStores) : []);
	const isLoading = ref(true);
	
	async function verifyUser() {
		try {
			const response = await axios.get('/api/v1/auth/verify');
			userInfo.value = response.data;
			localStorage.setItem('lunchbox_user', JSON.stringify(response.data));
		} catch (error) {
			if (!axios.isAxiosError(error)) {
				return;
			}
			console.error('驗證失敗或 Token 已過期');
			userInfo.value = null;
			localStorage.removeItem('lunchbox_user');
		}
	}

	async function get_today_store() {
		isLoading.value = true;
		try {
			const response = await axios.get('/api/v1/store/list/today');
			todayStore.value = response.data;
			localStorage.setItem('lunchbox_today_stores', JSON.stringify(response.data));
		} catch (error: unknown) {
			if (!axios.isAxiosError(error)) {
				return;
			}
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

			switch (status) {
				case 502:
					console.log('伺服器維護中 (502)，請稍後再試');
					break;
				default:
					console.log(`系統錯誤 (${status})`);
			}
		} finally {
				isLoading.value = false;
		}
	}
	
	const goToMenu = (item: Store) => {
		if (!item.is_active) {
			alert('商店未開放')
			return;
		}
		router.push({
			path: '/menu',
			query: {
				id: item.id,
				name: item.name
			}
		});
	};

	const goToAccount = () => {
		router.push('/user');
	}

	const goToCreateStore = () => {
		router.push('/create');
	}

	onMounted(() => {
		verifyUser();
		get_today_store();
	});
	
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

.top-box {
	position: relative;
	top: 0px;
	padding: 0 30px;
	display: flex;
	justify-content: space-between;
	align-items: center;
	width: 100%;
	height: 10vh;
	z-index: 101;
}


.logo {
	color: var(--primary-orange);
	font-size: 2.6rem;
	font-weight: 900;
	margin-top: 20px;
	letter-spacing: -1px;
	text-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.main-box {
  width: 100%;
  padding: 0 15px;
  margin-top: 3cap;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 10;
}

.store-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  width: 100%;
  max-width: 400px;
	padding-bottom: 200px;
}

.card {
	background: rgba(255, 255, 255, 0.65);
	backdrop-filter: blur(15px);
	border-radius: 24px;
	padding: 20px;
	border: 1px solid rgba(255, 255, 255, 0.4);
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
	width: 100%;
	text-align: left;
	cursor: pointer;
	font-family: inherit;
	transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
	display: block;
}

.card:active {
	transform: scale(0.96);
	background: rgba(255, 255, 255, 0.8);
}


.card-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 4px;
}

.card-header h3 {
	margin: 0;
	color: #444;
	font-size: 1.5rem;
	font-weight: 700;
	letter-spacing: 1px;
}

.deadline {
	font-size: 0.9rem;
	color: #666;
	margin: 5px 0;
}

.card.inactive {
	opacity: 0.6;
	cursor: not-allowed;
	filter: grayscale(0.5);
}

.empty-state {
	text-align: center;
	padding: 40px;
	color: #888;
	background: rgba(255, 255, 255, 0.4);
	border-radius: 20px;
	font-weight: 500;
}

.card-content {
	display: flex;
	align-items: center;
	justify-content: space-between;
	width: 100%;
}

.info-section {
	flex: 1;
}

.arrow-icon {
	width: 24px;
	height: 24px;
	color: #b2bec3;
	margin-left: 15px;
	transition: all 0.3s ease;
}

.arrow-icon svg {
	width: 100%;
	height: 100%;
	display: block;
}

.user-config-tag {
  display: flex;
	align-items: center;
	margin-top: 20px;
  gap: 12px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  padding: 6px 6px 6px 16px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.user-config-tag:active {
  transform: scale(0.97);
  background: rgba(255, 255, 255, 0.8);
}

.user-meta {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.greeting {
  font-size: 9px;
  color: #999;
  letter-spacing: 0.1em;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 2px;
}

.nickname {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  line-height: 1.2;
}

.config-icon-box {
  width: 36px;
  height: 36px;
  background: #f0f0f0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}

.config-icon-box svg {
  width: 20px;
  height: 20px;
}

.fab-btn {
	position: fixed;
	bottom: 30px;
	right: 25px;
	width: 60px;
	height: 60px;
	background-color: var(--primary-orange);
	color: white;
	border-radius: 20px;
	border: none;
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	z-index: 1000;
	box-shadow: 0 10px 25px rgba(255, 138, 0, 0.4);
	transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.fab-btn:active {
	transform: scale(0.85);
	background-color: #e67e00;
	box-shadow: 0 5px 15px rgba(255, 138, 0, 0.3);
}

.fab-btn svg {
	width: 28px;
	height: 28px;
	stroke-linecap: round;
	stroke-linejoin: round;
}

.footer-info {
	position: absolute;
	font-size: 12px;
	color: #666;
	bottom: 20px;
	left: 50%;
	transform: translateX(-50%);
}

.card-header h3 {
    margin: 0;
    color: #444;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
}

.card-header h3::before {
    content: '';
    display: inline-block;
    width: 7px;
    height: 30px;
    border-radius: 5px;
    margin-right: 12px;
    transition: background-color 0.3s ease;
}

.status-open::before {
    background-color: #2ecc71;
}

.status-closed::before {
    background-color: #e74c3c;
}

</style>