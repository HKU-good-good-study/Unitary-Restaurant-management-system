<script lang="ts">
  import { onMount } from 'svelte';
  import { validation } from '$lib/tool.svelte';

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
  let tableOrders=[];
  let ordersID=[];
  let tables= [];
  let occupiedTable=[];
  $: tableOrders=tableOrders;
  
  let tableDishes = [];
  let dishes =[];
  let dish ={};
  let dishesName = [];
  
  let dish1 = new Dish('Dish 1', 5);
  let dish2 = new Dish('Dish 2', 3);
  let dish3 = new Dish('Dish 3', 7);
  
  // let unservedDishes = [
  //   { table: 'Table 1', dishes: [dish1, dish2] },
  //   { table: 'Table 2', dishes: [dish3] }
  // ];
  // console.log(unservedDishes);

  let unservedDishes=[];
  $: unservedDishes=unservedDishes;

  let menu = [
    { name: dish1.getName(), quantity: dish1.getQuantity() },
    { name: dish2.getName(), quantity: dish2.getQuantity() },
    { name: dish3.getName(), quantity: dish3.getQuantity() }
  ];

  onMount(async() => {
    // 在这里可以添加与后端的通信逻辑，从数据库或API获取真实数据
    // history.replaceState(null, 'Profile', '/profile');
    await validation();
    await getAllOrder();
    document.title = 'Kitchen Staff Page';
  });

  function toggleWorkStatus() {
    // 在这里可以添加与后端的通信逻辑，更新工作状态
  }

  function updateMenu(index, quantity) {
    // 在这里可以添加与后端的通信逻辑，更新菜单信息
    menu[index].quantity = quantity;
  }

  async function fetchTable(){
    try {
          const response = await fetch('http://localhost:8000/table/all', {
              method: 'GET',
              credentials: 'include',
          });
          if (response.ok) {
              tables = await response.json();
              for(var i in tables){
                var table=tables[i];
                // console.log(table);
                
                if(table.status=='occupied'){
                  ordersID.push(table.order[Object.keys(table.order)[Object.keys(table.order).length-1]]);
                }
                // console.log(i+':');
                // console.log(Object.keys(table.order)[Object.keys(table.order).length-1]);
                // console.log(ordersID);                
              }
          } else {
              console.error('Error fetching table:', response.status);
              tables = []; // 设置 menus 为空数组
          }
      } catch (error) {
          console.error('Error fetching table:', error);
          tables = []; // 设置 menus 为空数组
      }
  }

  async function getAllOrder() {
    await fetchTable();    
    for(var i in ordersID){    
      if(ordersID[i]){        
        await getOrder(ordersID[i][ordersID[i].length-1]);       
      }    
    }    
    getAllDishes();
    // console.log(tableOrders);
    tableOrders=tableOrders;
  }

  function getAllDishes(){
    occupiedTable=[];
    for(var i in tableOrders){
      var order=tableOrders[i];
      // console.log(order);
      tableDishes=order.dish;
      // console.log(tableDishes);
      dishesName=Object.keys(tableDishes);
      dishes=[];
      // console.log(dishesName);
      for(var j in tableDishes){
        if(!tableDishes[j].served){          
          dishes=[...dishes,{name:j,quantity:tableDishes[j].amount}];
        }
        // console.log(j+tableDishes[j].amount);        
      }      
      unservedDishes["Table "+order.table]= dishes;
    }
    unservedDishes=unservedDishes;
    // console.log(unservedDishes);
  }

  async function getOrder(orderID){
    try {
          const response = await fetch('http://localhost:8000/table/order/'+orderID, {
              method: 'GET',
              credentials: 'include',
          });
          if (response.ok) {
              tableOrders.push(await response.json()) ;
          } else {
              console.error('Error fetching table order:', response.status);
              tableOrders = []; // 设置 menus 为空数组
          }
      } catch (error) {
          console.error('Error fetching table order:', error);
          tables = []; // 设置 menus 为空数组
      }
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

<!-- <div class="scroll-container">
  <h2>Unserved Dishes</h2>
  {#each unservedDishes as table (table.table)}
    <details class="table-container">
      <summary>{table.table}</summary>
      {#each table.dishes as dish (dish.getName())}
        <p>{dish.getName()} - {dish.getQuantity()}</p>
      {/each}
    </details>
  {/each}
</div> -->

<div class="scroll-container">
  <h2>Unserved Dishes</h2>
  {#each tableOrders as table}
    <details class="table-container">
      <summary>{"Table "+table.table}</summary>
      {#each unservedDishes["Table "+table.table] as unservedDish}
        <p>{unservedDish.quantity} * {unservedDish.name}</p>
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