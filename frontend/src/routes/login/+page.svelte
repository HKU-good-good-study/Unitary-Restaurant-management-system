<script lang="ts">
    import { onMount } from 'svelte';
    let username = '';
    let password = '';
    
    onMount(() => {
        let registerButton = document.getElementById("register");
        document.body.style.backgroundColor = '#ADD8E6'; // Light Blue
        if (registerButton) {
        registerButton.onclick = function(){
            window.location.href="http://localhost:5173/register";
        }
    }
    });


    async function submitForm() {
        const response = await fetch('http://localhost:8000/auth/users/tokens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        console.log(data);
    }
</script>

<style>

    body {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Set the height of the entire viewport */
        margin: 0; /* Remove default body margin */
        background-color: #ADD8E6; /* Light Blue background */
    }

    .login-container  {
        background-color: gray;
        width: 300px;
        display:flex;
        flex-direction: column;
        padding: 20px;
        color: white;
        border-radius: 5px;
        justify-content: center;
        align-items: center;
    }

    .input-field {
        margin-bottom: 10px;
    }

    button {
        background-color: #4B8BF4; /* Blue background */
        color: white;
        border: 1px solid #1F50A9; /* Dark blue border */
        padding: 10px 20px;
        cursor: pointer;
        align-self: center;
        text-shadow: none;
        
        font-family: Tahoma, sans-serif; /* Font similar to Windows XP */
        font-size: 11px;
        box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.5), /* Inner shadow */
                    1px 1px 1px rgba(255, 255, 255, 0.6) inset; /* Outer glow */
        transition: all 0.1s ease-in-out; /* Smooth transition */
    }

    button:active {
        background-color: #1F50A9; /* Darker blue background when clicked */
        box-shadow: none; /* Remove shadow when clicked */
    }
</style>

<body>
    <div class="login-container">
        <h2>Login</h2>
        <div class="input-field">
            <label for="username">Username:</label>
            <input id="username" bind:value={username} type="text" placeholder="Enter Username">
        </div>
        <div class="input-field">
            <label for="password">Password:</label>
            <input id="password" bind:value={password} type="password" placeholder="Enter Password">
        </div>
        <div class="buttons">
            <button on:click={submitForm}>Submit</button>
            <button id="register">Register</button>
        </div>
        
    </div>
</body>
