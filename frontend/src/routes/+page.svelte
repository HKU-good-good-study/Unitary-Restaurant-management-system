<script context="module">
    import { redirect } from '@sveltejs/kit';
  
    export function load() {
        throw redirect(307, '/login');
    }
</script>
  
<h1>hello</h1>