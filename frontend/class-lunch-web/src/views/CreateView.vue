<template>
	<div class="body">
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>
		
		<div class="header">
			<BackButton />
			<div class="logo">LunchBox</div>
		</div>

		<div class="content-container">
			<div v-if="is_loading && stores.length === 0" class="global-loading">
				<span>載入中...</span>
			</div>

			<div v-else class="store-grid">
				<div 
					v-for="store in stores" 
					:key="store.id" 
					class="store-card"
					:class="{ 'is-active': store.is_active }"
					@click="openManageDrawer(store)"
				>
					<div class="store-info">
						<h3 class="store-name">{{ store.name }}</h3>
						<span class="status-badge">
							{{ store.is_active ? '營業中' : '休息中' }}
						</span>
					</div>
				</div>
			</div>
			
			<p v-if="stores.length === 0 && !is_loading" class="no-data">暫無餐廳資料</p>
		</div>

		<button class="fab-btn" @click="openCreateDrawer">
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
				<line x1="12" y1="5" x2="12" y2="19"></line>
				<line x1="5" y1="12" x2="19" y2="12"></line>
			</svg>
		</button>

		<el-drawer
			v-model="is_drawer_open"
			:title="drawer_mode === 'create' ? '建立新餐廳' : '管理餐廳資料'"
			direction="rtl"
			size="85%"
			class="custom-drawer"
		>

			<div v-if="drawer_mode === 'create'" class="drawer-body">
				<div class="input-section">
					<div class="input-item">
						<p class="section-label">餐廳名稱:</p>
						<el-input 
							v-model="new_store_name" 
							placeholder="請輸入新餐廳名稱" 
							class="custom-input"
							clearable 
						/>
					</div>

					<div class="input-item">
						<p class="section-label">上傳菜單圖片 (可多張):</p>
						<el-upload
							action="#"
							list-type="picture-card"
							:auto-upload="false"
							v-model:file-list="uploaded_file_list"
							:on-remove="handleRemoveUploadedFile"
							class="custom-uploader"
						>
							<el-icon><Plus /></el-icon>
						</el-upload>
					</div>

				</div>
				<el-button class="action-btn" :loading="is_loading" @click="handleCreateStore">
					確認建立餐廳
				</el-button>
			</div>

			<div v-else-if="drawer_mode === 'manage' && selected_store" class="drawer-body">
				<div class="info-section">
					<div class="input-item">
						<p class="section-label">修改餐廳名稱:</p>
						<el-input 
							v-model="edit_form.name" 
							placeholder="請輸入餐廳名稱" 
							class="custom-input"
							clearable 
						/>
					</div>

					<div class="status-switch-row">
						<span class="status-label">營業狀態：</span>
						<el-switch 
							v-model="edit_form.is_active" 
							active-text="開啟" 
							inactive-text="關閉"
							active-color="var(--primary-orange)"
						/>
					</div>

					<div class="status-switch-row">
						<span class="status-label">今日餐廳：</span>
						<el-switch 
							v-model="edit_form.is_today_store" 
							active-text="是" 
							inactive-text="否"
							active-color="var(--primary-orange)"
						/>
					</div>

					<div class="input-item">
						<p class="section-label">現有菜單圖片：</p>
						<div class="menu-images-grid">
							<div v-for="(url, idx) in edit_form.menu_urls" :key="idx" class="menu-img-wrapper">
								<img :src="url" class="menu-thumb" />
								<el-button type="danger" size="small" circle @click="removeMenuImage(idx)">X</el-button>
							</div>
						</div>
						<el-upload
							action="#"
							:auto-upload="false"
							:on-change="handleAddMenuImage"
							:show-file-list="false"
							multiple
						>
							<el-button type="primary" plain>新增圖片</el-button>
						</el-upload>
					</div>

					<div v-if="edit_form.is_today_store" class="input-item">
						<p class="section-label">點餐截止時間:</p>
						<el-time-picker
							v-model="edit_form.deadline_time"
							placeholder="選擇截止時間"
							format="HH:mm"
							value-format="HH:mm:ss"
							class="custom-time-picker"
						/>
					</div>
				</div>
				
				<el-button class="action-btn" :loading="is_loading" @click="handleUpdateStoreData">
					儲存資料變更
				</el-button>
			</div>
		</el-drawer>

		<div class="footer-info">V0.0 Beta</div>
	</div>
</template>


<script setup lang="ts">
import BackButton from '@/components/BackButton.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { UploadUserFile, UploadFile } from 'element-plus';

interface BackendStoreResponse {
	id: string;
	name: string;
	is_active?: boolean;
	deadline?: string;
	is_today_store?: boolean;
	menu_url: string[];
}

interface Store {
	id: string;
	name: string;
	is_active: boolean;
	deadline?: string;
	is_today_store?: boolean;
	menu_url: string[];
}

const cachedStores = localStorage.getItem('lunchbox_admin_stores');

const stores = ref<Store[]>(cachedStores ? JSON.parse(cachedStores) : []);
const is_loading = ref<boolean>(false);
const is_drawer_open = ref<boolean>(false);
const drawer_mode = ref<'create' | 'manage'>('create');
const new_store_name = ref<string>('');
const new_store_menu_urls = ref<string[]>(['']);
const selected_store = ref<Store | null>(null);
const uploaded_file_list = ref<UploadUserFile[]>([]);
const menu_url_strings = ref<string[]>([]);

const edit_form = ref({
	name: '',
	is_active: true,
	deadline_time: '14:35:00',
	is_today_store: true,
	menu_urls: [] as string[]
});

const handleRemoveUploadedFile = (uploadFile: UploadFile) => {
	const targetUrl = (uploadFile.response as { url?: string } | undefined)?.url;
	if (targetUrl) {
		menu_url_strings.value = menu_url_strings.value.filter(url => url !== targetUrl);
	}
};

const fetchStores = async () => {
	try {
		is_loading.value = true;
		
		const [allStoresRes, todayStoresRes] = await Promise.all([
			axios.get<BackendStoreResponse[]>('/api/v1/store/list'),
			axios.get<BackendStoreResponse[]>('/api/v1/store/list/today')
		]);

		const allStores = allStoresRes.data;
		const todayStores = todayStoresRes.data;

		const mappedStores = allStores.map((store: BackendStoreResponse) => {
			const todayMatch = todayStores.find((t: BackendStoreResponse) => t.id === store.id);
			
			return {
				id: store.id,
				name: store.name,
				is_active: todayMatch ? (todayMatch.is_active ?? false) : false,
				is_today_store: todayMatch ? (todayMatch.is_today_store ?? false) : false,
				deadline: todayMatch ? todayMatch.deadline : undefined,
				menu_url: store.menu_url || [],
			};
		});

		stores.value = mappedStores;
		localStorage.setItem('lunchbox_admin_stores', JSON.stringify(mappedStores));

	} catch (error) {
		console.error('獲取餐廳清單失敗:', error);
		ElMessage.error('無法取得餐廳列表資料');
	} finally {
		is_loading.value = false;
	}
};

const openCreateDrawer = () => {
	drawer_mode.value = 'create';
	new_store_name.value = '';
	new_store_menu_urls.value = [''];
	is_drawer_open.value = true;
}

const openManageDrawer = (store: Store) => {
	drawer_mode.value = 'manage';
	selected_store.value = store;
	
	edit_form.value.name = store.name;
	edit_form.value.is_active = store.is_active;
	edit_form.value.is_today_store = store.is_today_store ?? false;
	edit_form.value.menu_urls = store.menu_url || [];
	edit_form.value.deadline_time = '12:00:00';

	if (!store.deadline) {
		is_drawer_open.value = true;
		return;
	}

	try {
		const parts = store.deadline.split('T');
		if (parts.length <= 1 || !parts[1]) {
			is_drawer_open.value = true;
			return;
		}

		const rawTime = parts[1].substring(0, 8);
		const timeArray = rawTime.split(':');

		if (timeArray.length <= 2 || !timeArray[0] || !timeArray[1] || !timeArray[2]) {
			is_drawer_open.value = true;
			return;
		}

		const localHour = (parseInt(timeArray[0], 10) + 8) % 24;
		const formattedHour = localHour.toString().padStart(2, '0');
		
		edit_form.value.deadline_time = `${formattedHour}:${timeArray[1]}:${timeArray[2]}`;

	} catch (error) {
		console.error('解析截止時間失敗，使用預設值', error);
	}

	is_drawer_open.value = true;
}

const removeMenuImage = async (index: number) => {
  if (!selected_store.value) return;
  const newUrls = [...edit_form.value.menu_urls];
  newUrls.splice(index, 1);
  await axios.patch(`/api/v1/store/${selected_store.value.id}/update`, {
    menu_url: newUrls
  });
  edit_form.value.menu_urls = newUrls;
  ElMessage.success('已刪除圖片');
	
	updateSingleStoreCache(selected_store.value.id, { menu_url: newUrls });
};

const handleAddMenuImage = async (file: UploadFile) => {
  if (!selected_store.value) return;
	if (!file.raw) {
    ElMessage.error('檔案讀取失敗');
    return;
  }
  try {
    const formData = new FormData();
    formData.append('files', file.raw);
    
    const res = await axios.post<string[]>(
      `/api/v1/store/stores/${selected_store.value.id}/upload-menu`, 
      formData
    );
    
    edit_form.value.menu_urls = res.data;
    ElMessage.success('圖片已新增');

		updateSingleStoreCache(selected_store.value.id, { menu_url: res.data });
  } catch (error) {
    console.error('圖片上傳失敗:', error);
    ElMessage.error('圖片上傳失敗');
  }
};

const handleCreateStore = async () => {
  const name = new_store_name.value.trim();
  if (!name) {
    ElMessage.warning('請輸入餐廳名稱');
    return;
  }

  try {
    is_loading.value = true;
    
    const storeRes = await axios.post<{ id: string }>('/api/v1/store/create', { name });
    console.log('創建餐廳響應:', storeRes.data);
		const newStoreId = storeRes.data.id;
		console.log('提取的 newStoreId:', newStoreId);

    const rawFiles = uploaded_file_list.value.map(item => item.raw).filter(Boolean) as File[];
    if (rawFiles.length > 0) {
			const formData = new FormData();
			rawFiles.forEach(file => formData.append('files', file));
			
			try {
				const uploadRes = await axios.post(`/api/v1/store/stores/${newStoreId}/upload-menu`, formData);
				ElMessage.success(`已上傳 ${rawFiles.length} 張圖片`);
				console.log('上傳成功，URLs:', uploadRes.data);
			} catch (uploadError) {
				console.error('圖片上傳失敗:', uploadError);
				if (axios.isAxiosError(uploadError)) {
					console.error('狀態碼:', uploadError.response?.status);
					console.error('後端錯誤:', uploadError.response?.data);
					ElMessage.error(`圖片上傳失敗: ${uploadError.response?.data?.detail || uploadError.message}`);
				} else {
					ElMessage.error('圖片上傳失敗，請稍後重試');
				}
			}
		}

    ElMessage.success('餐廳建立完成');
    uploaded_file_list.value = [];
    is_drawer_open.value = false;
    await fetchStores(); // 5. 建立成功後，fetchStores 會自動覆寫整份最新的快取

  } catch (error) {
    console.error('建立餐廳失敗:', error);
    ElMessage.error('建立餐廳失敗，請檢查網路或後端服務');
  } finally {
    is_loading.value = false;
  }
};

const handleUpdateStoreData = async () => {
	if (!selected_store.value) return;
	
	const targetName = edit_form.value.name.trim();
	if (!targetName) {
		ElMessage.warning('餐廳名稱不能為空');
		return;
	}

	try {
		is_loading.value = true;
		
		const todayStr = new Date().toLocaleDateString('zh-TW', {
			year: 'numeric', month: '2-digit', day: '2-digit'
		}).replace(/\//g, '-');
		
		const timeArray = edit_form.value.deadline_time.split(':');
		
		if (timeArray.length > 2 && timeArray[0] && timeArray[1] && timeArray[2]) {
			let utcHour = parseInt(timeArray[0], 10) - 8;
			if (utcHour < 0) {
				utcHour = 24 + utcHour;
			}
			const formattedUtcHour = utcHour.toString().padStart(2, '0');
			const utcTimeStr = `${formattedUtcHour}:${timeArray[1]}:${timeArray[2]}`;
			
			const fullIsoDeadline = `${todayStr}T${utcTimeStr}.000Z`;

			const updatePayload = {
				is_active: edit_form.value.is_active,
				name: targetName,
				deadline: fullIsoDeadline,
				is_today_store: edit_form.value.is_today_store
			};

			await axios.patch(`/api/v1/store/${selected_store.value.id}/update`, updatePayload);
			ElMessage.success('餐廳資料更新成功');
			is_drawer_open.value = false;
			await fetchStores();
		} else {
			ElMessage.error('時間格式不正確，儲存失敗');
		}
	} catch (error) {
		console.error('更新餐廳資料失敗:', error);
		ElMessage.error('更新失敗，請檢查內容格式');
	} finally {
		is_loading.value = false;
	}
};


const updateSingleStoreCache = (storeId: string, updatedFields: Partial<Store>) => {
	const currentCache = localStorage.getItem('lunchbox_admin_stores');
	if (!currentCache) return;
	try {
		const parsedStores = JSON.parse(currentCache) as Store[];
		const index = parsedStores.findIndex(s => s.id === storeId);
		if (index !== -1) {
			parsedStores[index] = { ...parsedStores[index], ...updatedFields } as Store;
			localStorage.setItem('lunchbox_admin_stores', JSON.stringify(parsedStores));
		}
	} catch (e) {
		console.error('更新單一餐廳快取失敗', e);
	}
};

onMounted(() => {
	fetchStores();
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

.decor-1 { width: 350px; height: 350px; background: var(--secondary-blue); top: -100px; left: -50px; }
.decor-2 { width: 300px; height: 300px; background: var(--primary-orange); bottom: -50px; right: -50px; animation-delay: -2s; }

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

.content-container {
	width: 90%;
	max-width: 400px;
	margin-top: 15vh;
	margin-bottom: 100px;
	z-index: 2;
}

.store-grid {
	display: grid;
	grid-template-columns: repeat(2, 1fr); 
	gap: 20px;
	width: 100%;
}

.store-card {
	background: rgba(255, 255, 255, 0.65);
	backdrop-filter: blur(10px);
	-webkit-backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.8);
	border-radius: 30px; 
	padding: 30px 15px;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
	transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.store-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
	background: rgba(255, 255, 255, 0.85);
}

.store-name {
	margin: 0 0 12px 0;
	font-size: 16px;
	color: #333;
	font-weight: 600;
}

.status-badge {
	font-size: 12px;
	padding: 4px 14px;
	border-radius: 15px;
	background: #909399;
	color: white;
	font-weight: 500;
}

.store-card.is-active {
	border: 1px solid rgba(255, 136, 0, 0.3);
}

.store-card.is-active .status-badge {
	background: var(--primary-orange);
	box-shadow: 0 2px 8px rgba(255, 136, 0, 0.2);
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

.fab-btn svg { width: 28px; height: 28px; stroke-linecap: round; stroke-linejoin: round; }

:deep(.custom-drawer) {
	background: rgba(255, 255, 255, 0.65) !important; 
	backdrop-filter: blur(15px) !important; 
	-webkit-backdrop-filter: blur(15px) !important;
	border-left: 1px solid rgba(255, 255, 255, 0.7) !important;
	border-radius: 40px 0 0 40px !important; 
	max-width: 360px;
}

:deep(.custom-drawer .el-drawer__header) { margin-bottom: 20px; padding: 30px 24px 0 24px; }
:deep(.custom-drawer .el-drawer__title) { font-weight: 700; color: #333; font-size: 18px; }
:deep(.custom-drawer .el-drawer__body) { padding: 10px 24px 30px 24px; }

.drawer-body {
	height: 100%;
	display: flex;
	flex-direction: column;
	justify-content: space-between; 
}

.input-section, .info-section { display: flex; flex-direction: column; gap: 20px; }
.input-item { display: flex; flex-direction: column; gap: 8px; width: 100%; }
.section-label, .status-label { margin: 0; font-size: 15px; color: #555; font-weight: 500; }

.status-switch-row {
	display: flex;
	align-items: center;
	justify-content: space-between;
	background: rgba(255, 255, 255, 0.5);
	padding: 15px 20px;
	border-radius: 20px;
	border: 1px solid rgba(255, 255, 255, 0.5);
}

:deep(.custom-time-picker.el-input) {
	width: 100% !important;
}
:deep(.custom-time-picker .el-input__wrapper) {
	background-color: white !important;
	border-radius: 20px !important;
	box-shadow: none !important;
	border: 1px solid #eee;
	height: 45px;
}

:deep(.custom-input .el-input__wrapper) {
	background-color: white !important;
	border-radius: 20px !important;
	box-shadow: none !important;
	border: 1px solid #eee;
}
:deep(.custom-input .el-input__inner) { height: 45px; text-align: center; }

.action-btn {
	width: 100%;
	height: 50px;
	border-radius: 25px;
	background-color: var(--primary-orange) !important;
	border: none !important;
	color: white !important;
	font-size: 16px;
	font-weight: bold;
	margin-top: auto; 
	box-shadow: 0 6px 15px rgba(255, 138, 0, 0.2);
}
.action-btn:hover { background-color: #e67e00 !important; transform: translateY(-1px); }

.no-data {
	text-align: center;
	color: #888;
	margin-top: 40px;
	font-size: 14px;
}

.footer-info {
	position: absolute;
	font-size: 12px;
	color: #666;
	bottom: 20px;
	left: 50%;
	transform: translateX(-50%);
}

.dynamic-url-row {
	display: flex;
	align-items: center;
	gap: 10px;
	width: 100%;
	margin-bottom: 8px;
}

.field-flex {
	flex: 1;
}

.remove-url-btn {
	flex-shrink: 0;
	border: 1px solid #ffcbcb !important;
	background-color: #fff5f5 !important;
	color: #f56c6c !important;
}
.remove-url-btn:hover {
	background-color: #f56c6c !important;
	color: white !important;
}

.add-url-btn {
	margin-top: 5px;
	border-radius: 15px !important;
	border: 1px dashed var(--secondary-blue) !important;
	color: var(--secondary-blue) !important;
	background: transparent !important;
	width: 100%;
	height: 35px;
	font-weight: 500;
}
.add-url-btn:hover {
	background: rgba(0, 132, 255, 0.05) !important;
}

.menu-images-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}
.menu-img-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
}
.menu-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #ddd;
}
.menu-img-wrapper .el-button {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 20px;
  height: 20px;
  padding: 0;
}
</style>
