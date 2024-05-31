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
    { name: 'liu', role: 'customer', status:false, count:0},
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
    currentPageRows[index].status = !currentPageRows[index].status;
  }

  function addUser(userName,userRole) {
    // 添加用户
    currentPageRows.push({name: userName, role: userRole, status: 0});
  }

  function updateRole(index,userRole) {
    // 修改用户角色权限
    currentPageRows[index].role = userRole;
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
    border:none;
    border-radius: 8%;
  }

  .updateButton{
    background-color: #D3D3D3;
    border-color: #D3D3D3;
    color:#00BFFF;
    height: 2rem;
    width: auto;
    font-size: 1rem;
    background-image: linear-gradient(45deg, #00BFFF 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .updateButton:hover{
    color: black;  border: 0;
    background-color: #00BFFF;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(0,191,255);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(0,191,255);
    box-shadow: 10px 10px 99px 6px rgba(0,191,255);
  }

  .activeButton{
    background-color: #aaa;
    border-color: #aaa;
    color:#b9e769;
    height: 2rem;
    width: 6rem;
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
    width: 6rem;    
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

  .addUser{
    position:fixed; 
    right: 10%; 
    top:10%; 
    display: inline-block; 
    width:auto ;
    height: 5%;     
    font-size:1rem;
    background-color: #FFFF00;
    border-color: #FFFF00;
    color:#000000;
    background-image: linear-gradient(45deg, #FFFF00 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .addUser:hover{
    color: black;  border: 0;
    background-color: #FFD700;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(255,215,0);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(255,215,0);
    box-shadow: 10px 10px 99px 6px rgba(255,215,0);
  }

  .btn-page-number{
    margin:5px;
  }

  .btn-next-prev{
    margin:5px;
  }
  table{
    position: absolute;
    top: 10%;
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
    position: absolute;
    top:80%;
    left: 53%;
  }

</style>

<div>

  <img width=10% {src} alt="{name}">
  <button class=addUser on:click={() =>addUser()}>
  addUser
  </button>

  <div>
    <table >
      <thead>
          <tr>
            <th>name</th>
            <th>role</th>
            <th>status</th>
            <th>operation</th>
          </tr>
        </thead>
        
        <tbody>
            {#each currentPageRows as currentPageRow, index}
              <tr>
                <td width=10%>{currentPageRow.name}</td>
                <td width=10%>{currentPageRow.role}</td>
                {#if currentPageRow.status}
                <td class = activeStatus width=10%>
                active 
                </td>
                {/if}
                {#if !currentPageRow.status}
                <td class= deactiveStatus width=10%>
                deactive 
                </td>
                {/if}
                
                <td width=20%>                
                  {#if currentPageRow.status}
                  <button class = deactiveButton 
                  on:click={() =>changeStatus(index)}>
                  deactivate
                  </button>
                  {/if}
                  {#if !currentPageRow.status}
                  <button class = activeButton 
                  on:click={() =>changeStatus(index)}>
                  activate
                  </button>
                  {/if}
                  <button class = updateButton 
                  on:click={() =>updateRole(index,1)}>
                  update
                  </button>
                </td>
              </tr>
            {/each}
        </tbody>

    </table>
  </div>


  <!--翻页栏-->
  <div>
    <nav class="pagination">
      <ul>
        <li>
        page {page + 1}/{totalPages.length}
        </li>
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


</div>