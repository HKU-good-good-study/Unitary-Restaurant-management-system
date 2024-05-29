   <script>
    let tableNumber = '';
    let dishNumber = '';
    let closedTableNumber = '';
    let sum = '';
    let note = '';
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
  
  <div class="container">
    <h2>Dinning Staff</h2>
    <div class="row">
      <button>Work</button>
      <button>Get Off Work</button>
    </div>
    <div class="row">
      <input bind:value={tableNumber} placeholder="Enter Table Number" />
      <button>Open Table</button>
      <button>Reserve</button>
      <button>Closure</button>
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
      <button>Turn On Lining Machine</button>
    </div>
  </div>
