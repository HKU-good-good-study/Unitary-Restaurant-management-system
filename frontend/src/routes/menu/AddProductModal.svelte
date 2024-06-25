<!-- <script>
    export let visible = false;
    export let onClose = () => {};
    export let onSave = () => {};
  
    let name = '';
    let price = 0;
    let weight = 0;
    let ingredients = [];
    let description = '';
    let image = '';
  
    function handleSave() {
      onSave({
        name,
        price,
        weight,
        ingredients,
        description,
        image
      });
      onClose();
    }
  
    function handleFileUpload(event) {
      image = event.target.files[0];
    }
  </script>
  
  <style>
    .modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.form-group label {
  width: 100px;
  font-size: 16px;
  font-weight: bold;
  margin-right: 10px;
}

.form-group input,
.form-group textarea {
  flex: 1;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.actions button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
  margin-left: 10px;
}

.actions button:hover {
  background-color: #0056b3;
}

  </style>
  
  {#if visible}
    <div class="modal" on:click={onClose}>
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
                <textarea id="ingredients" bind:value={ingredients} required></textarea>
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
  {/if} -->


  <script>
    export let visible = false;
    export let onClose;
    export let onSave;
  
    let name = '';
    let price = '';
    let weight = '';
    let ingredients = '';
    let description = '';
    let image = '';
  
    function handleSave() {
      onSave({ name, price, weight, ingredients, description, image });
      name = '';
      price = '';
      weight = '';
      ingredients = '';
      description = '';
      image = '';
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
            <textarea id="ingredients" bind:value={ingredients} required></textarea>
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
  {/if}