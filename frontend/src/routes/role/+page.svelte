<script>
  import { goto } from '$app/navigation';
  import { user } from '../../stores';
  import { onMount } from 'svelte';
  import { validation } from '$lib/tool.svelte';
  import { menuTable } from '../../stores';

  // let roleData=sessionStorage.getItem("role");
  //let role = roleData; // Change this to 'kitchen', 'manager', 'customer', or 'dining' based on the current user
  // role='Kitchen';
  //role='Dining';
  //role='Customer';
  let role="";
  role=user.role;

  var rolePermissions={};
  rolePermissions["Manager"]=["dining","kitchen","menu","usermanagement","profile"];  
  rolePermissions["Kitchen Staff"]=["kitchen","menu","profile"];
  rolePermissions["Dining Room Staff"]=["dining","menu","profile"];
  rolePermissions["Customer"]=["customer","menu","profile"];  
  rolePermissions[" "]=["menu"];

  function goToFunction(feature) {
    var url='./'+feature;
    if(feature=='menu'){
      menuTable.set('');
    }
    goto(url);
  }

  onMount(async () => {
      // history.replaceState(null, 'Profile', '/profile');
      document.title = 'Role Page';
      await validation();
      role=user.role;
      user.username=user.username;
  });

</script>

<style>
  .menu {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 40px;
    padding: 40px;
    background-color: #f8f8f8;
  }

  .function {
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

  .function h2 {
    color: #333;
    margin-bottom: 10px;
  }

  .function p {
    color: #666;
    margin-bottom: 10px;
  }

  .function img {
    width: 150px; /* Set the width of each product */
    height: auto; /* Automatically adjust height to maintain image proportions */
    object-fit: cover; /* Set the image fill method */
    margin-bottom: 8px;
    margin-top: 10px;
  }

  body{
	    margin: 0px;
  }
     
</style>

{#if user.username!='customer'}
<body>
  <div class="menu">
    {#each rolePermissions[role] as permission }
      <div class=function on:click={() => goToFunction(permission)}>
        <img src="./src/images/{permission}.png">
        <h2>{permission}</h2>
      </div>    
    {/each}  
  </div>
</body>
{/if}

{#if user.username=='customer'}
<div class="menu">
  <div class=function on:click={() => goToFunction('menu')}>
    <img src="./src/images/menu.png">
    <h2>menu</h2>
  </div>  
</div>  
{/if}