<script  context="module">
    import { user } from '../stores';    

    export async function validation (){
        const roleResponse = await fetch('http://localhost:8000/auth/users/me', {
            method: 'GET',
            credentials: 'include', // This is important for cookies to be sent
        });
        const roleData = await roleResponse.json();
        // console.log(roleData);
        user.username=roleData.username;
        user.role=roleData.role;
        user.imgSrc="./src/images/";
        user.imgSrc=user.imgSrc+user.role.split(" ")[0].toLowerCase()+'.png';
        user.email=roleData.email;
        user.phone_number=roleData.phone_number;
    }

    export function getNowTime(){
        // 获取当前时间
        const currentDate = new Date();
        // 格式化时间
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0');
        const day = String(currentDate.getDate()).padStart(2, '0');
        const hours = String(currentDate.getHours()).padStart(2, '0');
        const minutes = String(currentDate.getMinutes()).padStart(2, '0');
        const seconds = String(currentDate.getSeconds()).padStart(2, '0');

        const formattedDateTime = `${year}-${month}-${day}-${hours}:${minutes}:${seconds}`;
        return formattedDateTime;
    }

</script>