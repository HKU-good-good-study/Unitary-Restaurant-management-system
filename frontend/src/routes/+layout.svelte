<script>
    import HeaderBar from '$lib/HeaderBar.svelte';
    import { onMount } from 'svelte';
    import { user } from '../stores.js'; 
    import { page } from '$app/stores';

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

    $: user.name= user.name;

</script>

{#if user.name && $page.url.pathname != '/login'}
<div>
<HeaderBar back="true" bgcolor="linear-gradient(to right, #4978ff, #17f532)" color="#e4ff00">
    <svelte:fragment slot="backText">
        <i class="iconfont icon-close">Back</i>        
    </svelte:fragment>

    <!--svelte:fragment slot="search">
        < div class="flex-c flex1">
            <input class="ipt flex1" placeholder="Search..." value="" />
        </div >
    </svelte:fragment-->

   <svelte:fragment slot="user">
    <i >{user.name}</i>
    <i style:padding-left=5%><img width=10% src={user.imgSrc} alt="role"></i>
    </svelte:fragment>
    
    <svelte:fragment slot="logout">
    <i >logout</i>
    </svelte:fragment>
</HeaderBar>
</div>
{/if}
<slot></slot>
