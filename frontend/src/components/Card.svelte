<script lang="ts">
    import type { GamesDto } from '../lib/api/dto/GamesDto';
    import * as m from '../generated/paraglide/messages.js';
    export let game: GamesDto;
    export let onSelect: (game: GamesDto) => void;

    function bestReleaseDate(g: GamesDto): string {
        return (
            g.releaseDate?.releaseDateUs ??
            g.releaseDate?.releaseDateJp ??
            g.releaseDate?.releaseDateEu ??
            g.releaseDate?.releaseDateAu ??
            'Unknown'
        );
    }

    // Pick colors however you like; these are reasonable “Pokémon box” vibes.
    const ACCENTS: Record<string, string> = {
        red: '#EF4444',
        blue: '#3B82F6',
        yellow:'#fff647',
        gold: '#F59E0B',
        silver: '#94A3B8',
        crystal: '#22D3EE',
        ruby: '#E11D48',
        sapphire: '#2563EB',
        colosseum: '#531bb7',
        leafgreen: '#00C38E',
        firered: '#EE5253',
        emerald: '#10B981',
        xd: '#531bb7',
        pearl: '#E879F9',
        diamond: '#60A5FA',
        platinum: '#A3A3A3',
        black: '#111827',
        white: '#E5E7EB',
        x: '#2563EB',
        y: '#EF4444',
        sun: '#F59E0B',
        moon: '#6366F1',
        eevee: '#7c460f',
        pikachu: '#edf50b',
        sword: '#37c7f3',
        shield: '#ff2041',
        arceus: '#acb3c5',
        za: '#39eb25',
        scarlet: '#DC2626',
        violet: '#7C3AED',
    };

    function accentForGame(g: GamesDto): string {
        const name = (g.name ?? '').toLowerCase();

        // Find first matching keyword (ruby, sapphire, etc.)
        for (const key in ACCENTS) {
            if (name.includes(key)) return ACCENTS[key];
        }

        // fallback accent
        return '#6366F1';
    }

    $: accent = accentForGame(game);

    function handleClick() {
        onSelect(game);
    }
</script>

<button class="card" type="button" on:click={handleClick} style={`--accent: ${accent};`}>
    <div class="card__media">
        {#if game.credits?.imageUrl}
            <img
                    class="card__img"
                    src={`/nuzlucke${game.credits.imageUrl}`}
                    alt={`${game.name} cover`}
                    loading="lazy"
            />
        {:else}
            <div class="card__placeholder">m.noImage()</div>
        {/if}
    </div>

    <div class="card__body">
        <div class="card__title">{game.name}</div>

        <div class="meta">
            <span class="chip">{m.platform()} {game.platform}</span>
            {#if game.isRomHack}
                <span class="chip chip--warning">ROM Hack</span>
            {/if}
        </div>

        <div class="card__footer">
            <span class="chip">Creator: {game.creator}</span>
            <span class="small chip chip--warning">
        {#if game.generationsIncluded?.length}
          Gen {game.generationsIncluded.join(', ')}
        {/if}
      </span>
        </div>
    </div>
</button>

<style>
    .card {
        --accent: #6366F1;

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
        transition: transform 120ms ease, border-color 120ms ease, background 120ms ease, box-shadow 120ms ease;
    }

    .card:hover {
        transform: translateY(-1px);

        border-color: var(--accent);

        border-color: color-mix(in srgb, var(--accent) 55%, transparent);

        box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent);

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

    .card__title { font-weight: 800; font-size: 18px; margin-bottom: 8px; text-transform: capitalize;display: flex;justify-content: center; }

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

    @media (min-width: 720px) {
        .card { grid-column: span 6; }
    }
    @media (min-width: 1020px) {
        .card { grid-column: span 4; }
        .card__media { width: 140px; height: 140px; }
        .card { grid-template-columns: 140px 1fr; }
    }
</style>