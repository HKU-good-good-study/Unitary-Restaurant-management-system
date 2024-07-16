<script>
  import { onMount } from "svelte";  
  import { user } from '../../stores';
  import  {validation}  from '$lib/tool.svelte';  
  
  let role ='';
  $: role=user.role;

  let newPassword ='';
  let oldPassword ='';

  let showResetModal=false;

  
  let selectUser={username:"",role:"",status:true,index:-1,email:"",countryCode:"",phone_number:"",imgSrc:"",remarks:""};
  var userData={};
  let originUser={username:"",role:"",status:true,index:-1,email:"",countryCode:"",phone_number:"",imgSrc:"",remarks:""};


  onMount(async () => {
    await validation();
    // history.replaceState(null, 'Profile', '/profile');
    selectUser.role=user.role;
    selectUser.username=user.username;
    selectUser.imgSrc="./src/images/";
    selectUser.imgSrc=user.imgSrc+user.role.split(" ")[0].toLowerCase()+'.png';
    selectUser.email=user.email;
    // selectUser.phone_number=user.phone_number.slice(4);
    // selectUser.countryCode=selectUser.phone_number.split('-')[0];
    // selectUser.phone_number=selectUser.phone_number.split('-')[1]+selectUser.phone_number.split('-')[2]+selectUser.phone_number.split('-')[3];
    selectUser.countryCode=user.phone_number.split(' ')[0];
    selectUser.phone_number=user.phone_number.split(' ')[1];
    originUser.countryCode=selectUser.countryCode;
    originUser.phone_number=selectUser.phone_number;
    // console.log(selectUser);
    
    document.title = 'User profile';
    })



    async function update(){
      if(selectUser.username!=user.username){
        userData.username=selectUser.username;
      }
      
      if(selectUser.email!=user.email){
        userData.email=selectUser.email;
      }

      if(selectUser.countryCode!=originUser.countryCode || selectUser.phone_number!=originUser.phone_number){
        userData.phone_number=selectUser.countryCode + " " + selectUser.phone_number;
      }

      const response = await fetch('http://localhost:8000/auth/users/me', {
            method: 'PATCH',
            credentials: 'include', // This is important for cookies to be sent
            headers: {
              'Content-Type': 'application/json'
           },
            body: JSON.stringify(userData),
        });

      if (response.ok) {
        user.username=selectUser.username;
        user.email=selectUser.email;
        user.phone_number="tel:-"+selectUser.countryCode + "-" + selectUser.phone_number;
        location.reload();
        // console.log("pro"+user.username);
      } 
      else {
        const data=await response.json();
        alert(data.detail);
        console.error('Error update user:', response.status);
      }
    }
    
    async function resetPassword(){
      const resetData={
        new_password: newPassword,
        old_password: oldPassword
      }
      const response = await fetch('http://localhost:8000/auth/users/password-update', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(resetData)
      });
      // const data = await response.json();
      if(response.ok){        
        // console.log(data);
        showResetModal=false;
      }
      else{
        // console.log(data);
        alert("reset wrong!");
      }
    }
    

</script>

<style>
  .block {
    display: flex;
    justify-content: center;
    gap: 40px;
    padding: 100px;
    background-color: #f8f8f8;
  }

  .box {
    display: flex;
    flex-direction: column;
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 60px;
    background-color: #fff;
    width: 360px; /* Set the width of each product */
  }

  .box button{
    margin: auto;
    margin-top: 10px;
    width: 150px;
    height: 30px;
    
    margin-left: 5%;
    border:none;
    border-radius: 8%;
  }


  .box h2 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
  }

  .box .row {
    margin-bottom: 10px;
  }

  .resetButton{   
    background-color: #D3D3D3;
    border-color: #D3D3D3;
    color:#00BFFF;
    background-image: linear-gradient(45deg, #00BFFF 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 300ms ease-in-out;
  }

  .resetButton:hover{
    color: black;  border: 0;
    background-color: #00BFFF;  
    -webkit-box-shadow: 10px 10px 99px 6px rgba(0,191,255);  
    -moz-box-shadow: 10px 10px 99px 6px rgba(0,191,255);
    box-shadow: 10px 10px 99px 6px rgba(0,191,255);
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
{#if user.username!='customer'}
  <div class="block">
    <div class="box">
      <h2> Update user information here</h2>
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
          <input id="phoneNumber" bind:value={selectUser.phone_number} type="tel">
        </div>
        <div class="row">
          <label for="email">email:</label>
          <input id="email" bind:value={selectUser.email}>
        </div>
        <div class="row">
      <button on:click={update}>Update</button>
          <button class=resetButton on:click={()=> showResetModal = true}>Reset Password</button>
        </div>
      

      {#if showResetModal}
            <div class="modal" on:click={() => showResetModal = false}>
              <div class="modal-content" on:click|stopPropagation>

                <label for="oldPassword">oldPassword:</label>
                <input id="oldPassword" bind:value={oldPassword}  placeholder="Enter oldPassword">

                <label for="newPassword">newPassword:</label>
                <input id="newPassword" bind:value={newPassword}  placeholder="Enter newPassword">

                <button on:click={() => resetPassword()}>RESET</button>        
                <button on:click={() => showResetModal = false}>CLOSE</button> 
              </div>
            </div>
          {/if}
    </div>
  </div>
{/if}