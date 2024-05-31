<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let username = '';
    let password = '';
    let isRegisterModalOpen = false;
    let registerUsername = '';
    let registerPassword = '';
    let registerEmail = '';
    let registerPhoneNumber = '';
    let registerRole = 'Customer';
    let registerRemarks = '';

    onMount(() => {
        document.body.style.backgroundColor = '#f2f2f2'; // Light Gray
    });

    async function submitLogin() {
        const response = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        console.log(data);

        if (data.role === 'Manager') {
            goto('./manager');
        } else if (data.role === 'Dining Staff') {
            goto('./dining');
        } else if (data.role === 'Kitchen Staff') {
            goto('./kitchen');
        } else if (data.role === 'Customer') {
            goto('./customer');
        }
    }

    async function submitRegister() {
        if (!registerUsername || !registerPassword || !registerEmail || !registerPhoneNumber) {
            alert('Please fill in all the required fields.');
            return;
        }
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: registerUsername, password: registerPassword, email: registerEmail, phone_number: registerPhoneNumber, role: registerRole, remarks: registerRemarks })
        });
        const data = await response.json();
        console.log(data);

        if (data.role === 'Manager') {
            goto('./manager');
        } else if (data.role === 'Dining Staff') {
            goto('./dining');
        } else if (data.role === 'Kitchen Staff') {
            goto('./kitchen');
        } else if (data.role === 'Customer') {
            goto('./customer');
        }
    }

    function toggleRegisterModal() {
        isRegisterModalOpen = !isRegisterModalOpen;
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
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
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

    button {
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

    button:hover {
        background-color: #555;
    }

    .register-modal {
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
    </div>
    <div class="row">
        <button on:click={submitLogin}>Submit</button>
        <button on:click={toggleRegisterModal}>Register</button>
    </div>
</div>

{#if isRegisterModalOpen}
<div class="register-modal">
    <div class="register-form">
        <h2>Register</h2>
        <div class="row">
            <label for="registerUsername">Username:</label>
            <input id="registerUsername" bind:value={registerUsername} type="text" placeholder="Enter Username">
        </div>
        <div class="row">
            <label for="registerPassword">Password:</label>
            <input id="registerPassword" bind:value={registerPassword} type="password" placeholder="Enter Password">
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
            <button on:click={submitRegister}>Register</button>
            <button on:click={toggleRegisterModal}>Close</button>
        </div>
    </div>
</div>
{/if}