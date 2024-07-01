<script>
  import { onMount } from 'svelte';
  import { fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  let menuItems = [];
  let newMenuItem = {
    id: '',
    name: '',
    price: '',
    weight: '',
    ingredient: [],
    sold: '',
    availability: true,
    desc: '',
    image: null
  };
  let showModal = false;
  let newIngredient = { name: '', weight: '' };
  let ingredients = [];

  onMount(async () => {
    await fetchMenuItems();
  });

  async function fetchMenuItems() {
    try {
      const response = await fetch('http://localhost:8000/api/menu');
      menuItems = await response.json();
    } catch (error) {
      console.error('Error fetching menu items:', error);
    }
  }

  async function createMenuItem() {
    try {
      const response = await fetch('http://localhost:8000/api/menu', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newMenuItem)
      });
      const createdMenuItem = await response.json();
      menuItems = [...menuItems, createdMenuItem];
      resetNewMenuItem();
      showModal = false;
    } catch (error) {
      console.error('Error creating menu item:', error);
    }
  }

  function resetNewMenuItem() {
    newMenuItem = {
      id: '',
      name: '',
      price: '',
      weight: '',
      ingredient: [],
      sold: '',
      availability: true,
      desc: '',
      image: null
    };
    ingredients = [];
  }

  function toggleModal() {
    showModal = !showModal;
  }

  function addIngredient() {
    ingredients = [...ingredients, newIngredient];
    newMenuItem.ingredient = ingredients;
    newIngredient = { name: '', weight: '' };
  }

  function removeIngredient(index) {
    ingredients.splice(index, 1);
    ingredients = ingredients;
    newMenuItem.ingredient = ingredients;
  }

  function handleFileInput(event) {
    newMenuItem.image = event.target.files[0];
  }
</script>

<main>
  <h1>Menu</h1>
  <button on:click={toggleModal}>Add New Menu Item</button>

  {#if showModal}
    <div class="modal" transition:fly={{ y: 200, duration: 300, easing: quintOut }}>
      <div class="modal-content">
        <span class="close-button" on:click={toggleModal}>&times;</span>
        <h2>Add New Menu Item</h2>
        <form on:submit|preventDefault={createMenuItem}>
          <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" bind:value={newMenuItem.name} required />
          </div>
          <div class="form-group">
            <label for="price">Price:</label>
            <input type="number" id="price" bind:value={newMenuItem.price} required />
          </div>
          <div class="form-group">
            <label for="weight">Weight:</label>
            <input type="number" id="weight" bind:value={newMenuItem.weight} required />
          </div>
          <div class="form-group">
            <label for="sold">Sold:</label>
            <input type="number" id="sold" bind:value={newMenuItem.sold} required />
          </div>
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" bind:value={newMenuItem.desc} required></textarea>
          </div>
          <div class="form-group">
            <label for="availability">Availability:</label>
            <input type="checkbox" id="availability" bind:checked={newMenuItem.availability} />
          </div>
          <h3>Ingredients</h3>
          {#each ingredients as ingredient, index}
            <div class="ingredient-box">
              <span>{ingredient.name} - {ingredient.weight}</span>
              <span class="close-button" on:click={() => removeIngredient(index)}>&times;</span>
            </div>
          {/each}
          <div class="ingredient-input">
            <input type="text" bind:value={newIngredient.name} placeholder="Ingredient Name" />
            <input type="number" bind:value={newIngredient.weight} placeholder="Ingredient Weight" />
            <button type="button" on:click={addIngredient}>Add Ingredient</button>
          </div>
          <div class="form-group">
            <label for="image">Image:</label>
            <input type="file" id="image" on:change={handleFileInput} />
          </div>
          <button type="submit" class="save-button">Save</button>
        </form>
      </div>
    </div>
  {/if}

  <div class="menu-items">
    {#each menuItems as item}
      <div class="menu-item-box">
        <p>ID: {item.id}</p>
        <p>Name: {item.name}</p>
        <p>Price: {item.price}</p>
        <p>Weight: {item.weight}</p>
        <p>Ingredients:</p>
        {#each item.ingredient as ingredient}
          <p>{ingredient.name} - {ingredient.weight}</p>
        {/each}
        <p>Sold: {item.sold}</p>
        <p>Availability: {item.availability ? 'Available' : 'Unavailable'}</p>
        <p>Description: {item.desc}</p>
        {#if item.image}
          <img src={URL.createObjectURL(item.image)} alt={item.name} />
        {/if}
      </div>
    {/each}
  </div>
</main>

<style>
  .modal {
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal-content {
    background-color: #fefefe;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 600px;
  }

  .close-button {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }

  .close-button:hover,
  .close-button:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }

  .menu-items {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-gap: 20px;
  }

  .menu-item-box {
    border: 1px solid #ccc;
    padding: 20px;
    text-align: left;
  }

  .ingredient-box {
    background-color: #f1f1f1;
    padding: 5px 10px;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .ingredient-input {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }

  .ingredient-input input {
    flex-grow: 1;
  }

  .form-group {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
  }

  .form-group label {
    flex-basis: 100px;
    text-align: right;
    margin-right: 1rem;
  }

  .form-group input,
  .form-group textarea {
    flex-grow: 1;
  }

  .save-button {
    font-size: 1.2rem;
    padding: 0.8rem 1.5rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .save-button:hover {
    background-color: #45a049;
  }
</style>