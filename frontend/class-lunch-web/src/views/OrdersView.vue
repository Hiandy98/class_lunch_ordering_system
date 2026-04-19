<template>
	<div class="body">
		<div class="decoration decor-1"></div>
		<div class="decoration decor-2"></div>
		<div class="header">
			<BackButton />
			<div class="logo">LunchBox</div>
		</div>
	
		<div class="content-container">
			<div class="section">
				<h2 class="title">我的訂單</h2>

				<div v-for="(order, index) in myOrders" :key="order.id" class="order-item-card">
					<div class="order-content">
						<div class="name">{{ order.name }}</div>
						<div class="price">${{ order.price }}</div>
					</div>

					<el-button
							type="danger" 
							link 
							@click="removeOrder(index)"
							:loading="isLoaaing"
					>
						<el-icon><Delete /></el-icon>
					</el-button>
				</div>
				<p v-if="myOrders.length === 0" class="no-order">No Data</p>
			</div>

			<div class="section">
				<div class="section-header">
					<h2 class="title">訂餐數據</h2>
					<div class="summary-container">
						<span class="total-amount">{{ total_price }}</span>
						<span class="currency">TWD</span>
					</div>
				</div>
	
				<div class="table-container">
					<table class="order-table">
						<thead>
							<tr>
								<th>座號</th>
								<th>餐點</th>
								<th>金額</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(order, idx) in allOrders" :key="idx">
								<td>{{ Number(order.student_id) - 140251 }}</td>
								<td>
									<div v-for="(item, i) in order.content" :key="i">
										{{ item.name }}
									</div>
								</td>
								<td>{{ order.total_price }}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</div>
		<div class="footer-info">V0.0 Beta</div>
	</div>
</template>

<script setup lang="ts">
import BackButton from '@/components/BackButton.vue'
import { useRoute } from 'vue-router';
import { ref, onMounted, computed } from 'vue'
import { Delete } from '@element-plus/icons-vue'
import axios from 'axios';

const route = useRoute();

const store_id = route.query.id;
console.log(route.query.name);
console.log(store_id);

interface OrderItem {
  name: string;
  price: number;
}

interface MyOrders {
	id: string;
	name: string;
  price: number;
}

interface UserInfo {
	user_id: string;
	display_name: string;
	role: string;
}

interface Orders {
	id: string;
  student_id: string;
  content: OrderItem[];
  total_price: number;
	is_active: boolean;
}

const userInfo = ref<UserInfo | null>(null);
const allOrders = ref<Orders[]>([]);
const myOrders = ref<MyOrders[]>([]);
const isLoaaing = ref(false);

const total_price = computed(() => {
  return allOrders.value.reduce((sum, order) => sum + order.total_price, 0);
});

const verifyUser = async () => {
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

const getAllOrder = async () => {
	try {
		const response = await axios.get(`/api/v1/store/${store_id}/orders`);
		allOrders.value = response.data.filter((order: Orders) => order.is_active === true);

		myOrders.value = allOrders.value
			.filter(order => order.student_id === userInfo.value?.user_id)
			.map(order => ({
				id: order.id,
				name: order.content.map(item => item.name).join(', '),
				price: order.total_price 
			}));

	} catch(error) {
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

const removeOrder = async (index: number) => {
	if (isLoaaing.value) return;
  isLoaaing.value = true;
	try {
		const data = myOrders.value[index];
		if (!data) return;
		const response = await axios.patch('api/v1/order/cancel', null, {
			params: {
				id: data.id
			}
		});
		if (response.status === 200) {
      console.log('訂單建立成功：', response.data);
      alert('已取消訂單！');
			await getAllOrder();
    }
		myOrders.value.splice(index, 1);
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
}

onMounted( async () => {
	await verifyUser();
	await getAllOrder();
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


.content-container {
	width: 90%;
	max-width: 500px;
	margin-top: 100px;
	padding-bottom: 80px;
	z-index: 10;
}

.section {
	background: rgba(255, 255, 255, 0.6);
	backdrop-filter: blur(10px);
	border-radius: 24px;
	padding: 20px;
	margin-bottom: 25px;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.3);
}

.title {
	font-size: 1.2rem;
	color: #333;
	margin-bottom: 15px;
	font-weight: 700;
	display: flex;
	align-items: center;
}

.title::before {
	content: '';
	width: 4px;
	height: 18px;
	background: var(--primary-orange);
	margin-right: 8px;
	border-radius: 10px;
}


.price {
	margin-left: 10px;
	color: #888;
	font-size: 0.9rem;
}

.delete-btn {
	background: #ffeded;
	color: #ff5b5b;
	border: none;
	padding: 6px 12px;
	border-radius: 8px;
	cursor: pointer;
	font-size: 0.85rem;
	transition: 0.3s;
}

.delete-btn:hover {
	background: #ff5b5b;
	color: white;
}

.table-container {
	overflow-x: auto;
}

.order-table {
	width: 100%;
	border-collapse: collapse;
	font-size: 0.9rem;
}

.order-table th {
	text-align: left;
	color: #888;
	padding-bottom: 10px;
	font-weight: 500;
}

.order-table td {
	padding: 10px 0;
	border-top: 1px solid rgba(0, 0, 0, 0.05);
	color: #555;
}

.order-item-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: white;
  border-radius: 12px;
  margin-bottom: 10px;
}

.no-order {
  font-size: 1.3em;
  color: #555;
  text-align: center;
}

.order-content {
    display: flex;
    flex-direction: column;
}

.order-item-card .name {
    font-weight: 600;
    color: #333;
    line-height: 1.4;
    word-break: break-all;
}

.order-item-card .price {
    margin-left: 0;
    margin-top: 4px;
    color: var(--secondary-blue);
    font-weight: 700;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.summary-container {
		margin-bottom: 15px;
    display: flex;
    align-items: baseline;
}

.total-amount {
    color: var(--secondary-blue);
    font-size: 1.3rem;
    margin-right: 5px;
}

.currency {
    color: #bbb;
    font-size: 10px;
    font-weight: bold;
    transform: scale(0.9);
}
</style>