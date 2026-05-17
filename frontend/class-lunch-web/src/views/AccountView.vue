<template>
	<div class="body">
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>
		<div class="header">
			<BackButton />
			<div class="logo">LunchBox</div>
		</div>

		<div class="user-card">
			<div class="input-section">
				<p class="section-label">使用者名稱或ID:</p>
				<el-input
					v-model="user_name"
					:placeholder="now_user_name || '請輸入新名稱'"
					class="custom-input"
					clearable
				/>
			</div>

			<div class="input-section">
				<p class="section-label">變更密碼:</p>
				<div class="password-group">
					<el-input
						v-model="passwords.old"
						type="password"
						placeholder="目前密碼"
						show-password
						class="custom-input"
					/>
					<el-input
						v-model="passwords.new"
						type="password"
						placeholder="新密碼"
						show-password
						class="custom-input"
					/>
				</div>
			</div>

			<el-button class="save-btn" @click="handleUpdate" :loading="loading">
				儲存變更
			</el-button>
			<el-button
				type="danger"
				link
				class="logout-link"
				:disabled="loading"
				@click="handleLogout"
			>
				登出目前帳號
			</el-button>
		</div>

		<div class="footer-info">V0.0 Beta</div>
	</div>
</template>


<script setup lang="ts">
import BackButton from '@/components/BackButton.vue'
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const router = useRouter();

interface UserInfo {
	user_id: string;
	display_name: string;
	role: string;
}

interface UpdataPassword {
	old: string;
	new: string;
}

const user_info = ref<UserInfo | null>(null);
const user_name = ref<string>('');
const now_user_name = ref<string>('載入中...');
const loading = ref(false);

const passwords = reactive<UpdataPassword>({
	old: '',
	new: ''
});

async function verifyUser() {
	try {
		const response = await axios.get('/api/v1/auth/verify');
		user_info.value = response.data;
		now_user_name.value = user_info.value?.display_name || user_info.value?.user_id || '';
	} catch (error) {
		console.error('驗證失敗:', error);
		now_user_name.value = '讀取失敗';
		ElMessage.error('無法取得用戶資訊，請重新登入');
	}
}


const handleUpdate = async () => {
	const hasNameChange = user_name.value.trim() !== '';
	const hasPasswordChange = passwords.old.trim() !== '' || passwords.new.trim() !== '';

	if (!hasNameChange && !hasPasswordChange) {
		ElMessage.warning('請輸入要變更的使用者名稱或密碼');
		return;
	}

	if (hasPasswordChange) {
		if (!passwords.old || !passwords.new) {
			ElMessage.error('欲變更密碼，目前密碼與新密碼皆必須填寫');
			return;
		}
		if (passwords.old === passwords.new) {
			ElMessage.error('新密碼不能與目前密碼相同');
			return;
		}
	}

	const err_msg = (msg: string) => ElMessage.error(msg);

	try {
		loading.value = true;

		if (hasNameChange) {
			const namePayload = { display_name: user_name.value.trim() };
			await axios.patch('/api/v1/auth/rename', namePayload);
			user_name.value = '';
		}

		if (hasPasswordChange) {
			const pwdPayload = { old_pwd: passwords.old, new_pwd: passwords.new };
			await axios.patch('/api/v1/auth/repwd', pwdPayload);
			passwords.old = '';
			passwords.new = '';
		}

		ElMessage.success('儲存變更成功');

		
		setTimeout(async () => {
			await verifyUser();
		}, 100);

	} catch (error) {
		if (!axios.isAxiosError(error)) {
			console.error('非 Axios 錯誤:', error);
			return;
		}

		if (!error.response) {
			if (error.request) {
				err_msg('無法連線至伺服器');
			} else {
				console.error('請求設定錯誤:', error.message);
			}
			return;
		}

		const status = error.response.status;
		const detail = error.response.data?.detail;

		switch (status) {
			case 401:
				err_msg(detail || '密碼錯誤或驗證失效');
				break;
			case 404:
				err_msg(detail || '找不到該使用者帳號');
				break;
			case 422:
				err_msg(detail || '輸入的名稱或密碼格式不正確');
				break;
			case 500:
				err_msg(detail || '伺服器內部錯誤，更新失敗');
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

const handleLogout = async () => {
	try {
		loading.value = true;
		
		const response = await axios.post('/api/v1/auth/logout');
		
		if (response.data?.state === 'success') {
			user_info.value = null;
			now_user_name.value = '';
			
			ElMessage.success('已成功登出');
			
			router.push('/');
		} else {
			ElMessage.error('登出異常，請稍後再試');
		}
	} catch (error) {
		console.error('登出失敗:', error);
		ElMessage.error('無法連線至伺服器，登出失敗');
	} finally {
		loading.value = false;
	}
}



onMounted(() => {
	verifyUser();
})

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

.user-card {
	background: rgba(255, 255, 255, 0.65);
	backdrop-filter: blur(10px);
	-webkit-backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.8);
	box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
	
	border-radius: 40px;
	z-index: 2;
	width: 85%;
	max-width: 400px;
	display: flex;
	flex-direction: column;
	gap: 35px;
	margin-top: 15vh;
	padding: 60px 30px;
}

.input-section {
	width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 12px;
}

.section-label {
	margin: 0;
	font-size: 15px;
	color: #555;
	font-weight: 500;
}

.password-group {
	width: 100%;
	display: flex;
	flex-direction: column;
	gap: 10px;
}

:deep(.custom-input .el-input__wrapper) {
	background-color: white !important;
	border-radius: 20px !important;
	box-shadow: none !important;
	border: 1px solid #eee;
}

:deep(.custom-input .el-input__inner) {
	text-align: center;
	height: 45px;
}

.save-btn {
	width: 100%;
	height: 50px;
	border-radius: 25px;
	background-color: var(--primary-orange);
	border: none;
	color: white;
	font-size: 16px;
	font-weight: bold;
	margin-top: 20px;
	transition: all 0.3s ease;
}

.save-btn:hover {
	background-color: #e67e00;
	transform: translateY(-2px);
}

.logout-link {
	margin-top: -10px;
	font-size: 14px;
	color: #f56c6c;
	align-self: center;
	cursor: pointer;
	transition: opacity 0.2s;
}

.logout-link:hover {
	opacity: 0.8;
	text-shadow: 0 1px 2px rgba(245, 108, 108, 0.1);
}


</style>