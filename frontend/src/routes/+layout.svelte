<script>
    import HeaderBar from '$lib/HeaderBar.svelte';
    import { onMount } from 'svelte';
    import { user } from '../stores.js'; 
    import { page } from '$app/stores';
    import { validation } from '$lib/tool.svelte';

    onMount(async () => {
      // history.replaceState(null, 'Profile', '/profile');
      document.title = 'Role Page';
      await validation();
      user.name= user.name;
  });

    //$: user.name= user.name;

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
