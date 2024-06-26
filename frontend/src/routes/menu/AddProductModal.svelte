<script>
    import IngredientModal from './IngredientModal.svelte';
    export let visible = false;
    export let onClose;
    export let onSave;
  
    let name = '';
    let price = '';
    let weight = '';
    let ingredients = [];
    let description = '';
    let image = '';
  
    let ingredientModalVisible = false;
    let editingIngredient = null;

    function handleSave() {
      onSave({ name, price, weight, ingredients, description, image });
      name = '';
      price = '';
      weight = '';
      ingredients = [];
      description = '';
      image = '';
    }

    function handleAddIngredient(ingredient) {
      ingredients = [...ingredients, ingredient];
      ingredientModalVisible = false;
      editingIngredient = null;
    }

    function handleEditIngredient(index) {
      editingIngredient = ingredients[index];
      ingredientModalVisible = true;
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
    }
  
    label {
      display: block;
      font-weight: bold;
      margin-bottom: 5px;
    }
  
    input, textarea {
      width: 100%;
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

    /* Existing styles */
  .ingredient-item {
    display: inline-block;
    background-color: #f1f1f1;
    padding: 5px 10px;
    border-radius: 5px;
    margin-right: 5px;
    cursor: pointer;
  }
  </style>
  
  {#if visible}
    <div class="modal" on:click|self={onClose}>
      <div class="modal-content">
        <h2>Add New Dish</h2>
        <form on:submit|preventDefault={handleSave}>
          <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" bind:value={name} required />
          </div>
          <div class="form-group">
            <label for="price">Price:</label>
            <input type="number" id="price" bind:value={price} required />
          </div>
          <div class="form-group">
            <label for="weight">Weight:</label>
            <input type="number" id="weight" bind:value={weight} required />
          </div>
          <div class="form-group">
            <label for="ingredients">Ingredients:</label>
            <!-- <textarea id="ingredients" bind:value={ingredients} required></textarea> -->
            <div>
              {#each ingredients as ingredient, i}
                <div class="ingredient-item" on:click={() => handleEditIngredient(i)}>
                  {ingredient.name} - {ingredient.weight} g
                </div>
              {/each}
              <button type="button" class="ingredient-button" on:click={() => (ingredientModalVisible = true, editingIngredient = null)}>+</button>
            </div>
          </div>
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" bind:value={description} required></textarea>
          </div>
          <div class="form-group">
            <label for="image">Image:</label>
            <input type="text" id="image" bind:value={image} required />
          </div>
          <div class="actions">
            <button type="submit">Save</button>
            <button type="button" on:click={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>

    {#if ingredientModalVisible}
      <IngredientModal
        visible={ingredientModalVisible}
        onClose={() => (ingredientModalVisible = false, editingIngredient = null)}
        onSave={editingIngredient ? handleEditIngredient : handleAddIngredient}
        ingredient={editingIngredient}
      />
    {/if}
  {/if}


