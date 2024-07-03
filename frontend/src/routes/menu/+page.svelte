<script>
    import { onMount } from 'svelte';
    import { user } from '../../stores';
  
    let role = '';
    role = user.role;
  
    let menus = [];
    // let newMenu = { "availability": true, "desc": "", "id": "3", "image": "123", "ingredient": [ { "name": "", "weight": 0 } ], "name": "Beef Chow Fun", "price": 45, "sold": 45, "weight": 450 };
    let newMenu = {
        availability: true,
        desc: "",
        id: "",
        image: "",
        ingredient: [],
        name: "",
        price: 0,
        sold: 0,
        weight: 0
    };

    let ingredients = [
        { name: '', weight: 0 }
    ];
    let totalPrice = 0;
    let quantities = {};
    let showAddMenu = false;
  
    onMount(async () => {
        await fetchMenus();
        role = user.role;
  
    });
  
    async function fetchMenus() {
        const response = await fetch('http://localhost:8000/menu/all' ,{
          method: 'GET',
          credentials: 'include',
        });
        menus = await response.json();
    }
  
    function addIngredient() {
        ingredients = [...ingredients, { name: '', weight: 0 }];
    }
  
    function removeIngredient(index) {
        ingredients.splice(index, 1);
        ingredients = ingredients;
    }
  
    async function saveMenu() {
        while (!lock) {}
        newMenu.name = document.getElementById('menuName').value;
        newMenu.price = document.getElementById('menuPrice').value;
        newMenu.weight = document.getElementById('menuWeight').value;
        newMenu.availability = document.getElementById('menuAvail').checked;
        newMenu.desc = document.getElementById('menuDes').value;
        newMenu.sold = document.getElementById('menuSold').value;


        const response = await fetch('http://localhost:8000/menu/'+newMenu.id, {
            method: 'POST',
            headers: {
                  'Content-Type': 'application/json'
              },
            body: JSON.stringify(newMenu),
  
            credentials: 'include'
        });
        const createdMenu = await response.json();
  
        showAddMenu = false;
        lock = false;
    }
  
    function updateQuantity(menuId, operation) {
        if (operation === 'increment') {
            quantities[menuId] = (quantities[menuId] || 0) + 1;
        } else {
            quantities[menuId] = Math.max(0, (quantities[menuId] || 0) - 1);
        }
        calculateTotalPrice();
    }
  
    function calculateTotalPrice() {
        totalPrice = Object.entries(quantities).reduce((acc, [menuId, quantity]) => {
            const menu = menus.find(m => m.id === parseInt(menuId));
            return acc + (menu?.price || 0) * quantity;
        }, 0);
    }
    var lock = false;
    function getImage(file){
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = e => {
          newMenu.image= e.target.result;
          lock = true;
          newMenu.image = newMenu.image.split(',')[1];
          // newMenu.image = "123";
      };
    }
  </script>
  
  <h1>Menu</h1>
  
  {#if role === 'Manager' || role === 'Kitchen Staff'}
  <div>
      <button on:click={() => showAddMenu = true}>Add New Menu</button>
      {#if showAddMenu}
      <div class="add-menu-container">
          <div class="add-menu-form">
              <h2>Add New Menu</h2>
              <form on:submit|preventDefault={saveMenu}>
                  <!-- <label>
                        ID:
                        <input type="text" id="menuId" required>
                  </label> -->
                  <label>
                      Name:
                      <input type="text" id="menuName" required>
                  </label>
                  <label>
                      Price:
                      <input type="number" step="1" id="menuPrice" min="0" required>
                  </label>
                  <label>
                      Weight:
                      <input type="number" step="1" id="menuWeight" min="0" required>
                  </label>
                  <label>
                      Ingredients:
                      {#each ingredients as ingredient, index}
                      <div class="ingredient-container">
                          <input type="text" bind:value={ingredient.name} placeholder="Ingredient Name" required>
                          <input type="number" step="1" bind:value={ingredient.weight} placeholder="Ingredient Weight" min="0" required>
                          <button type="button" on:click={() => removeIngredient(index)}>x</button>
                      </div>
                      {/each}
                      <button type="button" on:click={addIngredient}>Add Ingredient</button>
                  </label>
                  <label>
                      Sold:
                      <input type="number" step="1" id="menuSold" min="0" required>
                  </label>
                  <label>
                      Availability:
                      <input type="checkbox" id="menuAvail">
                  </label>
                  <label>
                      Description:
                      <textarea id="menuDes" required></textarea>
                  </label>
                  <label>
                      Image:
                      <input type="file" on:change={(e) => getImage(e.target.files[0])}>
                  </label>
                  <button type="submit" on:click={() => fetchMenus}>Save</button>
                  <button type="button" on:click={() => showAddMenu = false}>Cancel</button>
              </form>
          </div>
      </div>
      {/if}
  </div>
  {/if}
  
  <h2>Menu List</h2>
  <div class="menu-list">
      {#each menus as menu}
      <div class="menu-item">
          <p>ID: {menu.id}</p>
          <p>Name: {menu.name}</p>
          <p>Price: ${menu.price}</p>
          <p>Weight: {menu.weight}g</p>
          {#if role !== 'Manager' && role !== 'kitchen staff'}
          <div class="quantity-container">
              <button on:click={() => updateQuantity(menu.id, 'decrement')}>-</button>
              <span>{quantities[menu.id] || 0}</span>
              <button on:click={() => updateQuantity(menu.id, 'increment')}>+</button>
          </div>
          {/if}
          <p>Ingredients:</p>
          {#each menu.ingredient as ingredient}
          <div class="ingredient-info">
              <p>{ingredient.name} - {ingredient.weight}g</p>
          </div>
          {/each}
          <p>Sold: {menu.sold}</p>
          <p>Availability: {menu.availability ? 'Yes' : 'No'}</p>
          <p>Description: {menu.desc}</p>
          <!-- <img src={`data:image/jpeg;base64,${btoa(String.fromCharCode(...new Uint8Array(menu.image)))}`} alt="{menu.name} image"> -->
          <img src={`data:image/jpeg;base64,${menu.image}`} alt="{menu.name} image" />
          {#if role === 'Manager' || role === 'Kitchen Staff'}
          <div class="actions">
              <button>Edit</button>
              <button>Delete</button>
          </div>
          {/if}
      </div>
      {/each}
  </div>
  
  {#if role !== 'Manager' && role !== 'Kitchen Staff'}
  <div class="total-price-container">
      <p>Total Price: ${totalPrice.toFixed(2)}</p>
  </div>
  {/if}
  
  <style>
      .menu-list {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
      }
  
      .menu-item {
          border: 1px solid #ccc;
          padding: 20px;
      }
  
      .ingredient-container {
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 10px;
      }
  
      .ingredient-info {
          background-color: #f5f5f5;
          padding: 5px 10px;
          border-radius: 5px;
      }
  
      .quantity-container {
          display: flex;
          align-items: center;
          gap: 10px;
      }
  
      .actions {
          display: flex;
          justify-content: flex-end;
          gap: 10px;
          margin-top: 10px;
      }
  
      .total-price-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f5f5f5;
        padding: 10px;
        text-align: right;
    }
  
    .add-menu-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 999;
    }
  
    .add-menu-form {
      background-color: white;
      padding: 20px;
      border-radius: 5px;
      width: 80%;
      max-width: 600px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
  
    .add-menu-form label {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      margin-bottom: 10px;
      width: 100%;
    }
  
    .add-menu-form input,
    .add-menu-form textarea {
      width: 100%;
      padding: 5px;
      border: 1px solid #ccc;
      border-radius: 3px;
    }
  
    .add-menu-form button {
      margin-top: 10px;
      padding: 5px 10px;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 3px;
      cursor: pointer;
    }
  
    .add-menu-form button:hover {
        background-color: #45a049;
    }
  </style>