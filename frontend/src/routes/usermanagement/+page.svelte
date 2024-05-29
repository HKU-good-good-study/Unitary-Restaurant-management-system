<script>
  import { onMount } from "svelte";

  let src = './src/images/0.png';
	let name = 'icon';

  let users = [];
  let page = 0;
  let totalPages = [];
  let currentPageRows = [];
  let itemsPerPage = 13;
  let loading = true;
  
  $: currentPageRows = totalPages.length > 0 ? totalPages[page] : [];
  $: console.log("Page is", page);

  const paginate = (items) => {
    const pages = Math.ceil(items.length / itemsPerPage);

    const paginatedItems = Array.from({ length: pages }, (_, index) => {
      const start = index * itemsPerPage;
      return items.slice(start, start + itemsPerPage);
    });

    console.log("paginatedItems are", paginatedItems);
    totalPages = [...paginatedItems];
  };

  onMount(() => {
    users =[
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
        { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
        { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    { name: 'liu', role: 'customer', status:false},
    { name: 'zhou', role: 'customer', status: true},
    
    
    // more user...
  ];
    paginate(users);
  });
  
  const setPage = (p) => {
    if (p >= 0 && p < totalPages.length) {
      page = p;
    }
  }

  function changeStatus(index) {
    // 更改用户账户状态
    // 用户账户状态 false停用/true 启用
    users[index].status = !users[index].status;
  }

  function addUser(userName,userRole) {
    // 添加用户
    users.push({name: userName, role: userRole, status: 0});
  }

  function updateRole(index,userRole) {
    // 修改用户角色权限
    users[index].role = userRole;
  }  
</script>

<style>
  nav > ul {
    list-style-type: none;
    display: flex;
  }

    .activeStatus{
    color: green;
  }

  .deactiveStatus{
    color: #8B8B7A;
  }
  
/*  .activeButton{
    background-color: #aaa;
    border-color: #c4f07a;
    color:b9e769
    height: 2rem;
    width: 3rem;
    background-image: linear-gradient(45deg, #c4f07a 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }
    .activeButton:hover {
    background-position: 0;
    color: #aaa;
    
  }*/

  button{
    margin-left: 5%;
  }

  .updateButton{
    height: 2rem;
    width: auto;
    font-size: 1rem;
  }

  .activeButton{
    background-color: #aaa;
    border-color: #aaa;
    color:#b9e769;
    height: 2rem;
    width: 3rem;
    font-size: 1rem;
    background-image: linear-gradient(45deg, #b9e769 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .activeButton:hover{
    color: black;  border: 0;
    background-color: #b9e769;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(185, 231, 105, 1);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(185, 231, 105, 1);
    box-shadow: 10px 10px 99px 6px rgba(185, 231, 105, 1);
  }
  

.deactiveButton{  
    background-color: #aaa;
    border-color: #aaa;
    color:#B22222;
    height: 2rem;
    width: 3rem;    
    font-size: 1rem;
    background-image: linear-gradient(45deg, #aaa 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .deactiveButton:hover{
    color: white;  border: 0;
    background-color: #B22222;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);
    box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);
  }


  table{
    position: fixed;
    top: 20%;
    left: 20%;
    width: 50%;
    align:"right";
    line-height: 2.5;
  }

  tr{    
  }

  td{
    text-align:center;
  }

  .pagination{
    position: fixed;
    top:85%;
    left: 53%;
  }

</style>

<div>
  <body bgcolor="#FFE4C4">

  <img {src} alt="{name}">

  <table >
    <thead>
        <tr>
          <th>姓名</th>
          <th>角色</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
          {#each currentPageRows as { name, role ,status}, index}
            <tr>
              <td width=10%>{name}</td>
              <td width=10%>{role}</td>
              {#if status}
              <td class = activeStatus width=10%>
              启用中
              </td>
              {/if}
              {#if !status}
              <td class= deactiveStatus width=10%>
              停用中
              </td>
              {/if}
              
              <td width=20%>
                {#if status}
                <!--button on:click={() =>changeStatus(index)}>
                {status ?  '停用' : '启用'}
                </button-->
                <button class = deactiveButton 
                on:click={() =>changeStatus(index)}>
                停用
                </button>
                {/if}
                {#if !status}
                <button class = activeButton 
                on:click={() =>changeStatus(index)}>
                启用
                </button>
                {/if}
                <button class = updateButton 
                on:click={() =>updateRole(index,)}>
                更新
                </button>
              </td>
            </tr>
          {/each}
      </tbody>
  </table>
  <!--导航栏-->
  <nav class="pagination">
    <ul>
      <li>
        <button
          type="button"
          class="btn-next-prev"
          on:click={() => setPage(page - 1)}>
          PREV
        </button>
      </li>

      {#each totalPages as page, i}
        <li>
          <button
            type="button"
            class="btn-page-number"
            on:click={() => setPage(i)}>
            {i + 1}
          </button>
        </li>
      {/each}

      <li>
        <button
          type="button"
          class="btn-next-prev"
          on:click={() => setPage(page + 1)}>
          NEXT
        </button>
      </li>
    </ul>
  </nav>
</div>