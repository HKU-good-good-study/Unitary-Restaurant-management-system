<script lang="ts">
  import { page } from '$app/stores';
  import { derived } from 'svelte/store';

  const queryParams = derived(page, $page => $page.url.searchParams);

  let successMessage = '';
  let errorMessage = '';

  queryParams.subscribe(params => {
    if (params.get('success') === 'true') {
      successMessage = 'Payment successful. Thank you for your purchase!';
    } else if (params.get('canceled') === 'true') {
      errorMessage = 'Payment was canceled. You have not been charged.';
    }
  });
</script>

{#if successMessage}
  <p align="center">{successMessage}</p>
{:else if errorMessage}
  <p align="center">{errorMessage}</p>
{/if}