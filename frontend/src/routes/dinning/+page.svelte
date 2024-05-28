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
    }
  
    h2 {
      text-align: center;
      color: #333;
      margin-bottom: 20px;
    }
  
    .container {
      max-width: 600px;
      margin: 0 auto;
      background-color: white;
      padding: 20px;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
  
    .row {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
    }
  
    .row > * {
      margin-right: 10px;
    }
  
    input {
      padding: 8px 12px;
      border: 1px solid #ccc;
      border-radius: 3px;
      flex-grow: 1;
    }
  
    button {
      background-color: #4CAF50;
      color: white;
      padding: 8px 12px;
      border: none;
      border-radius: 3px;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #45a049;
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

<div>
    <h2>Restaurant staff functions</h2>
    <div>
      <button>work</button>
      <button>get off work</button>
    </div>
    <div>
      <input bind:value={tableNumber} placeholder="Enter table number" />
      <button>open table</button>
      <button>Reserve</button>
      <button>closure</button>
    </div>
    <div>
      <input bind:value={dishNumber} placeholder="Enter dish number" />
      <button>Order food for customers</button>
    </div>
    <div>
      <button>Cross out the dishes that have been served</button>
    </div>
    <div>
      <input bind:value={closedTableNumber} placeholder="Enter the closed table number" />
      <input bind:value={sum} placeholder="Enter total amount" />
      <button>Checkout</button>
    </div>
    <div>
      <input bind:value={note} placeholder="Enter lost items and notes" />
      <button>Report lost items</button>
    </div>
    <div>
      <button>Turn on lining machine</button>
    </div>
</div>
  