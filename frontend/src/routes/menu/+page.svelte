<!-- <script>
  let role = 'manager'; // Change this to 'kitchen', 'manager', or 'customer' based on the current user

  let products = [
    { name: '商品1', price: '价格1', weight: '重量1' , image: './src/images/chopped-power-salad-with-chicken-0ad93f1931524a679c0f8854d74e6e57.jpg'},
    { name: '商品2', price: '价格2', weight: '重量2' , image: './src/images/photo-1571091718767-18b5b1457add.avif'},
    // 更多商品...
  ];

  function changePrice(index, price) {
    // 在这里可以添加与后端的通信逻辑，更新价格信息
    products[index].price = price;
  }

  function addProduct() {
    // 在这里可以添加与后端的通信逻辑，添加新的菜品
    products.push({ name: '新商品', price: '新价格', weight: '新重量', image: '新图片' });
  }

  function removeProduct(index) {
    // 在这里可以添加与后端的通信逻辑，删除菜品
    products.splice(index, 1);
  }
</script>

<style>
  .menu {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 20px;
    background-color: #f8f8f8;
  }
  .product {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    background-color: #fff;
    text-align: center;
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
  width: 200px;  /* 设置图片的宽度 */
  height: auto;  /* 自动调整高度以保持图片的比例 */
  object-fit: cover; /* 设置图片的填充方式 */
}

</style>

<div class="menu">
  {#each products as product, index (product.name)}
    <div class="product">
      <h2>{product.name}</h2>
      <p>价格: {product.price}</p>
      {#if role === 'manager' || role === 'kitchen'}
        <input type="text" bind:value={product.price} on:change={() => changePrice(index, product.price)} />
      {/if}
      <p>重量: {product.weight}</p>
      <img src={product.image}>
      {#if role === 'manager' || role === 'kitchen'}
        <button on:click={() => removeProduct(index)}>Delete dish</button>
      {/if}
    </div>
  {/each}
  {#if role === 'manager' || role === 'kitchen'}
    <button on:click={addProduct}>Add dish</button>
  {/if}
</div> -->
<script>
  let role = 'manager'; // Change this to 'kitchen', 'manager', or 'customer' based on the current user

  let products = [
    { name: '商品1', price: '价格1', weight: '重量1', image: './src/images/chopped-power-salad-with-chicken-0ad93f1931524a679c0f8854d74e6e57.jpg' },
    { name: '商品2', price: '价格2', weight: '重量2', image: './src/images/photo-1571091718767-18b5b1457add.avif' },
    // 更多商品...
  ];

  function changePrice(index, price) {
    // 在这里可以添加与后端的通信逻辑,更新价格信息
    products[index].price = price;
  }

  function addProduct() {
    // 在这里可以添加与后端的通信逻辑,添加新的菜品
    products.push({ name: '新商品', price: '新价格', weight: '新重量', image: '新图片' });
  }

  function removeProduct(index) {
    // 在这里可以添加与后端的通信逻辑,删除菜品
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
    width: 300px; /* 设置每个产品的宽度 */
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
    width: 200px; /* 设置图片的宽度 */
    height: auto; /* 自动调整高度以保持图片的比例 */
    object-fit: cover; /* 设置图片的填充方式 */
    margin-bottom: 10px;
  }
</style>

<div class="menu">
  {#each products as product, index (product.name)}
    <div class="product">
      <h2>{product.name}</h2>
      <p>价格: {product.price}</p>
      {#if role === 'manager' || role === 'kitchen'}
        <input type="text" bind:value={product.price} on:change={() => changePrice(index, product.price)} />
      {/if}
      <p>重量: {product.weight}</p>
      <img src={product.image} />
      {#if role === 'manager' || role === 'kitchen'}
        <button on:click={() => removeProduct(index)}>Delete dish</button>
      {/if}
    </div>
  {/each}
  {#if role === 'manager' || role === 'kitchen'}
    <button on:click={addProduct}>Add dish</button>
  {/if}
</div>