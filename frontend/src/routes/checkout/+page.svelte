<script lang="ts">
  import { onMount } from 'svelte';
  let orderId = '';

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault(); // Prevent the default form submission behavior
    try {
      const response = await fetch('http://localhost:8000/checkout/new', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // This is important for cookies to be sent
        body: JSON.stringify({
          order_id: orderId,
          // Include other necessary fields as per your TransactionCreate model
        }),
      });

      if (response.ok) {
        const data = await response.json();
        window.location.href = data.url; // Redirect to the payment URL
      } else {
        console.error('Failed to create transaction:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
</script>

<form on:submit={handleSubmit}>
  <label for="orderId">Order ID:</label>
  <input type="text" id="orderId" bind:value={orderId} required>
  <button type="submit">Submit</button>
</form>