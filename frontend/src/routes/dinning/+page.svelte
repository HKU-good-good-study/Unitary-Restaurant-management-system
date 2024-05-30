<script>
  import Table from 'C:/Users/11570/Desktop/Unitary-Restaurant-management-system/frontend/src/routes/dinning/Tables.svelte';
  let tables = [1, 2, 3, 4, 5]; // 这里可以根据你的实际需求调整餐桌的数量
</script>

<style>
  .table-container {
    border: 1px solid #ccc;
    margin: 10px;
    padding: 10px;
    border-radius: 5px;
  }
</style>

<div class="container">
  <h2>Dinning Staff</h2>
  <div class="row">
    <button>Work</button>
    <button>Get Off Work</button>
  </div>
  {#each tables as tableNumber}
    <div class="table-container">
      <Table {tableNumber} />
    </div>
  {/each}
</div>
