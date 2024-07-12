<script>
  import { onMount } from "svelte";  
  import { user } from '../../stores';
  import { validation } from "$lib/tool.svelte";

  let src = './src/images/0.png';
	let name = 'icon';
  let role ='';
  $: role=user.role;


  let page = 0;
  let totalPages = [];
  let currentPageRows = [];
  let itemsPerPage = 13;
  let loading = true;

  let showAddUserDialog = false;
  let showUpdateDialog=false;
  let showDeleteModal=false;
  let showResetModal=false;

  let users = [{username:"",role:"",status:true,password:"",email:"",countryCode:"",phone_number:"",remarks:""}];
  let newUser={username:"",role:"",status:true,password:"",email:"",countryCode:"",phoneNumber:"",remarks:""};
  let selectUser={username:"",role:"",status:true,index:-1,email:"",countryCode:"",phoneNumber:"",remarks:""};
  var userData={};
  let originUser={username:"",role:"",status:true,index:-1,email:"",countryCode:"",phoneNumber:"",remarks:""};

  
  $: currentPageRows = totalPages.length > 0 ? totalPages[page] : [];
  //$: console.log("Page is", page);
  //$: console.log(user);
  const paginate = (items) => {
    const pages = Math.ceil(items.length / itemsPerPage);

    const paginatedItems = Array.from({ length: pages }, (_, index) => {
      const start = index * itemsPerPage;
      return items.slice(start, start + itemsPerPage);
    });

    //console.log("paginatedItems are", paginatedItems);
    totalPages = [...paginatedItems];
  };


  onMount(async () => {
    await validation();  
    role=user.role;    
    document.title = 'User Management';
    await fetchUsers();
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
  
   // 添加用户 用户默认密码位手机号码

  async function submitAddUser(){
      const userData = {
          username: newUser.username,
          password: newUser.password,
          email: newUser.email,
          phone_number: newUser.countryCode + " " + newUser.phoneNumber,
          role: newUser.role,
          remarks: newUser.remarks
      };

      const response = await fetch('http://localhost:8000/auth/users/new', {
          method: 'POST',
          credentials: 'include',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData)
      });
      await fetchUsers();
      //const data = await response.json();
      //console.log(data);
  }

  async function addUser(){
    newUser.password='!Qw123456';
    //users.push(newUser);
    await submitAddUser();
    users = users;
    paginate(users);
    showAddUserDialog=false;
    console.log(newUser);
  }

  function addUserBotton() {   
    showAddUserDialog=true;
    newUser={username:"",role:"",status:true,password:"",email:"",countryCode:"",phoneNumber:""};  
  }
 

  function updateBotton(index) {  
    selectUser.username= users[index].username;
    selectUser.role= users[index].role;
    selectUser.status= users[index].status;
    selectUser.email= users[index].email;
    selectUser.countryCode= users[index].countryCode;
    selectUser.phoneNumber= users[index].phone_number;
    selectUser.index=index;    
    originUser.username=selectUser.username;
    originUser.role=selectUser.role;
    originUser.status=selectUser.status;
    originUser.email=selectUser.email;
    originUser.countryCode=selectUser.countryCode;
    originUser.phoneNumber=selectUser.phoneNumber;
    showUpdateDialog=true;
  }

  async function update() {
    let number = selectUser.index;
    await submitUpdate(users[number].username);
    users=users;
    paginate(users);    
    showUpdateDialog=false;
  }

  async function submitUpdate(username){
      if(selectUser.username!=originUser.username){
        userData.username=selectUser.username;
      }
      
      if(selectUser.email!=originUser.email){
        userData.email=selectUser.email;
      }

      if(selectUser.role!=originUser.role){
        userData.role=selectUser.role;
      }

      if(selectUser.countryCode!=originUser.countryCode || selectUser.phoneNumber!=originUser.phoneNumber){
        userData.phone_number=selectUser.countryCode + " " + selectUser.phoneNumber;
      }   

      const response = await fetch('http://localhost:8000/auth/users/username='+ username, {
          method: 'PATCH',
          credentials: 'include',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(userData)
      });
      await fetchUsers();
      const data = await response.json();
      console.log(data);
  }
  
  async function fetchUsers(){
    try {
          const response = await fetch('http://localhost:8000/auth/users/all', {
              method: 'GET',
              credentials: 'include',
          });
          if (response.ok) {
              users = await response.json();
              var x;
              for(x in users){
                users[x].phone_number=users[x].phone_number.slice(4);
                users[x].countryCode=users[x].phone_number.split('-')[0];
                users[x].phone_number=users[x].phone_number.split('-')[1]+users[x].phone_number.split('-')[2]+users[x].phone_number.split('-')[3];
              }
              // console.log(users);
          } else {
              console.error('Error fetching users:', response.status);
              users = []; // 设置 users 为空数组
          }
      } catch (error) {
          console.error('Error fetching users:', error);
          users = []; // 设置 users 为空数组
      }
  }

  async function deleteUser(){
    try {
          const response = await fetch('http://localhost:8000/auth/users/username='+selectUser.username, {
              method: 'delete',
              credentials: 'include',
          });
          if (response.ok) {
            await fetchUsers();
            showUpdateDialog = false;
            showDeleteModal = false;
            users=users;
          } else {
              showDeleteModal = false;
              console.error('Error delete user:', response.status);
          }
      } catch (error) {
          showDeleteModal = false;
          console.error('Error fetching user:', error);
      }
  }

  async function resetPassword(){
      const response = await fetch('http://localhost:8000/auth/users/password-reset-token', {
          method: 'POST',
          credentials: 'include',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(selectUser.email)
      });
      const data = await response.json();
      console.log(data);

      // const resetData={
      //   credentials: 'include',
      // };
      // console.log(resetData);
      // const resetResponse = await fetch('http://localhost:8000/auth/users/password-reset',{
      //     method: 'POST',
      //     credentials: 'include',
      //     headers: {
      //         'Content-Type': 'application/json'
      //     },
      //     body: JSON.stringify(resetData)        
      // });
      // const resetData = await resetResponse.json();      
      // console.log(resetData);

      showResetModal=false;
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

  .row {
    margin-bottom: 10px;
  }
  
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

  .deleteButton{  
    background-color: #aaa;
    border-color: #aaa;
    color:#B22222;
    background-image: linear-gradient(45deg, #aaa 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .deleteButton:hover{
    color: white;  border: 0;
    background-color: #B22222;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);
    box-shadow: 10px 10px 99px 6px rgba(178, 34, 34, 1);
  }

  .resetButton{
    background-color: #aaa;
    border-color: #aaa;
    color:#b9e769;
    background-image: linear-gradient(45deg, #b9e769 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .resetButton:hover{
    color: black;  border: 0;
    background-color: #b9e769;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(185, 231, 105, 1);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(185, 231, 105, 1);
    box-shadow: 10px 10px 99px 6px rgba(185, 231, 105, 1);
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
  {#if role=='Manager'}
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
                  <td width=10%>{currentPageRow.username}</td>
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
                    on:click={() =>updateBotton(index+page*itemsPerPage)}>
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
              <option value="Customer">Customer</option>
              <option value="Manager">Manager</option>
              <option value="Dining Room Staff">Dining Room Staff</option>          
              <option value="Kitchen Staff">Kitchen Staff</option>
            </select>
          </div>
          <div class="row">
            <label for="userName">name:</label>
            <input id="userName" bind:value={newUser.username} placeholder={"Enter new user name"} />
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
            <input id="phoneNumber" bind:value={newUser.phoneNumber} type="tel" placeholder="Enter Phone Number">
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


     <!--UpdateDialog-->
    {#if showUpdateDialog}
      <div class="modal" on:click={() => showUpdateDialog = false}>
        <div class="modal-content" on:click|stopPropagation>

          <h3>please update user information</h3>

          <div class="row">
            <label for="userRole">role:</label>
            <select id="userRole"bind:value={selectUser.role}>
              <option value="Customer">Customer</option>
              <option value="Manager">Manager</option>
              <option value="Dining Room Staff">Dining Room Staff</option>          
              <option value="Kitchen Staff">Kitchen Staff</option>
            </select>
          </div>

          <div class="row">
            <label for="userName">name:</label>
            <input id="userName" bind:value={selectUser.username} />
          </div> 

          <div class="row">
            <label for="countryCode">country code:</label>
            <select id="countryCode" bind:value={selectUser.countryCode}>
                <option value="+1">USA (+1)</option>
                <option value="+1">CANADA (+1)</option>
                <option value="+44">Britain (+44)</option>
                <option value="+86">China (+86)</option>
                <option value="+91">India (+91)</option>
                <option value="+852">HongKong SAR (+852)</option>
                <option value="+52">Mexico (+52)</option>
            </select>
          </div>

          <div class="row">
            <label for="phoneNumber">phone number:</label>
            <input id="phoneNumber" bind:value={selectUser.phoneNumber} type="tel">
          </div>

          <div class="row">
            <label for="email">email:</label>
            <input id="email" bind:value={selectUser.email}>
          </div>

          <button on:click={update}>Submit</button>
          <button on:click={() => showUpdateDialog = false}>CLOSE</button>  
          <button class=deleteButton on:click={() => showDeleteModal = true}>DELETE</button>
          <button class=resetButton on:click={()=> showResetModal = true}>RESET PASSWORD</button>

          {#if showDeleteModal}
            <div class="modal" on:click={() => showDeleteModal = false}>
              <div class="modal-content" on:click|stopPropagation>
                <h2>Are you sure deleting it?</h2>
                <button on:click={() => deleteUser()}>DELETE</button>        
                <button on:click={() => showDeleteModal = false}>CLOSE</button> 
              </div>
            </div>
          {/if}     

          {#if showResetModal}
            <div class="modal" on:click={() => showResetModal = false}>
              <div class="modal-content" on:click|stopPropagation>
                <h2>Are you sure reset password?</h2>
                <button on:click={() => resetPassword()}>RESET PASSWORD</button>        
                <button on:click={() => showResetModal = false}>CLOSE</button> 
              </div>
            </div>
          {/if}

        </div>    
      </div>
    {/if} 
  {/if}
</div>