<script>
  import { onMount } from "svelte";  
  import { user } from '../../stores';
  import  {validation}  from '$lib/tool.svelte';  
  
  let role ='';
  $: role=user.role;

  
  let selectUser={name:"",role:"",status:true,index:-1,email:"",countryCode:"",phone_number:"",imgSrc:""};


  onMount(async () => {
    await validation();
    // history.replaceState(null, 'Profile', '/profile');
    selectUser.name=user.name;
    selectUser.imgSrc="./src/images/";
    selectUser.imgSrc=user.imgSrc+user.role.split(" ")[0].toLowerCase()+'.png';
    selectUser.email=user.email;
    selectUser.phone_number=user.phone_number.slice(4);
    selectUser.countryCode=selectUser.phone_number.split('-')[0];
    selectUser.phone_number=selectUser.phone_number.split('-')[1]+selectUser.phone_number.split('-')[2]+selectUser.phone_number.split('-')[3];
    console.log(selectUser);
    
    document.title = 'User profile';
    })


    // $: selectUser.name=user.name;
    // $: selectUser.imgSrc="./src/images/";
    // $: selectUser.imgSrc=user.imgSrc+user.role.split(" ")[0].toLowerCase()+'.png';
    // $: selectUser.email=user.email;
    // $: selectUser.phone_number=user.phone_number.slice(4);
    // $: selectUser.countryCode=selectUser.phone_number.split('-')[0];
    // $: selectUser.phone_number=selectUser.phone_number.split('-')[1]+selectUser.phone_number.split('-')[2]+selectUser.phone_number.split('-')[3];
    // $: console.log(selectUser);

   

    
    function update(){
      user.name=selectUser.name;
      user.imgSrc=selectUser.imgSrc;
      user.email=selectUser.email;
      user.phone_number="tel:"+selectUser.countryCode+selectUser.phone_number;
      console.log(user);
    }
</script>

<style>

</style>

    <h3>please update user information</h3>

    <div class="row">
      <label for="userName">name:</label>
      <input id="userName" bind:value={selectUser.name} />
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
      <input id="phoneNumber" bind:value={selectUser.phone_number}>
    </div>
    <div class="row">
      <label for="email">email:</label>
      <input id="email" bind:value={selectUser.email}>
    </div>
    <button on:click={update}>Submit</button>