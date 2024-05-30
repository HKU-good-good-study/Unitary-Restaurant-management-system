<script>
  let role = 'manager'; // Change this to 'kitchen', 'manager', or 'customer' based on the current user

  let products = [
    { name: 'Salad', price: 'Price 1', weight: 'Weight 1', quantity: 0, image: './src/images/chopped-power-salad-with-chicken-0ad93f1931524a679c0f8854d74e6e57.jpg' },
    { name: 'Beef Burger', price: 'Price 2', weight: 'Weight 2', quantity: 0, image: './src/images/photo-1571091718767-18b5b1457add.avif' },
    // More dishes...
  ];

  function changePrice(index, price) {
    // Here you can add communication logic with the backend to update price information
    products[index].price = price;
  }

  function increaseQuantity(index) {
    products[index].quantity += 1;
  }

  function decreaseQuantity(index) {
    if (products[index].quantity > 0) {
      products[index].quantity -= 1;
    }
  }

  function addProduct() {
    // Here you can add communication logic with the backend and add new dishes
    products.push({ name: 'New Food', price: 'New Price', weight: 'New Weight', quantity: 0, image: 'New Picture' });
  }

  function removeProduct(index) {
    // Here you can add communication logic with the backend and delete dishes
    products.splice(index, 1);
  }
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
      <p>Quantity: {product.quantity}</p>
      <button on:click={() => increaseQuantity(index)}>+</button>
      <button on:click={() => decreaseQuantity(index)}>-</button>
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
