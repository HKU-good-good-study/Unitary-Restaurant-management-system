<!-- //自定义HeaderBar组件 -->
<script>
    import { goto } from '$app/navigation';

    // 是否显示回退按钮
    export let back = true
    // 标题
    export let title = ''
    // 颜色
    export let color = '#fff'
    // 背景色
    export let bgcolor = '#22d59c'
    // 是否居中标题
    export let center = false
    // 是否固定
    export let fixed = true
    // 是否镂空透明
    export let transparent = false
    // 层级
    export let zIndex = 2021

    // function goBack() {
    //     console.log('go back')
    //     history.go(-1)
    //     // history.back(-1)
    // }

    function goBack(){
        goto('/role')
    }

    function gotoRole(){
        goto('/role')
    }

    async function logOut(){
        const response = await fetch ('http://localhost:8000/auth/users/tokens',{
            method: 'DELETE',
            credentials: 'include', // This is important for cookies to be sent
        });
        if (response.ok) {
            goto('/login')
          } else {
              console.error('Error fetching login:', response.status);
          }
        
    }

</script>

<style>
    .user{
        position:relative;
        padding: 10px;
        left:73%;
        display: inline-block;
        color: black; 
        width: 8%;
    }
    
    .link{
        margin-left:5%;
        display: inline-block;
    }

    .logout{
        position:relative;
        padding: 10px;
        left: 80%;
        display: inline-block;
        color: black; 
    }

    .header-bar{        
        padding:0px;
        margin:0px;
        border:0px;
    }
    
    .back{
        position:relative;
        display: inline-block;
        padding: 10px;
    }
</style>

<div class="header-bar" class:transparent class:fixed={transparent||fixed}>
    <div style:color style:background={bgcolor} style:z-index={zIndex}>
        <!-- //返回 -->
        {#if back && back != 'false'}
            <div class="back" on:click={goBack}>
                <slot name="backIco" /><slot name="backText" />
            </div>
        {/if}

        <!-- //用户姓名及标识 -->
        <div class= user on:click={gotoRole}>
            <slot name="user" />
        </div>

        <div class= logout on:click={logOut}>
            <slot name="logout"/>
        </div>  

        <!-- //标题 -->
        <div class="hdbar-title" class:center>
            {#if $$slots.title}
                <slot name="title" />
            {:else}
                {@html title}
            {/if}
        </div>

        <!-- //搜索框 -->
        <div class="action hdbar-action__search">
            <slot name="search" />
        </div>

        
    </div>
</div>