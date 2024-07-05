<script>
  import Table from './Tables.svelte';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { validation } from '$lib/tool.svelte';
    import Tables from './Tables.svelte';

  // 创建一个对象来存储每个 table 的状态
  let tableStatus = {
    1: 'idle',
    2: 'idle',
    3: 'idle',
    4: 'reserved',
    5: 'idle',
    6: 'occupied',
    7: 'reserved',
    8: 'idle',
    9: 'occupied',
    10: 'occupied',
    11: 'idle',
    12: 'idle',
    13: 'idle',
    14: 'idle',
    15: 'idle',
    16: 'idle',
    17: 'idle',
    18: 'occupied',
    19: 'idle',
    20: 'idle',
    21: 'idle'
  };

  let tables=[{id: "A1",order: {},status: "idle",time: new Date(),seats: 2},
  {id: "A2",order: {},status: "occupied",time: new Date(),seats: 2},
  {id: "A3",order: {},status: "idle",time: new Date(),seats: 2},
  {id: "A4",order: {},status: "reserved",time: new Date(),seats: 2},
  {id: "A5",order: {},status: "idle",time: new Date(),seats: 2},
  {id: "B1",order: {},status: "reserved",time: new Date(),seats: 4},
  {id: "B2",order: {},status: "idle",time: new Date(),seats: 4},
  {id: "B3",order: {},status: "occupied",time: new Date(),seats: 4},
  {id: "B4",order: {},status: "reserved",time: new Date(),seats: 4},
  {id: "C1",order: {},status: "idle",time: new Date(),seats: 8},
  {id: "C2",order: {},status: "idle",time: new Date(),seats: 8},
  {id: "C3",order: {},status: "occupied",time: new Date(),seats: 8},
  {id: "C4",order: {},status: "idle",time: new Date(),seats: 8},
  {id: "D1",order: {},status: "reserved",time: new Date(),seats: 10},
  {id: "D2",order: {},status: "idle",time: new Date(),seats: 10},
  ];


  let selectedTable = '';
  let showModal = false;
  let dishNumber = '';
  let closedTableNumber = '';
  let sum = '';
  let note = '';
  let showAddTable = false;

  let addTableSeats=0;
  let addTableNumber ='';
  let newTable={
    id: "",
    order: {},
    status: "idle",
    time: new Date(),
    seats: 0
  }

  function handleTableClick(tableNumber) {
    selectedTable = tableNumber;
    showModal = true;
  }

  function setTableStatus(tableNumber, newStatus) {
    tables[tableNumber].status = newStatus;
    console.log(tables);
  }

  function goToMenu() {
    goto('./menu');
  }

  function addTableButton(){
    addTableNumber = '';
    addTableSeats = 0;
    showAddTable=true;
  }

  // async function addTable(){
  //   if(addTableNumber=='')alert('new table numbaer cannot be empty!');
  //   else {
  //     newTableNumber = addTableNumber;
  //     newTableSeats = addTableSeats;
  //     const now = new Date();
  //     newTable.id=newTableNumber;
  //     newTable.time=now;
  //     const response = await fetch('http://localhost:8000/table/'+newTableNumber,{
  //         method: 'post',
  //         headers: {
  //               'Content-Type': 'application/json'
  //           },
  //           credentials: 'include', // This is important for cookies to be sent
  //           body: JSON.stringify(newTable)
  //     });
  //     if (response.ok) {
        
  //     } 
  //     else {
  //         console.error('Error fetching addTable:', response.status);
  //     }    
  //     showAddTable=false;
  //   }
  // }

  function addTable(){
    if(addTableNumber=='')alert('new table numbaer cannot be empty!');
    if(addTableSeats<1)alert('table seats cannot < 1');
    else {
      newTable.id = addTableNumber;
      newTable.seats = addTableSeats;
      const now = new Date();
      newTable.time=now
      newTable.status='idle';
      tables.push(newTable);
      tables=tables;
      showAddTable=false;
      console.log(tables);
    }
  }

  onMount(async() => {
    await validation();
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

  
</style>

<div class="container">
  <h2>Dining Staff</h2>
  <div class="row">
    <button>Work</button>
    <button>Get Off Work</button>
    <button on:click={()=> addTableButton()}>Add Table</button>
  </div>
  <div class="table-grid">
    {#each tables as table, index}
      <div class="table-container" on:click={() => handleTableClick(+index)}>
        <Table id={table.id} status={table.status} on:changeStatus={(event) => setTableStatus(+index, event.detail.status)} />
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

{#if showModal}
<div class="modal" on:click={() => showModal = false}>
  <div class="modal-content" on:click|stopPropagation>
    <h3>Table {tables[selectedTable].id}</h3>
    <h4>{tables[selectedTable].seats} seats</h4>
    <div class="row">
      <select bind:value={tables[selectedTable].status}>
        <option value="idle">Idle</option>
        <option value="reserved">Reserved</option>
        <option value="occupied">Occupied</option>
      </select>
      <button on:click={() => showModal = false}>CLOSE</button>
    </div>
    <div class="row">
      <input bind:value={dishNumber} placeholder="Enter Dish Number" />
      <button>Order Food for Customers</button>
    </div>
    <div class="row">
      <button>Cross Out Served Dishes</button>
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
      <button on:click={goToMenu}>Go to Menu</button>
    </div>
  </div>
</div>
{/if}