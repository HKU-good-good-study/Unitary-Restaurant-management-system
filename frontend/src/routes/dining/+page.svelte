<script>
  import Table from './Tables.svelte';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { validation } from '$lib/tool.svelte';
  import { menuTable } from '../../stores';
  import { user } from '../../stores';
  import { getNowTime } from '$lib/tool.svelte';

  // let tables=[{id: "A1",order: {},status: "idle",time: new Date(),seats: 2},
  // {id: "A2",order: {},status: "occupied",time: new Date(),seats: 2},
  // {id: "A3",order: {},status: "idle",time: new Date(),seats: 2},
  // {id: "A4",order: {},status: "reserved",time: new Date(),seats: 2},
  // {id: "A5",order: {},status: "idle",time: new Date(),seats: 2},
  // {id: "B1",order: {},status: "reserved",time: new Date(),seats: 4},
  // {id: "B2",order: {},status: "idle",time: new Date(),seats: 4},
  // {id: "B3",order: {},status: "occupied",time: new Date(),seats: 4},
  // {id: "B4",order: {},status: "reserved",time: new Date(),seats: 4},
  // {id: "C1",order: {},status: "idle",time: new Date(),seats: 8},
  // {id: "C2",order: {},status: "idle",time: new Date(),seats: 8},
  // {id: "C3",order: {},status: "occupied",time: new Date(),seats: 8},
  // {id: "C4",order: {},status: "idle",time: new Date(),seats: 8},
  // {id: "D1",order: {},status: "reserved",time: new Date(),seats: 10},
  // {id: "D2",order: {},status: "idle",time: new Date(),seats: 10},
  // ];

  // @ts-ignore
  let tables= [];

  let role = user.role;
  // $: console.log(role);

  let selectedTable = '';

  let tableOrders=[];
  let tableOrder='';

  let dishes = [];
  let dish ={};
  let dishesName = [];

  let closedTableNumber = '';
  let sum = '';
  let note = '';
  
  let showModal = false;
  let showAddTable = false;
  let showUpdateModal = false;   
  let showDeleteModal = false;
  let showCrossOutModal = false;

  let addTableSeats=0;
  let addTableNumber ='';
  let newTable={
    id: "",
    order: {},
    status: "idle",
    time: "",
    seats: 0
  }

  let updateTableID ='';
  let updatetableSeats = '';
  let tableID = '';
  let updateTable={
    id: "",
    order: {},
    status: "idle",
    time: "",
    seats: 0
  }


  async function handleTableClick(tableNumber) {
    selectedTable = tableNumber;
    updateTableID = tables[selectedTable].id;
    tableID = updateTableID;
    updatetableSeats = tables[selectedTable].seats;
    await getOrder();
    showModal = true;
    showUpdateModal = true;
  }

  function goToMenu(selectedTable) {  
    menuTable.set(selectedTable);
    goto('./menu');
  }

  function addTableButton(){
    addTableNumber = '';
    addTableSeats = 0;
    showAddTable=true;
  }

  async function addTable(){
    if(addTableNumber=='')alert('new table numbaer cannot be empty!');
    if(addTableSeats<1)alert('table seats cannot < 1');
    else {
      newTable.id = addTableNumber;
      newTable.status='idle';      
      // const now = new Date().toTimeString();
      const now = getNowTime();
      newTable.time=now;      
      newTable.seats = addTableSeats;      
      console.log(newTable);     
      const response = await fetch('http://localhost:8000/table/'+addTableNumber,{
          method: 'post',
          headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // This is important for cookies to be sent
            body: JSON.stringify(newTable)
      });
      if (response.ok) {
        await fetchTable();
        console.log(newTable);        
      } 
      else {
          console.error('Error fetching addTable:', response.status);
      }    
      showAddTable=false;
    }
  }

  async function submitUpdate(){
    const response = await fetch('http://localhost:8000/table/'+tableID,{
          method: 'put',
          headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // This is important for cookies to be sent
            body: JSON.stringify(updateTable)
      });
      if (response.ok) {
        await fetchTable();    
      } 
      else {
          console.error('Error fetching updateTable:', response.status);
      }
  }

  async function updateTableStatus(tableNumber, newStatus) {
    tableID = tables[tableNumber].id;
    tables[tableNumber].status = newStatus;
    tables[tableNumber].time = new Date().toUTCString();
    updateTable=tables[tableNumber];
    await submitUpdate();
  }

  async function updatetable(){
    tables[selectedTable].time = new Date().toUTCString();
    tables[selectedTable].id = updateTableID;
    tables[selectedTable].seats = updatetableSeats;    
    updateTable=tables[selectedTable];
    console.log(tables[selectedTable]);
    await submitUpdate();
    showUpdateModal = false;
  }

  async function deleteTable(){
    try {
          const response = await fetch('http://localhost:8000/table/'+tableID, {
              method: 'delete',
              credentials: 'include',
          });
          if (response.ok) {
            await fetchTable();
            showUpdateModal = false;
            showDeleteModal = false;
          } else {
              showDeleteModal = false;
              console.error('Error delete table:', response.status);
          }
      } catch (error) {
          showDeleteModal = false;
          console.error('Error fetching table:', error);
      }
  }

  function tryDeleteTable(){
    showDeleteModal=true;
  }

  async function fetchTable(){
    try {
          const response = await fetch('http://localhost:8000/table/all', {
              method: 'GET',
              credentials: 'include',
          });
          if (response.ok) {
              tables = await response.json();
          } else {
              console.error('Error fetching table:', response.status);
              tables = []; // 设置 menus 为空数组
          }
      } catch (error) {
          console.error('Error fetching table:', error);
          tables = []; // 设置 menus 为空数组
      }
  }

  // function addTable(){
  //   if(addTableNumber=='')alert('new table numbaer cannot be empty!');
  //   if(addTableSeats<1)alert('table seats cannot < 1');
  //   else {
  //     newTable.id = addTableNumber;
  //     newTable.seats = addTableSeats;
  //     const now = new Date().toString();
  //     newTable.time=now
  //     newTable.status='idle';
  //     tables.push(newTable);
  //     tables=tables;
  //     showAddTable=false;
  //     console.log(tables);
  //   }
  // }

  async function getOrder(){
    try {
          const response = await fetch('http://localhost:8000/table/table_order/'+tableID, {
              method: 'GET',
              credentials: 'include',
          });
          if (response.ok) {
              tableOrders = await response.json();
          } else {
              console.error('Error fetching table order:', response.status);
              tableOrders = []; // 设置 menus 为空数组
          }
      } catch (error) {
          console.error('Error fetching table order:', error);
          tables = []; // 设置 menus 为空数组
      }
  }

  function crossOutButton(){
    showCrossOutModal = true;
    tableOrder=tableOrders[tableOrders.length-1];
    dishes=tableOrder.dish;
    dishesName = Object.keys(dishes);    
  }

  onMount(async() => {
    await validation();
    await fetchTable();
    // history.replaceState(null, 'Profile', '/profile');
    document.title = 'Dining Staff Page';
  });
</script>

<style>
  .container {
    margin-top: 30px; /* 增加容器的上边距 */
  } 

  .table-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    grid-gap: 30px;
    margin-top: 20px;
  }

  .modal {
    padding: 50px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal-content {
    max-width: 800px;
    padding: 30px;
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    max-width: 600px;
    width: 100%;
  }

  .modal-content h3{
    position: relative;
    display: inline-block;
  }

  .modal-content h4{
    position: relative;
    display: inline-block;
    left: 70%;
  }

  .modal-content .row {
    margin-bottom: 20px;
  }

  .modal-content input {
    height:30px;
  }

  .addModal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .addModal-content {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    max-width: 600px;
    width: 100%;
  }
  .addModal-content .row {
    margin-bottom: 20px;
  }

  .addModal-content input {
    height:30px;
  }

  .addModal-content button{
    margin-left: 5%;
    border:none;
    border-radius: 8%;
    font-size: 12px;
  }

  .table-grid {
    grid-gap: 30px;
  }

  button {
    padding: 10px 20px;
    font-size: 16px;
  }

  .table-container {
    margin: 0 10px;
  }

  .modal select {
    font-size: 16px;
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid #ccc;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .deactiveButton{  
    background-color: #aaa;
    border-color: #aaa;
    color:#B22222;
    height: 2rem;
    width: 6rem;    
    font-size: 1rem;
    background-image: linear-gradient(45deg, #aaa 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .deactiveButton:hover{
    color: white;  border: 0;
    background-color: #B22222;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);
    box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);
  }

  .updateButton{
    background-color: #D3D3D3;
    border-color: #D3D3D3;
    color:#00BFFF;
    height: 2rem;
    width: auto;
    font-size: 1rem;
    background-image: linear-gradient(45deg, #00BFFF 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .updateButton:hover{
    color: black;  border: 0;
    background-color: #00BFFF;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(0,191,255);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(0,191,255);
    box-shadow: 10px 10px 99px 6px rgba(0,191,255);
  }
  
</style>

<div class="container">
  <h2>{role}</h2>
  <div class="row">
    <button>Work</button>
    <button>Get Off Work</button>
    <button on:click={()=> addTableButton()}>Add Table</button>
  </div>
  <div class="table-grid">
    {#each tables as table, index}
      <div class="table-container" on:click={() => handleTableClick(+index)}>
        <Table id={table.id} status={table.status} on:changeStatus={(event) => updateTableStatus(+index, event.detail.status)}/>
      </div>
    {/each}
  </div>
</div>


{#if showAddTable}
<div class="addModal" >
  <div class="addModal-content" on:click|stopPropagation>
    <div class="row">
      <label for= "addTableNumber">New Table Number:</label>
      <input id="addTableNumber" bind:value={addTableNumber} placeholder="Enter New Table Number" />      
    </div>
    <div class="row">
      <label for = "Seats Number">Seats Number:</label>
      <input id = "Seats Number" type=number bind:value={addTableSeats} min=0 placeholder="Enter Seats Number" />    
    </div>
    <button on:click={() => addTable()}>ADD</button>
    <button on:click={() => showAddTable = false}>CLOSE</button>     
  </div>
</div>
{/if}

{#if role == 'Dining Room Staff' && showModal}
<div class="modal" on:click={() => showModal = false}>
  <div class="modal-content" on:click|stopPropagation>
    <h3>Table {tables[selectedTable].id}</h3>
    <h4>{tables[selectedTable].seats} seats</h4>
    <div class="row">
      <select bind:value={tables[selectedTable].status}  on:change={() => updateTableStatus(+selectedTable, tables[selectedTable].status)}>
        <option value="idle">Idle</option>
        <option value="reserved">Reserved</option>
        <option value="occupied">Occupied</option>
      </select>
      <button on:click={() => showModal = false}>CLOSE</button>
    </div>
    <!-- <div class="row">
      <input bind:value={dishNumber} placeholder="Enter Dish Number" />
      <button>Order Food for Customers</button>
    </div> -->
    <div class="row">
      <button on:click={()=> crossOutButton()}>Cross Out Served Dishes</button>
    </div>
    <div class="row">
      <input bind:value={closedTableNumber} placeholder="Enter Closed Table Number" />
      <input bind:value={sum} placeholder="Enter Total Amount" />
      <button>Checkout</button>
    </div>
    <div class="row">
      <input bind:value={note} placeholder="Enter Lost Items and Notes" />
      <button>Report Lost Items</button>
    </div>
    <div class="row">
      <button on:click={() => goToMenu(tables[selectedTable].id)}>Go to Menu</button>
    </div>
    {#if showCrossOutModal}
    <div class="modal" on:click={() => showCrossOutModal = false}>
      <div class="modal-content" on:click|stopPropagation>
        {#each dishesName as dishName}
        <div class="row">          
          {dishName}:{dishes[dishName].amount}
        </div>
        {/each}
      </div>
    </div>
    {/if}
  </div>
</div>
{/if}

{#if role=='Manager'&& showUpdateModal }
<div class="addModal" >
  <div class="modal" on:click={() => showUpdateModal = false}>
    <div class="addModal-content" on:click|stopPropagation>
      <div class="row">
        <label for= "addTableNumber">New Table Number:</label>
        <input id="addTableNumber" bind:value={updateTableID} placeholder="Enter New Table Number" />      
      </div>
      <div class="row">
        <label for = "Seats Number">Seats Number:</label>
        <input id = "Seats Number" type=number bind:value={updatetableSeats} min=0 placeholder="Enter New Seats Number" />    
      </div>
      <button class="updateButton" on:click={() => updatetable()}>UPDATE</button>
      <button on:click={() => showUpdateModal = false}>CLOSE</button>     
      <button class="deactiveButton" on:click={() => tryDeleteTable()}>DELETE</button>
      {#if showDeleteModal}
      <div class="addModal" >
        <div class="modal" on:click={() => showUpdateModal = false}>
          <div class="addModal-content" on:click|stopPropagation>
            <h2>Are you sure deleting it?</h2>
            <button on:click={() => deleteTable()}>DELETE</button>        
            <button on:click={() => showUpdateModal = false}>CLOSE</button> 
          </div>
        </div>
      </div>
      {/if}     
    </div>
  </div>
</div>
{/if}