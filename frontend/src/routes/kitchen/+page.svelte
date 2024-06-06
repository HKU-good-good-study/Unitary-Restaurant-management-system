<!-- <script lang="ts">
  import { onMount } from 'svelte';

  // 定义菜单和菜品的类型
  class Dish {
    constructor(name, quantity) {
      this.name = name;
      this.quantity = quantity;
    }
    getName () {
      return this.name;
    }
    getQuantity () {
      return this.quantity;
    }
  }
  
  let dish1 = new Dish('Dish 1', 5);
  let dish2 = new Dish('Dish 2', 3);
  let dish3 = new Dish('Dish 3', 7);
  
  let unservedDishes = 0;
  let menu = [
    { name: dish1.getName(), quantity: dish1.getQuantity() },
    { name: dish2.getName(), quantity: dish2.getQuantity() },
    { name: dish3.getName(), quantity: dish3.getQuantity() }
  ];

  onMount(() => {
    // 在这里可以添加与后端的通信逻辑，从数据库或API获取真实数据
  });

  function toggleWorkStatus() {
    // 在这里可以添加与后端的通信逻辑，更新工作状态
  }

  function updateMenu(index, quantity) {
    // 在这里可以添加与后端的通信逻辑，更新菜单信息
    menu[index].quantity = quantity;
  }
</script>

<style>
  body {
    background-color: #f4f4f4;
    font-family: 'Arial', sans-serif;
  }

  h1 {
    color: #333;
    text-align: center;
    padding: 20px 0;
  }

  h2 {
    color: #777;
    margin-bottom: 10px;
  }

  div {
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin: 20px auto;
    padding: 20px;
    width: 80%;
  }

  button {
    background-color: #333;
    border: none;
    border-radius: 5px;
    color: #fff;
    cursor: pointer;
    padding: 10px 20px;
  }

  button:hover {
    background-color: #444;
  }

  input[type="number"] {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 5px;
    width: 50px;
  }
</style>

<h1>Kitchen Staff</h1>

<div>
  <h2>Work Status</h2>
  <button on:click={toggleWorkStatus}>Toggle Work</button>
</div>

<div>
  <h2>Unserved Dishes</h2>
  <p>{unservedDishes}</p>
</div>

<div>
  <h2>Menu</h2>
  {#each menu as dish, index (dish.name)}
    <div>
      <p>{dish.name}</p>
      <input type="number" min="0" bind:value={dish.quantity} on:change={() => updateMenu(index, dish.quantity)} />
    </div>
  {/each}
</div> -->
<script lang="ts">
  import { onMount } from 'svelte';

  class Dish {
    constructor(name, quantity) {
      this.name = name;
      this.quantity = quantity;
    }
    getName () {
      return this.name;
    }
    getQuantity () {
      return this.quantity;
    }
  }
  
  let dish1 = new Dish('Dish 1', 5);
  let dish2 = new Dish('Dish 2', 3);
  let dish3 = new Dish('Dish 3', 7);
  
  let unservedDishes = [
    { table: 'Table 1', dishes: [dish1, dish2] },
    { table: 'Table 2', dishes: [dish3] }
  ];
  let menu = [
    { name: dish1.getName(), quantity: dish1.getQuantity() },
    { name: dish2.getName(), quantity: dish2.getQuantity() },
    { name: dish3.getName(), quantity: dish3.getQuantity() }
  ];

  onMount(() => {
    // 在这里可以添加与后端的通信逻辑，从数据库或API获取真实数据
    history.replaceState(null, '', '/profile');
  });

  function toggleWorkStatus() {
    // 在这里可以添加与后端的通信逻辑，更新工作状态
  }

  function updateMenu(index, quantity) {
    // 在这里可以添加与后端的通信逻辑，更新菜单信息
    menu[index].quantity = quantity;
  }
</script>

<style>
  /* 添加了滚动容器的样式 */
  .scroll-container {
    height: 200px;
    overflow-y: auto;
  }

  .table-container {
    border: 1px solid #ddd;
    border-radius: 5px;
    margin: 10px 0;
    padding: 10px;
  }

  body {
    background-color: #f4f4f4;
    font-family: 'Arial', sans-serif;
  }

  h1 {
    color: #333;
    text-align: center;
    padding: 20px 0;
  }

  h2 {
    color: #777;
    margin-bottom: 10px;
  }

  div {
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin: 20px auto;
    padding: 20px;
    width: 80%;
  }

  button {
    background-color: #333;
    border: none;
    border-radius: 5px;
    color: #fff;
    cursor: pointer;
    padding: 10px 20px;
  }

  button:hover {
    background-color: #444;
  }

  input[type="number"] {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 5px;
    width: 50px;
  }
</style>

<h1>Kitchen Staff</h1>

<div>
  <h2>Work Status</h2>
  <button on:click={toggleWorkStatus}>Toggle Work</button>
</div>

<div class="scroll-container">
  <h2>Unserved Dishes</h2>
  {#each unservedDishes as table (table.table)}
    <details class="table-container">
      <summary>{table.table}</summary>
      {#each table.dishes as dish (dish.getName())}
        <p>{dish.getName()} - {dish.getQuantity()}</p>
      {/each}
    </details>
  {/each}
</div>

<div>
  <h2>Menu</h2>
  {#each menu as dish, index (dish.name)}
    <div>
      <p>{dish.name}</p>
      <input type="number" min="0" bind:value={dish.quantity} on:change={() => updateMenu(index, dish.quantity)} />
    </div>
  {/each}
</div>