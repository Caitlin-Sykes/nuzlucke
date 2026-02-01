<script lang="ts">
  import { onMount } from 'svelte';
  import { getAvailableGames, type GamesDto } from '../lib/api/dto/GamesDto';

  let games: GamesDto[] = [];
  let loading = true;
  let error: string | null = null;

  function bestReleaseDate(g: GamesDto): string {
    return (
      g.releaseDate?.releaseDateUs ??
      g.releaseDate?.releaseDateJp ??
      g.releaseDate?.releaseDateEu ??
      g.releaseDate?.releaseDateAu ??
      'Unknown'
    );
  }

  function selectGame(game: GamesDto) {
    // For now, just “select” it. Replace with navigation later.
    // This keeps your UI working immediately.
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
        <button class="card" type="button" on:click={() => selectGame(game)}>
          <div class="card__media">
            {#if game.credits?.imageUrl}
              <img class="card__img" src={`/nuzlucke${game.credits.imageUrl}`} alt={`${game.name} cover`} loading="lazy" />
            {:else}
              <div class="card__placeholder">No image</div>
            {/if}
          </div>

          <div class="card__body">
            <div class="card__title">{game.name}</div>

            <div class="meta">
              <span class="chip">{game.platform}</span>
              {#if game.isRomHack}
                <span class="chip chip--warning">ROM Hack</span>
              {/if}
              <span class="chip chip--muted">Release: {bestReleaseDate(game)}</span>
            </div>

            <div class="card__footer">
              <span class="small">
                {game.creator}
                {#if game.generationsIncluded?.length}
                  · Gen {game.generationsIncluded.join(', ')}
                {/if}
              </span>
              <span class="cta">Select →</span>
            </div>
          </div>
        </button>
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

  .card {
    grid-column: span 12;
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: 12px;
    padding: 12px;
    border-radius: 16px;
    text-align: left;

    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);

    cursor: pointer;
    transition: transform 120ms ease, border-color 120ms ease, background 120ms ease;
  }
  .card:hover {
    transform: translateY(-1px);
    border-color: rgba(99, 102, 241, 0.45);
    background: rgba(255,255,255,0.055);
  }

  .card__media {
    width: 120px;
    height: 120px;
    border-radius: 14px;
    overflow: hidden;
    background: rgba(0,0,0,0.25);
    border: 1px solid rgba(255,255,255,0.08);
    display: grid;
    place-items: center;
  }
  .card__img { width: 100%; height: 100%; object-fit: cover; }
  .card__placeholder { font-size: 12px; opacity: 0.7; }

  .card__title { font-weight: 800; font-size: 18px; margin-bottom: 8px; text-transform: capitalize;}

  .meta { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }

  .chip {
    font-size: 12px;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.05);
    opacity: 0.95;
  }
  .chip--warning { border-color: rgba(245, 158, 11, 0.35); }
  .chip--muted { opacity: 0.8; }

  .card__footer {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px;
  }

  .small { font-size: 12px; opacity: 0.75; }
  .cta { font-weight: 700; opacity: 0.9; }

  .btn {
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.06);
    color: inherit;
    padding: 8px 12px;
    border-radius: 12px;
    cursor: pointer;
  }

  @media (min-width: 720px) {
    .card { grid-column: span 6; }
  }
  @media (min-width: 1020px) {
    .card { grid-column: span 4; }
    .card__media { width: 140px; height: 140px; }
    .card { grid-template-columns: 140px 1fr; }
  }
</style>