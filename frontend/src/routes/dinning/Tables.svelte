<script>
  export let tableNumber;
  export let status; // 接收当前餐桌的状态
</script>

<style>
  .table {
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    cursor: pointer;
  }

  .table.idle {
    border-color: #ccc;
  }

  .table.reserved {
    border-color: #FFB74D;
  }

  .table.occupied {
    border-color: #E53935;
  }
</style>

<div class="table {status}">Table {tableNumber}</div>

<!-- <script>
  import { goto } from '$app/navigation'; /* go to menu page after pressing "go to menu"*/

  export let tableNumber;
  let dishNumber = '';
  let closedTableNumber = '';
  let sum = '';
  let note = '';
  let showModal = false;

  function goToMenu() {
      goto('./menu');
  }
</script>

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
    max-width: 600px;
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
  }

  button {
    background-color: #333;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
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

<div class="table" on:click="{() => showModal = true}">
<h3>Table {tableNumber}</h3>
</div>

{#if showModal}
<div class="modal" on:click="{() => showModal = false}">
    <div class="modal-content" on:click|stopPropagation>
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
        <div class="row">
            <button on:click="{() => showModal = false}">CLOSE</button>
        </div>
    </div>
</div>
{/if}
 -->
