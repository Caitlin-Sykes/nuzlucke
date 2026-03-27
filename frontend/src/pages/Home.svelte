<script lang="ts">
  import { onMount } from 'svelte';
  import Card from '../components/Card.svelte';
  import { getAvailableGames, type GamesDto } from '../lib/api/dto/GamesDto';
  import * as m from '../generated/paraglide/messages';

  let games: GamesDto[] = [];
  let loading = true;
  let error: string | null = null;

  function selectGame(game: GamesDto) {
    alert(`Selected: ${game.name}`);
  }

  onMount(async () => {
    try {
      loading = true;
      error = null;
      games = await getAvailableGames();
    } catch (e) {
      error = e instanceof Error ? e.message : m['errors.noGames']();
    } finally {
      loading = false;
    }
  });
</script>

<header class="hero">
  <h1>{m['home.title']()}</h1>
  <p>{m['home.description']()}</p>
</header>

<main class="page">
  {#if loading}
    <div class="state">{m['home.state.waiting']()}</div>
  {:else if error}
    <div class="state state--error">
      <div class="state__title">{m['home.state.load_games_fail']()}</div>
      <div class="state__body">{error}</div>
      <button class="btn" on:click={() => location.reload()}>{m['actions.retry']()}</button>
    </div>
  {:else}
    <section class="grid" aria-label={m['home.available_games']()}>
      {#each games as game (game.name)}
        <Card {game} onSelect={selectGame} />
      {/each}
    </section>
  {/if}
</main>

<style>
  .hero {
    padding: 28px 18px 10px;
    border-bottom: 1px solid rgb(255 255 255 / 8%);
  }
  h1 { margin: 0 0 6px; font-size: 32px; letter-spacing: -0.02em; }
  p { margin: 0; opacity: 0.85; }

  .page { max-width: 1100px; margin: 0 auto; padding: 18px; }

  .state {
    padding: 16px;
    border-radius: 14px;
    background: rgb(255 255 255 / 4%);
    border: 1px solid rgb(255 255 255 / 8%);
  }
  .state--error { border-color: rgb(239 68 68 / 35%); }
  .state__title { font-weight: 700; margin-bottom: 6px; }
  .state__body { opacity: 0.9; margin-bottom: 12px; white-space: pre-wrap; }

  .grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 20px 70px;
  }

  .btn {
    border: 1px solid rgb(255 255 255 / 14%);
    background: rgb(255 255 255 / 6%);
    color: inherit;
    padding: 8px 12px;
    border-radius: 12px;
    cursor: pointer;
  }
</style>