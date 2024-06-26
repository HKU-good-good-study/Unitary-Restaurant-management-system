<script>
    export let visible = false;
    export let onClose;
    export let onSave;
    export let ingredient = null;
  
    let ingredientName = '';
    let ingredientWeight = '';

    $: {
        if (ingredient) {
        ingredientName = ingredient.name;
        ingredientWeight = ingredient.weight;
        }
    }
  
    function handleSave() {
      onSave({ name: ingredientName, weight: ingredientWeight });
      ingredientName = '';
      ingredientWeight = '';
      onClose();
    }
  </script>
  
  <style>
    .modal {
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
      background-color: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
      width: 400px;
    }
  
    .form-group {
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  
    label {
      font-weight: bold;
      margin-right: 10px;
    }
  
    input {
      flex-grow: 1;
      padding: 5px;
      border: 1px solid #ccc;
      border-radius: 3px;
    }
  
    .actions {
      display: flex;
      justify-content: flex-end;
      margin-top: 10px;
    }
  
    button {
      margin-left: 10px;
    }
  </style>
  
  {#if visible}
    <div class="modal" on:click|self={onClose}>
      <div class="modal-content">
        <h2>Add Ingredient</h2>
        <form on:submit|preventDefault={handleSave}>
          <div class="form-group">
            <label for="ingredientName">Ingredient Name:</label>
            <input type="text" id="ingredientName" bind:value={ingredientName} required />
          </div>
          <div class="form-group">
            <label for="ingredientWeight">Weight:</label>
            <input type="number" id="ingredientWeight" bind:value={ingredientWeight} required />
          </div>
          <div class="actions">
            <button type="submit">Save</button>
            <button type="button" on:click={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  {/if}