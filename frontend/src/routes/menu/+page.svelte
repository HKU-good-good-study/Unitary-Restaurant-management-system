<script>
    import { onMount } from 'svelte';
    import { user } from '../../stores';
    import { validation } from '$lib/tool.svelte';
    import { menuTable } from '../../stores';
    import { onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
    import { getNowTime } from '$lib/tool.svelte';

    let role = '';
    $: role = user.role;
  
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

    let tables= [];
    let tablesNumber=[];

    let newOrder={        
        "table": "string",
        "time": "string",
        "id": "string",
        "dish": {}
    };

    let ingredients = [
        { name: '', weight: 0 }
    ];
    let totalPrice = 0;
    let quantities = {};

    let showAddMenu = false;
    let showInputTableNumber = true;

    let menuTableNumber='';
    const unsubscribe = menuTable.subscribe((value) => (menuTableNumber=value));
    console.log(menuTableNumber);
    onDestroy(unsubscribe);
  
    onMount(async () => {
        await validation();
        await fetchMenus();
        await fetchTableNmbuer();
        role = user.role;
        calculateTotalPrice(); // 在这里调用 calculateTotalPrice
    });

    async function fetchMenus() {
      try {
          const response = await fetch('http://localhost:8000/menu/all', {
              method: 'GET',
              credentials: 'include',
          });
          if (response.ok) {
              menus = await response.json();
          } else {
              console.error('Error fetching menus:', response.status);
              menus = []; // 设置 menus 为空数组
          }
      } catch (error) {
          console.error('Error fetching menus:', error);
          menus = []; // 设置 menus 为空数组
      }
    }

    async function fetchTableNmbuer(){
    try {
          const response = await fetch('http://localhost:8000/table/all', {
              method: 'GET',
              credentials: 'include',
          });
          if (response.ok) {
              tables = await response.json();              
              for(var i in tables){
                tablesNumber.push(tables[i].id);
              }
            //   console.log(tablesNumber);
          } else {
              console.error('Error fetching table:', response.status);
              tables = []; // 设置 menus 为空数组
          }
      } catch (error) {
          console.error('Error fetching table:', error);
          tables = []; // 设置 menus 为空数组
      }
    }

    function submitTableNumber(){
        if(tablesNumber.includes(menuTableNumber)){
            showInputTableNumber=false;
        }
        else{
            alert("please check it is table number?");
        }
    }
  
    async function submitOrder(){
        const response = await fetch('http://localhost:8000/table/order/'+menuTableNumber,{
          method: 'put',
          headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // This is important for cookies to be sent
            body: JSON.stringify(newOrder)
      });
      if (response.ok) {
        goto("./dining");
      } 
      else {
          console.error('Error fetching updateTable:', response.status);
      }
    }

    async function createOrder(){
        newOrder.id='1';
        newOrder.table=menuTableNumber.toString();
        newOrder.dish= {};           
        newOrder.time = getNowTime();

        // 遍历 currentOrder 对象，将菜品信息添加到 newOrder.dish 对象中
        for (const [menuId, orderItem] of Object.entries(currentOrder)) {
            if (orderItem.quantity > 0) {
                newOrder.dish[orderItem.menu.name] = {
                    amount: orderItem.quantity,
                    description: orderItem.menu.desc,
                    served:false
                };
            }
        }
        
        await submitOrder();
    }


    function createTextBox() {
      var textBox = document.createElement('input');
      textBox.setAttribute('type', 'text');
      textBox.setAttribute('placeholder', 'Ingredient Name');
      textBox.setAttribute('class', 'ingredient-name');
      textBox.setAttribute('required', true);

      var weightBox = document.createElement('input');
      weightBox.setAttribute('type', 'number');
      weightBox.setAttribute('placeholder', 'Ingredient Weight');
      weightBox.setAttribute('class', 'ingredient-weight');
      weightBox.setAttribute('min', '0');
      weightBox.setAttribute('required', true);

      var container = document.createElement('div');
      container.setAttribute('class', 'ingredient-container');
      container.appendChild(textBox);
      container.appendChild(weightBox);
      container.appendChild(document.createElement('button')).textContent = 'x';

      document.body.appendChild(container);
    }
  
    function addIngredient() {
        ingredients = [...ingredients, { name: '', weight: 0 }];
        // createTextBox();
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
        newMenu.ingredient = ingredients;


        if (isEditMode) {
            // 编辑操作
            await updateMenu(newMenu);
        } else {
            newMenu.id = document.getElementById('menuId').value;
            // 新建操作
            const response = await fetch('http://localhost:8000/menu/' + newMenu.id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newMenu),
                credentials: 'include'
            });
            const createdMenu = await response.json();
        }

        await fetchMenus();
        showAddMenu = false;
        isEditMode = false; // 重置为 false
        // 重新启用 id 输入框
        lock = false;
        defaultMenu();
    }

async function updateMenu(menu) {
    const response = await fetch('http://localhost:8000/menu/' + menu.id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(menu),
        credentials: 'include'
    });
    const updatedMenu = await response.json();
    // 在这里更新 menus 数组中对应的菜品信息
    const index = menus.findIndex(m => m.id === menu.id);
    menus[index] = updatedMenu;
    menus = menus;
}
    let currentOrder = {};

    // function updateQuantity(menuId, operation) {
    //     if (operation === 'increment') {
    //         quantities[menuId] = (quantities[menuId] || 0) + 1;
    //         currentOrder[menuId] = (currentOrder[menuId] || 0) + 1;
    //     } else {
    //         quantities[menuId] = Math.max(0, (quantities[menuId] || 0) - 1);
    //         currentOrder[menuId] = Math.max(0, (currentOrder[menuId] || 0) - 1);
    //     }
    //     calculateTotalPrice();
    // }
    function updateQuantity(menu, operation) {
        if (operation === 'increment') {
            quantities[menu.id] = (quantities[menu.id] || 0) + 1;
            currentOrder[menu.id] = (currentOrder[menu.id] || { menu, quantity: 0 });
            currentOrder[menu.id].quantity += 1;
        } else {
            quantities[menu.id] = Math.max(0, (quantities[menu.id] || 0) - 1);
            currentOrder[menu.id] = (currentOrder[menu.id] || { menu, quantity: 0 });
            currentOrder[menu.id].quantity = Math.max(0, currentOrder[menu.id].quantity - 1);
        }
        calculateTotalPrice();
    }
  
    function calculateTotalPrice() {
        totalPrice = Object.values(currentOrder).reduce((acc, orderItem) => {
            return acc + (orderItem.menu.price * orderItem.quantity);
        }, 0);
    }
    var lock = false;
    // function getImage(file){
    //   const reader = new FileReader();
    //   reader.readAsDataURL(file);
    //   reader.onload = e => {
    //       newMenu.image= e.target.result;
    //       lock = true;
    //       newMenu.image = newMenu.image.split(',')[1];
    //       // newMenu.image = "123";
    //   };
    // }
    function getImage(file) {
    // 检查文件类型是否为 JPEG 或 PNG
        if (!['image/jpeg', 'image/png'].includes(file.type)) {
            alert('Please upload a JPEG or PNG image file.');
            return;
        }

        // 创建一个 Image 对象并设置 src 属性
        const img = new Image();
        img.src = URL.createObjectURL(file);

        // 等待图片加载完成
        img.onload = () => {
            // 检查图片尺寸是否符合要求
            if (img.width > 320 || img.height > 200) {
                // 调整图片尺寸
                const canvas = document.createElement('canvas');
                canvas.width = 320;
                canvas.height = 200;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, 320, 200);

                // 将调整后的图片转换为 base64 字符串
                canvas.toBlob((blob) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(blob);
                    reader.onload = () => {
                        newMenu.image = reader.result.split(',')[1];
                        lock = true;
                    };
                }, file.type);
            } else {
                // 直接将原图片转换为 base64 字符串
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => {
                    newMenu.image = reader.result.split(',')[1];
                    lock = true;
                };
            }
        };
    }

    let isEditMode = false;
    async function handleEdit(menu) {
        newMenu = { ...menu };
        console.log(newMenu.id);
        showAddMenu = true;
        isEditMode = true;
    }

    function assignValue(){
        document.getElementById('menuId').value = newMenu.id;
        document.getElementById('menuName').value = newMenu.name;
        document.getElementById('menuPrice').value = newMenu.price;
        document.getElementById('menuWeight').value = newMenu.weight;
        document.getElementById('menuAvail').checked = newMenu.availability;
        document.getElementById('menuDes').value = newMenu.desc;
        document.getElementById('menuSold').value = newMenu.sold;
        ingredients = newMenu.ingredient;
    }

    async function handleDelete(id) {
        const response = await fetch(`http://localhost:8000/menu/${id}`, {
            method: 'DELETE',
            credentials: 'include',
        });
        if (response.ok) {
            await fetchMenus();
        } else {
            console.error('Error deleting menu:', response.status);
        }
    }

    function loaded(node) {
        assignValue();
        return {
            destroy() {
                // cleanup logic, if any
            }
        };
    }

    function defaultMenu(){
        newMenu = {
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
    }

    function cancelModal(){
        showAddMenu = false;
        isEditMode = false;
        defaultMenu();
    }
  </script>
  
  {#if showInputTableNumber}
    <div class="modal">
        <div class="modal-content" on:click|stopPropagation>
            <label>
                Please input table number
                <input type="text" id="menuTableNumber" bind:value={menuTableNumber} required>
            </label>
            <button on:click={() => submitTableNumber()} >submit</button>
        </div>
    </div>
  {/if}
  
  {#if !showInputTableNumber}
  <h1>Menu Table {menuTableNumber}</h1>
  {/if}
  
  {#if role === 'Manager' || role === 'Kitchen Staff'}
  <div>
      <button on:click={() => showAddMenu = true}>Add New Dish</button>
      {#if showAddMenu}
      <div class="add-menu-container">
          <div class="add-menu-form" use:loaded={assignValue()}>
              <h2>Add New Dish</h2>
              <form on:submit|preventDefault={saveMenu}>
                  <label>
                        ID:
                        <input type="text" id="menuId" disabled={isEditMode} required>
                        {#if isEditMode}
                        <span class="readonly-label">(unchangeable)</span>
                        {/if}
                    </label>
                  <label>
                      Name:
                      <input type="text" id="menuName" required>
                  </label>
                  <label>
                      Price:
                      <input type="number" step="1" id="menuPrice" value="{newMenu.id || ''}" min="0" required>
                  </label>
                  <label>
                      Weight:
                      <input type="number" step="1" id="menuWeight" value="{newMenu.name || ''}" min="0" required>
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
                      <input type="file" on:change={(e) => getImage(e.target.files[0])} required>
                  </label>
                  <button type="submit" on:click={() => fetchMenus}>Save</button>
                  <button type="button" on:click={() => cancelModal()}>Cancel</button>
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
          <!-- <div class="quantity-container">
              <button on:click={() => updateQuantity(menu.id, 'decrement')}>-</button>
              <span>{quantities[menu.id] || 0}</span>
              <button on:click={() => updateQuantity(menu.id, 'increment')}>+</button>
          </div> -->
          <div class="quantity-container">
            <button on:click={() => updateQuantity(menu, 'decrement')}>-</button>
            <span>{quantities[menu.id] || 0}</span>
            <button on:click={() => updateQuantity(menu, 'increment')}>+</button>
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
              <button on:click={() => handleEdit(menu)}>Edit</button>
              <button on:click={() => handleDelete(menu.id)}>Delete</button>
          </div>
          {/if}
      </div>
      {/each}
  </div>
  
    {#if role !== 'Manager' && role !== 'Kitchen Staff'}
    <div class="total-price-container">
        <p>My Order:</p>
        {#each Object.values(currentOrder) as orderItem}
        {#if orderItem.quantity > 0}
        <div class="order-item">
            <p>{orderItem.menu.name} x {orderItem.quantity}</p>
            <div class="quantity-controls">
                <button on:click={() => updateQuantity(orderItem.menu, 'decrement')}>-</button>
                <button on:click={() => updateQuantity(orderItem.menu, 'increment')}>+</button>
            </div>
        </div>
        {/if}
        {/each}
        <div class="total-price">Total Price: ${totalPrice.toFixed(2)}</div>
    </div>
    {/if}

    {#if role === 'Dining Room Staff'}
    <button on:click={() => createOrder()}>Submit Order</button>
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
          overflow: hidden; 
      }

      .menu-item img {
        width: 100%; /* 添加这行 */
        height: 200px; /* 添加这行 */
        object-fit: cover; /* 添加这行 */
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
        position: sticky;
        bottom: 0;
        left: 0;
        width: 99.5%;
        background-color: #f5f5f5;
        padding: 10px;
        text-align: left;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        max-width: 100%;
        overflow-x: auto;
        display: inline-block;
    }

    .total-price-container p {
        margin: 5px 0;
    }

    .order-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .quantity-controls {
        display: flex;
        gap: 5px;
    }

    .quantity-controls button {
        background-color: #e0e0e0;
        border: none;
        padding: 5px 10px;
        cursor: pointer;
    }

    .total-price {
        text-align: right;
        font-weight: bold;
        margin-top: 10px;
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

    .readonly-label {
        color: #999;
        font-size: 0.8rem;
        margin-left: 5px;
    }

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
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        max-width: 600px;
        width: 100%;
    }
  </style>