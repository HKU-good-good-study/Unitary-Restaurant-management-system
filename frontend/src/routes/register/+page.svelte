<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    let username = '';
    let password = '';
    let confirmPassword = '';
    let email = '';
    let phoneNumber = '';
    let role = 'Dining Room Staff';
    //role = 'Kitchen Staff';
    //role = 'Manager';
    role = 'Customer';
    let countryCode = ''
    let remarks = '';
    

    onMount(() => {
        history.replaceState(null, 'Profile', '/profile');
        document.title = 'Profile';

        document.body.style.backgroundColor = '#ADD8E6'; // Light Blue
        let loginButton = document.getElementById("login");
        if (loginButton){
            loginButton.onclick = function() {
                window.location.href="http://localhost:5173/login";
            }
        }
    });

    async function submitRegistrationForm() {
        if (password !== confirmPassword) {
            console.error("Passwords don't match!");
            return;
        }
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
        //goto('./login');
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

.form-container {
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
    width: fit-content;
}

h2 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}

.input-field {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    justify-content: space-between;
}

.input-field > * {
    margin-right: 15px;
}

input {
    padding: 10px 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
    flex-grow: 1;
    font-size: 16px;
    margin-bottom: 15px;
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



</style>

<html lang="utf-8">
        <div class="form-container">
            <h2>Register</h2>
            <div class="input-field">
                <label for="username">Username:</label>
                <input id="username" bind:value={username} type="text" placeholder="Enter Username">
            </div>
            <div class="input-field">
                <label for="password">Password:</label>
                <input id="password" bind:value={password} type="password" placeholder="Enter Password">
            </div>
            <div class="input-field">
                <label for="confirmPassword">Confirm Password:</label>
                <input id="confirmPassword" bind:value={confirmPassword} type="password" placeholder="Confirm Password">
            </div>
            <div class="input-field">
                <label for="email">Email:</label>
                <input id="email" bind:value={email} type="email" placeholder="Enter Email">
            </div>
            <div id="phone number" class="input-field">
                <div class="input-field">
                    <label for="countryCode">Country Code:</label>
                    <select id="countryCode" bind:value={countryCode}>
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
                <div class="input-field">
                    <label for="phoneNumber">Phone Number:</label>
                    <input id="phoneNumber" bind:value={phoneNumber} type="tel" placeholder="Enter Phone Number">
                </div>
            </div>
            <div id="buttons">
                <button on:click={submitRegistrationForm}>Register</button>
                <button id="login">Back To Login</button>
            </div>
            
        </div>
    
</html>