<script>
  import { goto } from '$app/navigation';
  import { user } from '../../stores';
  import { onMount } from 'svelte';

  // let roleData=sessionStorage.getItem("role");
  //let role = roleData; // Change this to 'kitchen', 'manager', 'customer', or 'dining' based on the current user
  // role='Kitchen';
  //role='Dining';
  //role='Customer';
  let role="";
  $: role=user.role;

  var rolePermissions={};
  rolePermissions["Manager"]=["dining","kitchen","menu","usermanagement"];  
  rolePermissions["Kitchen Staff"]=["kitchen","menu"];
  rolePermissions["Dining Room Staff"]=["dining","menu"];
  rolePermissions["Customer"]=["customer","menu"];  
  rolePermissions[" "]=["menu"];

  function goToFunction(feature) {
    var url='./'+feature;
    goto(url);
  }

  onMount(async () => {
      // history.replaceState(null, 'Profile', '/profile');
      document.title = 'Role Page';
      const roleResponse = await fetch('http://localhost:8000/auth/users/me', {
              method: 'GET',
              credentials: 'include', // This is important for cookies to be sent
      });
      const roleData = await roleResponse.json();
      console.log(roleData);
      user.name=roleData.username;
      user.role=roleData.role;
      user.imgSrc="./src/images/";
      user.imgSrc=user.imgSrc+user.role.split(" ")[0].toLowerCase()+'.png';
      user.email=roleData.email;
      user.phone_number=roleData.phone_number;
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
    margin-bottom: 10px;
  }
</style>


<div class="menu">
  {#each rolePermissions[role] as permission }
    <div class=function on:click={() => goToFunction(permission)}>
      <img src="./src/images/{permission}.png">
      <h2>{permission}</h2>
    </div>    
  {/each}  
</div>