<script>
  import { onMount } from 'svelte';

  // 存储员工数据
  let employees = [
    { id: 1, name: 'John Doe', department: 'diningRoom' },
    { id: 2, name: 'Jane Smith', department: 'kitchen' },
    { id: 3, name: 'Bob Johnson', department: 'diningRoom' },
    { id: 4, name: 'Alice Williams', department: 'kitchen' }
  ];
  let dishes = [
    { name: 'Burger', popularity: 8.5 },
    { name: 'Pizza', popularity: 9.0 },
    { name: 'Salad', popularity: 7.2 },
    { name: 'Pasta', popularity: 8.7 }
  ];
  let complaints = [
    { dish: 'Burger', details: 'Overcooked' },
    { dish: 'Pizza', details: 'Delivery late' },
    { dish: 'Salad', details: 'Wrong dressing' }
  ];
  let cashFlow = {
    daily: 1500,
    monthly: 45000,
    yearly: 540000,
    perDish: {
      Burger: 800,
      Pizza: 1200,
      Salad: 500,
      Pasta: 900
    }
  };
  let storage = {
    diningRoom: {
      chairs: 50,
      tables: 20,
      silverware: 100,
      napkins: 500
    },
    kitchen: {
      stoves: 4,
      ovens: 2,
      fridges: 3,
      cookingUtensils: 50
    }
  };
  let menu = [
    { name: 'Burger', price: 12.99 },
    { name: 'Pizza', price: 15.99 },
    { name: 'Salad', price: 9.99 },
    { name: 'Pasta', price: 13.99 }
  ];

  // 从后端获取数据的接口
  async function fetchEmployees() {
    return employees;
  }

  async function fetchDishes() {
    return dishes;
  }

  async function fetchComplaints() {
    return complaints;
  }

  async function fetchCashFlow() {
    return cashFlow;
  }

  async function fetchStorage() {
    return storage;
  }

  async function fetchMenu() {
    return menu;
  }

  // 处理各种操作的函数
  function hireEmployee(department) {
    // 添加新员工
  }

  function checkSchedule() {
    // 查看员工排班
  }

  function updatePrice(dish, newPrice) {
    // 更新菜品价格
  }

  function actAsDiningRoomStaff() {
    // 模拟dining room staff的操作
  }

  function fireEmployee(employeeId) {
    // 解雇员工
  }
</script>

<main class="flex justify-center items-center h-screen">
  <div class="container bg-gray-900 rounded-2xl px-8 py-12 w-full max-w-md text-center">
    <h1 class="text-4xl font-bold text-white mb-8">Restaurant Manager</h1>

    <div class="mb-8">
      <h2 class="text-2xl font-bold text-white mb-4">Employee Management</h2>
      <button class="bg-gray-800 text-white px-8 py-4 rounded-xl mb-2 hover:bg-gray-700 transition-colors duration-300" on:click={hireEmployee}>
        Hire Employee
      </button>
      <button class="bg-gray-800 text-white px-8 py-4 rounded-xl mb-4 hover:bg-gray-700 transition-colors duration-300" on:click={checkSchedule}>
        Check Schedule
      </button>
      <button class="bg-gray-800 text-white px-8 py-4 rounded-xl mb-8 hover:bg-gray-700 transition-colors duration-300" on:click={fireEmployee}>
        Fire Employee
      </button>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-bold text-white mb-4">Menu Management</h2>
      <div class="flex justify-center items-center mb-2">
        <input type="text" class="bg-gray-800 text-white px-4 py-3 rounded-xl mr-2 text-lg mb-2" placeholder="Dish Name" />
        <input type="number" class="bg-gray-800 text-white px-4 py-3 rounded-xl text-lg mb-2" placeholder="New Price" />
      </div>
      <button class="bg-gray-800 text-white px-8 py-4 rounded-xl mb-2 hover:bg-gray-700 transition-colors duration-300" on:click={() => updatePrice('Burger', 14.99)}>
        Update Burger Price
      </button>
      <button class="bg-gray-800 text-white px-8 py-4 rounded-xl mb-2 hover:bg-gray-700 transition-colors duration-300" on:click={() => updatePrice('Pizza', 17.99)}>
        Update Pizza Price
      </button>
      <button class="bg-gray-800 text-white px-8 py-4 rounded-xl mb-8 hover:bg-gray-700 transition-colors duration-300" on:click={actAsDiningRoomStaff}>
        Act as Dining Room Staff
      </button>
    </div>
  </div>
</main>

<style>
  body {
      font-family: Arial, sans-serif;
      background-color: #f2f2f2;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
  }

  .container {
      max-width: 800px;
      background-color: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      margin: 0 auto;
      width: fit-content;
  }

  h2 {
      text-align: center;
      color: #333;
      margin-bottom: 30px;
  }

  .row {
      display: flex;
      align-items: center;
      margin-bottom: 20px;
      justify-content: space-between;
  }

  .row > * {
      margin-right: 15px;
  }

  input {
      padding: 10px 15px;
      border: 1px solid #ccc;
      border-radius: 5px;
      flex-grow: 1;
      font-size: 16px;
      margin-bottom: 15px; /* Added margin-bottom for spacing */
  }

  button {
      background-color: #333;
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      font-size: 16px;
      font-weight: bold;
      transition: background-color 0.3s ease;
  }

  button:hover {
      background-color: #555;
  }

  .complaint-dialog {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background-color: white;
      padding: 20px;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      z-index: 1;
  }

  .complaint-dialog textarea {
      width: 100%;
      height: 100px;
      margin-bottom: 10px;
  }
</style>