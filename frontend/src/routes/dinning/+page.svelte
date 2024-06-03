<script>
  import Table from './Tables.svelte';
  let tables = Array.from({ length: 21 }, (_, i) => i + 1); // 创建21个餐桌
  const rowSize = 7; // 每行7个餐桌
</script>

<style>
  .table-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    grid-gap: 10px;
  }

  .table-container {
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    cursor: pointer;
  }
</style>

<div class="container">
  <h2>Dining Staff</h2>
  <div class="row">
    <button>Work</button>
    <button>Get Off Work</button>
  </div>
  <div class="table-grid">
    {#each tables as tableNumber}
      <div class="table-container" on:click={() => showModal = true}>
        <Table {tableNumber} />
      </div>
    {/each}
  </div>
</div>