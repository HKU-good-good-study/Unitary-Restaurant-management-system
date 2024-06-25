<script>
  import { onMount } from 'svelte';
  import { user } from '../../stores';
  import AddProductModal from './AddProductModal.svelte';

  let role = '';
  role = user.role;

  let products = [
    { id: 1, name: 'Salad', price: 13.99, weight: 120, quantity: 0, image: './src/images/salad.jpg', sold: 0, ingredients: [{'name': 'Carrot', 'weight': 120, 'id': 1}, {'name': 'Lettuce', 'weight': 80, 'id': 2}], description: 'A fresh and healthy salad with a variety of vegetables.' },
    { id: 2, name: 'Beef Burger', price: 15.99, weight: 200, quantity: 0, image: './src/images/beefburger.jpg', sold: 0, ingredients: [{'name': 'Beef Patty', 'weight': 150, 'id': 1}, {'name': 'Bun', 'weight': 50, 'id': 2}], description: 'A juicy beef burger with fresh toppings.' },
  ];
  let total = 0;
  let showAddProductModal = false;

  function updateTotal() {
    total = 0;
    products.forEach((product) => {
      total += product.price * product.quantity;
    });
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
    let newId = products.length + 1;
    products.push({ id: newId, name: 'New Food', price: 'New Price', weight: 'New Weight', quantity: 0, image: 'New Picture', sold: 0, ingredients: [], description: 'New Description' });
    updateTotal();
    showAddProductModal = true;
  }

  function removeProduct(index) {
    products.splice(index, 1);
    updateTotal();
  }

  function handleSaveProduct(newProduct) {
    products.push({
      id: products.length + 1,
      ...newProduct
    });
    products = products;
    updateTotal();
    closeAddProductModal();
  }
  function closeAddProductModal() {
    showAddProductModal = false;
  }


  onMount(() => {
    document.title = 'Menu Page';
  });
</script>

<style>
  /* 整体布局 */
.menu {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  background-color: #f8f8f8;
}

/* 单个菜品 */
.product {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  background-color: #fff;
  text-align: center;
  width: 300px;
}

/* 菜品 ID */
.product .id {
  font-size: 16px;
  color: #666;
  margin-bottom: 5px;
}

/* 菜品名称 */
.product .dish-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

/* 价格 */
.product .price {
  font-size: 16px;
  color: #666;
  margin-bottom: 10px;
}

/* 重量 */
.product .weight {
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

/* 数量控制 */
.product .quantity {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.product .quantity-btn {
  width: 30px;
  height: 30px;
  font-size: 18px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 50%;
  cursor: pointer;
}

.add-dish-btn {
    width: 70px;
    height: 70px;
    font-size: 30px;
    background-color: #f0f0f0;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    margin-left: 10px;
    /* enlarge */
    display: flex;
    justify-content: center;
    align-items: center;
  }

.add-dish-btn:hover {
  background-color: #e0e0e045;
}

.product .quantity-input {
  width: 40px;
  text-align: center;
  margin: 0 10px;
}

/* 图片 */
.product .pic {
  width: 2000px;
  height: 2000px;
  object-fit: cover;
  margin-bottom: 10px;
}

/* 配料 */
.product .ingredients {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

/* 描述 */
.product .description {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

/* 已售数量 */
.product .sold {
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

/* 添加菜品按钮 */
.add-dishes {
  width: 100%;
  text-align: center;
  margin-top: 20px;
}

.add-dishes button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
}

.add-dishes button:hover {
  background-color: #0056b3;
}

.menu {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    padding: 20px;
    background-color: #f8f8f8;
    min-height: calc(100vh - 80px); /* 减去页脚高度 */
    align-items: center;
  }

/* 可用性提示 */
.availability {
  font-size: 14px;
  color: #999;
  margin-top: 20px;
  text-align: center;
}

/* .cart {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  border-top: 1px solid #ddd;
  padding: 10px;
  text-align: right;
  font-size: 16px;
  font-weight: bold;
  height: 80px; 
} */
  
.cart-total {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    font-size: 24px;
    font-weight: bold;
    max-height: 300px; 
    overflow-y: auto; 
  }

  .cart-total p {
    margin: 5px 0;
  }
  
</style>

<div class="menu">
  {#each products as product, index (product.id)}
    <div class="product">
      <p>ID: {product.id}</p>
      <h2>{product.name}</h2>
      <p>Price: ${product.price.toFixed(2)}</p>
      <p>Weight: {product.weight}g</p>
      <div class="quantity">
        <button on:click={() => decreaseQuantity(index)} class="quantity-btn">-</button>
        <span class="quantity-text">Quantity: {product.quantity}</span>
        <button on:click={() => increaseQuantity(index)} class="quantity-btn">+</button>
      </div>
      <img src={product.image} alt={product.name} />
      <h3>Ingredients:</h3>
      <ul>
        {#each product.ingredients as ingredient}
          <li>{ingredient.name} ({ingredient.weight}g)</li>
        {/each}
      </ul>
      <p>{product.description}</p>
      <p>Sold: {product.sold}</p>
      {#if role === "Manager" || role === "Kitchen Staff"}
        <button on:click={() => removeProduct(index)}>Delete dish</button>
      {/if}
    </div>
  {/each}
  {#if role === "Manager" || role === "Kitchen Staff"}
    <button on:click={addProduct} class="add-dish-btn">+</button>
  {/if}
</div>

<AddProductModal
  visible={showAddProductModal}
  onClose={() => (closeAddProductModal())}
  onSave={handleSaveProduct}
/>

{#if role === "Customer" || role === "Dining Room Staff" || role === " "}
<div class="cart-container">
  <div class="cart-calc">
    <h2>Your Order</h2>
    <ul>
      {#each products as product, index (product.id)}
        {#if product.quantity > 0}
          <li>
            {product.name} - ${product.price.toFixed(2)} x {product.quantity} = ${(product.price * product.quantity).toFixed(2)}
            <button on:click={() => increaseQuantity(index)} class="quantity-btn">+</button>
            <button on:click={() => decreaseQuantity(index)} class="quantity-btn">-</button>
          </li>
        {/if}
      {/each}
    </ul>
  </div>
  <div class="cart-total">
    <p>Total: ${total.toFixed(2)}</p>
  </div>
</div>
{/if}