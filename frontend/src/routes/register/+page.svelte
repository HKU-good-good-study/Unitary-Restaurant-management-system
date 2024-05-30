<script>
    import { onMount } from 'svelte';
    let username = '';
    let password = '';
    let confirmPassword = '';
    let email = '';
    let phoneNumber = '';
    let role = 'Manager';
    let countryCode = ''
    let remarks = '';

    onMount(() => {
        document.body.style.backgroundColor = '#ADD8E6'; // Light Blue
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

    .form-container {
        background-color: gray;
        width: 300px;
        padding: 20px;
        color: white;
        border-radius: 5px;
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

<html lang="utf-8">
    <body>
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
            
            
            <button on:click={submitRegistrationForm}>Register</button>
        </div>
    </body>
    
</html>