<script>
    import HeaderBar from '$lib/HeaderBar.svelte';
    import { user } from '../stores.js'; 
    import { page } from '$app/stores';
    import { validation } from '$lib/tool.svelte';
    import { onMount  } from 'svelte';
    
    onMount(async () => {
      // history.replaceState(null, 'Profile', '/profile');
      document.title = 'Role Page';
      if($page.url.pathname == '/login' || $page.url.pathname == '/register'){}
      else {
        await validation();
      }
      user.username=user.username;     
    });


     $: user.username=user.username;
    //  $: console.log("lay"+user.username);
</script>

<style>
    body{
	    margin: 0px;
    }
    
    img{
        position: relative;
        padding-left: 5%;
        margin-bottom: -5%;
        width: 30px;
    }

    
</style>

{#if user.username && $page.url.pathname != '/login'}
<!-- <body> -->
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
    <i >{user.username}</i>
    <img src={user.imgSrc} alt="role">
    </svelte:fragment>
    
    <svelte:fragment slot="logout">
    <i >logout</i>
    </svelte:fragment>
</HeaderBar>
<!-- </body> -->
{/if}
<slot></slot>
