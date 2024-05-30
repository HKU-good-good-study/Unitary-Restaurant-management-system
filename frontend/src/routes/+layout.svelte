<script>
    import HeaderBar from '$lib/HeaderBar.svelte';

    let user={name:"zhou", role: "manager", imgSrc:"./src/images/"};
    let png=".png";
    user.imgSrc=user.imgSrc+user.role+png;


</script>

{#if user.name}
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
    <span >{user.name}</span>
    <span style:padding-left=5% ><img width=10% src={user.imgSrc}></span>
    </svelte:fragment>
</HeaderBar>
</div>
{/if}
<slot></slot>
