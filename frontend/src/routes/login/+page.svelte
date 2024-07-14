
<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { user } from '../../stores'; 
    import { validation } from '$lib/tool.svelte';

    let username = '';
    let password = '';
    let isRegisterModalOpen = false;
    let registerUsername = '';
    let registerEmail = '';
    let registerPhoneNumber = '';
    let registerRole = 'Customer';
    let registerRemarks = '';

    let showResetModal = false;
    let showInputModal = false;
    let userEmail = '';
    let resetToken ='';

    onMount(() => {
        document.body.style.backgroundColor = '#f2f2f2'; // Light Gray
        // history.replaceState(null, 'Profile', '/profile');
        document.title = 'Login Page';
        userEmail='';
        resetToken='';
    });

    async function submitLogin() {
        const response = await fetch('http://localhost:8000/auth/users/tokens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // This is important for cookies to be sent
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        // console.log(data);

        // const roleResponse = await fetch('http://localhost:8000/auth/users/me', {
        //     method: 'GET',
        //     credentials: 'include', // This is important for cookies to be sent
        // });
        // const roleData = await roleResponse.json();
        // console.log(roleData);

        // user.name=roleData.username;
        // user.role=roleData.role;
        // user.imgSrc="./src/images/";
        // user.imgSrc=user.imgSrc+user.role.split(" ")[0].toLowerCase()+'.png';
        // user.email=roleData.email;
        // user.phone_number=roleData.phone_number;
        // console.log(user);

        await validation();

        // sessionStorage.setItem("role",roleData.role);
        // sessionStorage.setItem("username",roleData.username);
        // sessionStorage.setItem("email",roleData.email);
        // sessionStorage.setItem("phone_number",roleData.phone_number);
        

        goto('./role');
    }

    function goToRegister() {
        goto('./register');
    }

    function toggleRegisterModal() {
        isRegisterModalOpen = !isRegisterModalOpen;
        goToRegister();
    //     window.location.href = "http://localhost:5173/register";
    }
    async function noRegisterOrder(){
        username="testC";
        password='!Qw123456';
        const response = await fetch('http://localhost:8000/auth/users/tokens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', // This is important for cookies to be sent
            body: JSON.stringify({ username, password })
        });
        const data=await response.json();
        console.log(data);
        
        await validation();
        goto('./menu');
    }

    async function getResetPassword(){
        showInputModal=true;
        const emailData={
            email:userEmail
        }
        try {
        const response = await fetch('http://localhost:8000/auth/users/password-reset-token', {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(emailData),
        });

        if (response.ok) {
            showResetModal=true;
            console.log("check reset token");
        } 
        else {
            console.error("Error requesting password reset token:", response.statusText);
            return null;
        }
        } 
        catch (error) {
        console.error("Error requesting password reset token:", error);
        return null;
        }      
  }

    async function resetPassword(){
      const resetData={
              new_password: '!Qw123456',
              token: resetToken
            };
      // console.log(resetData);
      const response = await fetch('http://localhost:8000/auth/users/password-reset',{
          method: 'POST',
          credentials: 'include',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(resetData)        
      });
      if (response.ok) {
        alert("reset password");
        showResetModal=false;
      } 
      else {
        console.error("Error reset password :", response.statusText);
        return null;
      }
      
  }
</script>

<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    .container {
        max-width: 800px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
        margin-top: 100px;
        width: fit-content;
    }

    h2 {
        text-align: center;
        color: #333;
        margin-bottom: 30px;
    }

    .row {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        justify-content: space-between;
    }

    .row > * {
        margin-right: 15px;
    }

    input {
        padding: 10px 15px;
        border: 1px solid #ccc;
        border-radius: 5px;
        flex-grow: 1;
        font-size: 16px;
        margin-bottom: 15px; /* Added margin-bottom for spacing */
    }

    .row button {
        background-color: #333;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }

    .row button:hover {
        background-color: #555;
    }

    .underline{
        text-decoration: underline;
        text-decoration-color:#0550c0;
        text-decoration-thickness: 1%;
        text-decoration-style:wavy;
        font-size: small;
        color: #555;
    }

    /* .register-modal {
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
    .register-form {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
    } */

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


    <div class="container">
        <h2>Login</h2>

        <div class="row">
            <label for="username">Username:</label>
            <input id="username" bind:value={username} type="text" placeholder="Enter Username">
        </div>

        <div class="row">
            <label for="password">Password:</label>
            <input id="password" bind:value={password} type="password" placeholder="Enter Password">
            <p class="underline" on:click={()=> getResetPassword()}>forgetPassword</p>
        </div>           

        <div class="row">
            <button on:click={submitLogin}>Submit</button>
            <button on:click={toggleRegisterModal}>Register</button>
            <button on:click={noRegisterOrder}>Order without registration</button>
        </div>
    </div>
    

    {#if showInputModal}
    <div class="modal" on:click={() => showInputModal = false}>
        <div class="modal-content" on:click|stopPropagation>
        <h2>Please input email</h2>
        <div class="row">
            <label for="email">Email:</label>
            <input id="email" bind:value={userEmail}>
        </div>
        <button on:click={() => getResetPassword()}>Submit</button>        
        <button on:click={() => showInputModal = false}>Close</button> 
        </div>
    </div>
    {/if}

    {#if showResetModal}
    <div class="modal" on:click={() => showResetModal = false}>
        <div class="modal-content" on:click|stopPropagation>
        <h2>Please input reset token</h2>
        <div class="row">
            <label for="token">resetToken:</label>
            <input id="token" bind:value={resetToken}>
        </div>
        <button on:click={() => resetPassword()}>RESET PASSWORD</button>        
        <button on:click={() => showResetModal = false}>CLOSE</button> 
        </div>
    </div>
    {/if}

<!-- {#if isRegisterModalOpen}
<div class="register-modal">
    <div class="register-form">
        <h2>Register</h2>
        <div class="row">
            <label for="registerUsername">Username:</label>
            <input id="registerUsername" bind:value={registerUsername} type="text" placeholder="Enter Username">
        </div>
        <div class="row">
            <label for="registerEmail">Email:</label>
            <input id="registerEmail" bind:value={registerEmail} type="email" placeholder="Enter Email">
        </div>
        <div class="row">
            <label for="registerPhoneNumber">Phone Number:</label>
            <input id="registerPhoneNumber" bind:value={registerPhoneNumber} type="tel" placeholder="Enter Phone Number">
        </div>
        <div class="row">
            <label for="registerRole">Role:</label>
            <select id="registerRole" bind:value={registerRole}>
                <option value="Manager">Manager</option>
                <option value="Dining Staff">Dining Staff</option>
                <option value="Kitchen Staff">Kitchen Staff</option>
                <option value="Customer">Customer</option>
            </select>
        </div>
        <div class="row">
            <label for="registerRemarks">Remarks:</label>
            <textarea id="registerRemarks" bind:value={registerRemarks} placeholder="Enter Remarks"></textarea>
        </div>
        <div class="row">
            <button on:click={goToRegister}>Register</button>
            <button on:click={toggleRegisterModal}>Close</button>
        </div>
    </div>
</div>
{/if} -->
