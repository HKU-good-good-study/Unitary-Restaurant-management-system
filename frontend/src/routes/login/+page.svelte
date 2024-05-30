<script>
    import { onMount } from 'svelte';
    let username = '';
    let password = '';

    onMount(() => {
        document.body.style.backgroundColor = '#ADD8E6'; // Light Blue
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
    .login-container {
        background-color: gray;
        width: 300px;
        padding: 20px;
        color: white;
        border-radius: 5px;
        margin: 0 auto;
    }
    .input-field {
        margin-bottom: 10px;
    }
    button {
        background-color: gray;
        color: white;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
    }
</style>

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
    <button on:click={submitForm}>Submit</button>
</div>
