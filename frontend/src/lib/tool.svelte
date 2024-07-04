<script  context="module">
    import { user } from '../stores';    

    export async function validation (){
        const roleResponse = await fetch('http://localhost:8000/auth/users/me', {
            method: 'GET',
            credentials: 'include', // This is important for cookies to be sent
        });
        const roleData = await roleResponse.json();
        console.log(roleData);
        user.name=roleData.username;
        user.role=roleData.role;
        user.imgSrc="./src/images/";
        user.imgSrc=user.imgSrc+user.role.split(" ")[0].toLowerCase()+'.png';
        user.email=roleData.email;
        user.phone_number=roleData.phone_number;
    }

</script>