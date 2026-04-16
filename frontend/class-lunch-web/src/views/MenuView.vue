<template>
	<div class="body">
		<div class="header">
			<BackButton />
			<div class="logo">LunchBox</div>
			<button class="order-btn" @click="handleGoTo" type="button">
				<span class="goto-text">訂單</span>
				<svg class="goto-icon" viewBox="0 0 24 24" fill="none" 
					stroke="currentColor" 
					stroke-width="3" 
					stroke-linecap="round" 
					stroke-linejoin="round"
				>
					<path d="M9 18l6-6-6-6" />
				</svg>
  		</button>
		</div>
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>

		<div class="store-name">{{ store_name }}</div>

		<div class="carousel-wrapper">
      <el-carousel
        height="40vh"
        :autoplay="false"
        arrow="always"
        indicator-position="outside"
      >
        <el-carousel-item v-for="(url, index) in menuImages" :key="index">
          <div class="img-box">
            <el-image
              class="main-img"
              :src="url"
              :preview-src-list="menuImages"
              :initial-index="index"
              fit="contain"
              preview-teleported
							:z-index="3000"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><icon-picture /></el-icon>
									<h1>404 Not Found</h1>
                </div>
              </template>
            </el-image>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

		<div class="input-section">
			<el-card class="input-card">
				<template #header>
					<div class="card-header">
						<span>餐點清單，總計 {{ total_price }} 元</span>
						<el-button type="primary" size="small" circle @click="addRow" :loading="isLoaaing" >
							<el-icon><Plus /></el-icon>
						</el-button>
					</div>
				</template>

				<div v-for="(item, index) in foodList" :key="index" class="food-row">
					<el-input v-model="item.name" placeholder="品名" class="name-input" />
					
					<el-input-number 
						v-model="item.price" 
						:min="0" 
						controls-position="right" 
						class="price-input" 
						placeholder="價格"
						@change="priceChange"
					/>

					<el-button
						v-if="foodList.length > 1" 
						type="danger" 
						link 
						@click="removeRow(index)"
					>
						<el-icon><Delete /></el-icon>
					</el-button>
				</div>

				<div class="action-bar">
					<el-button type="primary" class="submit-btn" @click="submitAll">
						送出 {{ foodList.length }} 個項目
					</el-button>
				</div>
			</el-card>
		</div>
	
		<div class="footer-info">V0.0 Beta</div>
	</div>
</template>

<script setup lang="ts">
import BackButton from '@/components/BackButton.vue'
import { useRoute } from 'vue-router';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import router from '@/router';
import { Plus, Delete } from '@element-plus/icons-vue';


const route = useRoute();

const store_id = route.query.id;
console.log();
console.log(store_id);

interface UserInfo {
	user_id: string;
	display_name: string;
	role: string;
}

interface FoodItem {
  name: string;
  price: number;
}

const total_price = ref<number>(0);
const isLoaaing = ref(false);

const foodList = ref<FoodItem[]>([
  { name: '', price: 0 }
]);

const addRow = () => {
  foodList.value.push({ name: '', price: 0 });
};

const removeRow = (index: number) => {
  foodList.value.splice(index, 1);
};

const submitAll = async () => {
	if (isLoaaing.value) return;
  isLoaaing.value = true;
  
	const validData = foodList.value.filter(item => item.name.trim() !== '');
  
  if (validData.length === 0) {
    console.log("至少填寫一個項目");
		alert("至少填寫一個項目")
    return;
  }
  console.log('準備送出的資料：', validData);
	const payload = {
			store_id: store_id,            // 從 route.query 取得的 ID
			total_price: total_price.value,
			is_active: true,
			content: validData.map(item => ({
				name: item.name,
				price: item.price
			}))
		};

	try{
		const response = await axios.post('/api/v1/order/create', payload);
		if (response.status === 201) {
      console.log('訂單建立成功：', response.data);
      alert('訂單已送出！');
    }
	} catch(error) {
		if (!axios.isAxiosError(error)) {
				return
			}
			if (!error.response) {
				if (error.request) {
					alert('無法連線至伺服器');
				} else {
					console.error('請求設定錯誤', error.message);
				}
				
				return;
			}

			const status = error.response.status;
			const detail = error.response.data?.detail;

			switch (status) {
				case 401:
					alert(detail || '帳號或密碼錯誤');
					break;
				case 502:
					alert('伺服器維護中 (502)，請稍後再試');
					break;
				default:
					alert(`系統錯誤 (${status})`);
			}
	} finally {
		isLoaaing.value = false
	}
};


const userInfo = ref<UserInfo | null>(null);
const store_name = ref<string>(route.query.name as string);

function handleGoTo() {
	router.push({
			path: '/order',
			query: {
				id: store_id,
			}
		});
}

function priceChange() {
	total_price.value = 0;
	foodList.value.forEach((item) => {
		total_price.value += item.price;
	})
}

async function verifyUser() {
	try {
		const response = await axios.get('/api/v1/auth/verify');
		userInfo.value = response.data;
	} catch (error) {
		if (!axios.isAxiosError(error)) {
			return;
		}
		console.error('驗證失敗或 Token 已過期');
	}
}

// const url = "https://p3-pc-sign.douyinpic.com/tos-cn-i-0813/765613b6cc3545bd812f3f117bcb285a~noop.jpeg?biz_tag=pcweb_cover&card_type=303&column_n=0&from=327834062&lk3s=138a59ce&s=PackSourceEnum_SEARCH&se=false&x-expires=1776330000&x-signature=nFHgKHtnkrNb%2FvHvWpZ%2Fh4pOPB0%3D"
const menuImages = ref<string[]>([]);

async function fetchMenu() {
	try {
		const response = await axios.get(`/api/v1/store/${store_id}/menu`);
		menuImages.value = response.data.menu_url;
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
	}
}

onMounted(() => {
	verifyUser();
	fetchMenu();
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

.carousel-wrapper {
  width: 70%;
  margin-top: 20px;
  z-index: 2;
}

.img-box {
  width: 100%;
  height: 100%;
}

.main-img {
  width: 100%;
  height: 100%;
  border-radius: 10%;
  background: rgba(64, 64, 64, 0.12);
  cursor: zoom-in;
}

:deep(.el-carousel__indicator--horizontal .el-carousel__button) {
  background-color: var(--secondary-blue);
  opacity: 1;
}

.store-name {
  margin-top: 11vh;
  margin-bottom: 10px;
  font-size: 30px;
  font-weight: 700;
  color: #333;
  z-index: 2;
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

.input-section {
  width: 80%;
  max-width: 600px;
  margin: 20px 0 50px 0;
  z-index: 101;
}

.input-card {
	background: rgba(255, 255, 255, 0.65);
	backdrop-filter: blur(10px);
	-webkit-backdrop-filter: blur(10px);
	border: 1px solid rgba(255, 255, 255, 0.8);
	box-shadow: 
		0 4px 15px rgba(0, 0, 0, 0.05),
		inset 0 0 2px rgba(255, 255, 255, 0.5);
	border-radius: 10%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.food-row {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  align-items: center;
}

.name-input {
  flex: 2;
}

.price-input {
  flex: 1;
}

.action-bar {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.submit-btn {
  width: 100%;
  height: 40px;
  border-radius: 20px;
	background: linear-gradient(135deg, #ff9d2f, #ff6b00);
	box-shadow: 0 8px 20px rgba(255, 107, 0, 0.3);
	border: none;
}

:deep(.el-input-number) {
	width: 100px !important;
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

.order-btn {
	position: fixed;
	top: 40px;
	right: 30px;
	z-index: 1000;
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

.goto-icon {
	width: 20px;
	height: 20px;
}

.goto-text {
	font-size: 14px;
	font-weight: 600;
	margin-left: 2px;
}

.order-btn:active {
	transform: scale(0.9);
	background: rgba(255, 255, 255, 0.4);
}

.order-btn:hover {
	color: #1f2937;
}

.image-slot {
	display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #a8abb2;
  font-size: 30px;
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