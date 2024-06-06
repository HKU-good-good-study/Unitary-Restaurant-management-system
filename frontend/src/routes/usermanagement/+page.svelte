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
  let showAddUserDialog = false;
  let showUpdateDialog=false;
  let newUser={name:"",role:"",status:true,password:"",email:"",countryCode:"",phoneNumber:""};

  
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
    history.replaceState(null, '', '/profile');

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
    paginate(users);
  }
  
   // 添加用户
  function addUser(){
    newUser.password=newUser.phoneNumber;
    users.push(newUser);
    paginate(users);
    showAddUserDialog=false;
    console.log(newUser);
  }

  function addUserBotton() {   
    showAddUserDialog=true;
    newUser={name:"",role:"",status:true,password:"",email:"",countryCode:"",phoneNumber:""};  
  }

  /*async function submitRegistrationForm() {
        const userData = {
            username: username,
            password: password,
            email: email,
            phone_number: countryCode + " " + phoneNumber,
            role: role,
            remarks: remarks
        };

        const response = await fetch('http://localhost:8000/auth/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        const data = await response.json();
        console.log(data);
    }*/

  

  function updateBotton() {   
    showUpdateDialog=true;  
  }
  function update(index) {
    // 修改用户角色权限
    users[index].role = userRole;
    paginate(users);    
    showAddUserDialog=false;
    console.log(newUser);
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
    position:absolute; 
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
    position: fixed;
    top:80%;
    left: 53%;
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

<div>

  <img width=10% {src} alt="{name}">
  <button class=addUser on:click={() =>addUserBotton()}>
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
                  on:click={() =>changeStatus(index+page*itemsPerPage)}>
                  deactivate 
                  </button>
                  {/if}
                  {#if !currentPageRow.status}
                  <button class = activeButton 
                  on:click={() =>changeStatus(index+page*itemsPerPage)}>
                  activate
                  </button>
                  {/if}
                  <button class = updateButton 
                  on:click={() =>updateBotton(index+page*itemsPerPage,1)}>
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

  <!-- addUserDialog-->
  {#if showAddUserDialog}
  <div class="modal" on:click={() => showAddUserDialog = false}>
    <div class="modal-content" on:click|stopPropagation>
      <h3>please input new user information</h3>
      <div class="row">
        <label for="userRole">role:</label>
        <select id="userRole"bind:value={newUser.role}>
          <option value="customer">customer</option>
          <option value="management">management</option>
          <option value="dinning">dinning</option>          
          <option value="kitchen">kitchen</option>
        </select>
      </div>
      <div class="row">
        <label for="userName">name:</label>
        <input id="userName" bind:value={newUser.name} placeholder="Enter new user name" />
      </div> 
      <div class="row">
        <label for="countryCode">country code:</label>
        <select id="countryCode" bind:value={newUser.countryCode}>
            <option value="+1">USA (+1)</option>
            <option value="+1">CANADA (+1)</option>
            <option value="+44">Britain (+44)</option>
            <option value="+86">China (+86)</option>
            <option value="+91">India (+91)</option>
            <option value="+852">HongKong SAR (+852)</option>
            <option value="+52">Mexico (+52)</option>
            <!-- Add more options as needed -->
        </select>
      </div>
      <div class="row">
        <label for="phoneNumber">phone number:</label>
        <input id="phoneNumber" bind:value={newUser.phoneNumber} placeholder="Enter Phone Number">
      </div>
      <div class="row">
        <label for="email">email:</label>
        <input id="email" bind:value={newUser.email} placeholder="Enter Email">
      </div>
      <button on:click={addUser}>Submit</button>
      <button on:click={() => showAddUserDialog = false}>CLOSE</button>     
    </div>    
  </div>
  {/if}

</div>