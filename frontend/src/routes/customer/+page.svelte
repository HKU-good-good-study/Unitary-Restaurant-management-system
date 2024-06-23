<script>
  import { onMount } from 'svelte';

  let reservationStatus = '';
  let orderStatus = '';
  let complaintStatus = '';
  let billStatus = '';
  let lineStatus = '';
  let showComplaintDialog = false;
  let complaintText = '';

  function handleComplaint() {
    showComplaintDialog = true;
  }

  function submitComplaint() {
    // 处理投诉内容
    console.log('Complaint:', complaintText);
    showComplaintDialog = false;
    complaintText = '';
  }

  function closeComplaintDialog() {
    showComplaintDialog = false;
    complaintText = '';
  }

  onMount(() => {
    // history.replaceState(null, 'Profile', '/profile');
    document.title = 'Customer Page';
  });
</script>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 80%;
    margin: auto;
    font-family: Arial, sans-serif;
  }
  .row {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-bottom: 20px;
  }
  .row p {
    flex-basis: 70%;
  }
  .row button {
    flex-basis: 20%;
    height: 40px;
    background-color: #f8f8f8;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
  }
  .row button:hover {
    background-color: #ddd;
  }
  .complaint-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  z-index: 100;
}

.complaint-dialog h3 {
  margin-top: 0;
}

.complaint-dialog textarea {
  width: 400px;
  height: 150px;
  font-size: 16px;
  padding: 10px;
}

.complaint-dialog button {
  margin-top: 10px;
}
</style>

<div class="container">
  <h2>Restaurant page</h2>
  <div class="row">
    <p>Booking status: {reservationStatus}</p>
    <button on:click={() => {/* 处理预订 */}}>Booking</button>
  </div>

  <div class="row">
    <p>Order status: {orderStatus}</p>
    <button on:click={() => {/* 处理点菜 */}}>Ordering</button>
  </div>

  <div class="row">
      <p>Bill status: {billStatus}</p>
      <button on:click={() => {/* 处理结账 */}}>Check Out</button>
  </div>
  
  <div class="row">
      <p>Queue status: {lineStatus}</p>
      <button on:click={() => {/* 处理排队 */}}>Line Up</button>
  </div>

    

  <div class="row">
      <p>Complaint status: {complaintStatus}</p>
      <button on:click={handleComplaint}>Complaint</button>
  </div>
  
    {#if showComplaintDialog}
      <div class="complaint-dialog">
        <h3>File a Complaint</h3>
        <textarea bind:value={complaintText} placeholder="Enter your complaint here..."></textarea>
        <button on:click={submitComplaint}>Submit</button>
        <button on:click={closeComplaintDialog}>Cancel</button>
      </div>
    {/if}
</div>
