<script>
  import Table from './Tables.svelte';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

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

  let selectedTable = null;
  let showModal = false;
  let dishNumber = '';
  let closedTableNumber = '';
  let sum = '';
  let note = '';

  function handleTableClick(tableNumber) {
    selectedTable = tableNumber;
    showModal = true;
  }

  function setTableStatus(tableNumber, newStatus) {
    tableStatus[tableNumber] = newStatus;
  }

  function goToMenu() {
    goto('./menu');
  }

  onMount(() => {
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

  .modal-content .row {
    margin-bottom: 20px;
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
  </div>
  <div class="table-grid">
    {#each Object.keys(tableStatus) as tableNumber}
      <div class="table-container" on:click={() => handleTableClick(+tableNumber)}>
        <Table {tableNumber} status={tableStatus[tableNumber]} on:changeStatus={(event) => setTableStatus(+tableNumber, event.detail.status)} />
      </div>
    {/each}
  </div>
</div>

{#if showModal}
<div class="modal" on:click={() => showModal = false}>
  <div class="modal-content" on:click|stopPropagation>
    <h3>Table {selectedTable}</h3>
    <div class="row">
      <select bind:value={tableStatus[selectedTable]}>
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