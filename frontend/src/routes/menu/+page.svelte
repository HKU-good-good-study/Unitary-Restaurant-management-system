<script>
  import { onMount } from 'svelte';
  
  let role = 'customer'; // Change this to 'kitchen', 'manager', or 'customer' based on the current user

  let products = [
    { name: 'Salad', price: 13.99, weight: 'Weight 1', quantity: 0, image: './src/images/chopped-power-salad-with-chicken-0ad93f1931524a679c0f8854d74e6e57.jpg' },
    { name: 'Beef Burger', price: 15.99, weight: 'Weight 2', quantity: 0, image: './src/images/photo-1571091718767-18b5b1457add.avif' },
    // More dishes...
  ];
  let total = 0;

  function updateTotal() {
    total = 0;
    products.forEach((product) => {
      total += product.price * product.quantity;
    });
  }

  function addToCart(index) {
    products[index].quantity += 1;
    updateTotal();
  }

  function removeFromCart(index) {
    if (products[index].quantity > 0) {
      products[index].quantity -= 1;
      updateTotal();
    }
  }

  function changePrice(index, price) {
    // Here you can add communication logic with the backend to update price information
    products[index].price = price;
  }

  function increaseQuantity(index) {
    products[index].quantity += 1;
    updateTotal();
  }

  function decreaseQuantity(index) {
    if (products[index].quantity > 0) {
      products[index].quantity -= 1;
    }
    updateTotal();
  }

  function addProduct() {
    // Here you can add communication logic with the backend and add new dishes
    products.push({ name: 'New Food', price: 'New Price', weight: 'New Weight', quantity: 0, image: 'New Picture' });
  }

  function removeProduct(index) {
    // Here you can add communication logic with the backend and delete dishes
    products.splice(index, 1);
  }

  onMount(() => {
    history.replaceState(null, 'Profile', '/profile');
    document.title = 'Profile';
  });
</script>

<style>
  .menu {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    padding: 20px;
    background-color: #f8f8f8;
  }

  .product {
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    background-color: #fff;
    text-align: center;
    width: 300px; /* Set the width of each product */
  }

  .product h2 {
    color: #333;
    margin-bottom: 10px;
  }

  .product p {
    color: #666;
    margin-bottom: 10px;
  }

  .product img {
    width: 200px; /* Set the width of each product */
    height: auto; /* Automatically adjust height to maintain image proportions */
    object-fit: cover; /* Set the image fill method */
    margin-bottom: 10px;
  }

  .cart {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 20px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }

  .cart h2 {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 15px;
  }

  .cart ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }

  .cart li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e0e0e0;
  }

  .cart button {
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 3px;
    padding: 5px 10px;
    cursor: pointer;
    font-size: 14px;
  }

  .cart button:hover {
    background-color: #0056b3;
  }

  .cart p {
    font-size: 16px;
    font-weight: bold;
    text-align: right;
    margin-top: 15px;
  }

  .quantity-btn {
    width: 40px; /* 设置按钮宽度 */
    height: 40px; /* 设置按钮高度 */
    font-size: 16px; /* 设置按钮内部文字/图标大小 */
    display: inline-flex; /* 使用flexbox布局 */
    justify-content: center; /* 水平居中 */
    align-items: center; /* 垂直居中 */
  }
</style>

<div class="menu">
  {#each products as product, index (product.name)}
  <div class="product">
    <h2>{product.name}</h2>
    <p>Price: {product.price}</p>
    {#if role === 'manager' || role === 'kitchen staff'}
      <input type="text" bind:value={product.price} on:change={() => changePrice(index, product.price)} />
    {/if}
    <p>Weight: {product.weight}</p>
    <p>Quantity: <input type="number" min="0" bind:value={product.quantity} /></p>
    <div>
      <button on:click={() => increaseQuantity(index)} class="quantity-btn">+</button>
<button on:click={() => decreaseQuantity(index)} class="quantity-btn">-</button>
    </div>
    <img src={product.image} />
    {#if role === 'manager' || role === 'kitchen staff'}
      <button on:click={() => removeProduct(index)}>Delete dish</button>
    {/if}
  </div>
  {/each}
  {#if role === 'manager' || role === 'kitchen staff'}
    <button on:click={addProduct}>Add dish</button>
  {/if}
</div>

{#if role === 'customer' || role === 'unregistered'}
  <div class="cart">
    <h2>Your Order</h2>
    <ul>
      {#each products as product, index (product.name)}
        {#if product.quantity > 0}
          <li>
            {product.name} - {product.price} x {product.quantity} = {product.price * product.quantity}
            <button on:click={() => addToCart(index)} class="quantity-btn">+</button>
            <button on:click={() => removeFromCart(index)} class="quantity-btn">-</button>
          </li>
        {/if}
      {/each}
    </ul>
    <p>Total: {total.toFixed(2)}</p>
  </div>
{/if}