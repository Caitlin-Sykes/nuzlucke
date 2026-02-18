<script lang="ts">
  import { onMount } from 'svelte';
  import Card from '../components/Card.svelte';
  import { getAvailableGames, type GamesDto } from '../lib/api/dto/GamesDto';

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
      error = e instanceof Error ? e.message : 'Failed to load games.';
    } finally {
      loading = false;
    }
  });
</script>

<header class="hero">
  <h1>Nuzlucke</h1>
  <p>Select a Pokémon game to start your run.</p>
</header>

<main class="page">
  {#if loading}
    <div class="state">Loading games…</div>
  {:else if error}
    <div class="state state--error">
      <div class="state__title">Couldn’t load games</div>
      <div class="state__body">{error}</div>
      <button class="btn" on:click={() => location.reload()}>Retry</button>
    </div>
  {:else}
    <section class="grid" aria-label="Available games">
      {#each games as game (game.name)}
        <Card {game} onSelect={selectGame} />
      {/each}
    </section>
  {/if}
</main>

<style>
  .hero {
    padding: 28px 18px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  h1 { margin: 0 0 6px; font-size: 32px; letter-spacing: -0.02em; }
  p { margin: 0; opacity: 0.85; }

  .page { max-width: 1100px; margin: 0 auto; padding: 18px; }

  .state {
    padding: 16px;
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
  }
  .state--error { border-color: rgba(239, 68, 68, 0.35); }
  .state__title { font-weight: 700; margin-bottom: 6px; }
  .state__body { opacity: 0.9; margin-bottom: 12px; white-space: pre-wrap; }

  .grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 14px;
  }

  .btn {
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.06);
    color: inherit;
    padding: 8px 12px;
    border-radius: 12px;
    cursor: pointer;
  }
</style>