<script lang="ts">
    import type {GamesDto} from '../lib/api/dto/GamesDto';
    import * as m from '../generated/paraglide/messages';
    import Info from '~icons/solar/info-square-bold';
    import Circle from '~icons/solar/bolt-circle-bold';
    import Check from '~icons/solar/check-square-line-duotone';
    import Cross from '~icons/solar/close-square-line-duotone';

    export let game: GamesDto;
    export let onSelect: (game: GamesDto) => void;

    function formatGenRange(gens: number[] | undefined): string {
        if (!gens || gens.length === 0) return 'N/A';
        const min = Math.min(...gens);
        const max = Math.max(...gens);
        return min === max ? `${min}` : `${min}-${max}`;
    }

    const ACCENTS: Record<string, { background: string; border: string }> = {
        red: { background: 'linear-gradient(135deg, #d01920 0%, #ff4d4d 50%, #b11217 100%)', border: '#FFD700' },
        blue: { background: 'linear-gradient(135deg, #104c8e 0%, #3a7bd5 50%, #0a325e 100%)', border: '#FFD700' },
        yellow: { background: 'linear-gradient(135deg, #f9ce14 0%, #fff06a 50%, #d4ac0d 100%)', border: '#a2acb5' },
        gold: { background: 'linear-gradient(135deg, #bf953f 0%, #fcf6ba 45%, #b38728 50%, #fbf5b7 55%, #aa771c 100%)', border: '#d4af37' },
        silver: { background: 'linear-gradient(135deg, #9ba2ac 0%, #e5e7eb 50%, #7c818a 100%)', border: '#bec2cb' },
        crystal: { background: 'linear-gradient(135deg, #5875b9 0%, #a1c4fd 50%, #5875b9 100%)', border: '#c0c0c0' },
        ruby: { background: 'linear-gradient(135deg, #b13d2f 0%, #e52d27 50%, #8e3126 100%)', border: '#595654' },
        sapphire: { background: 'linear-gradient(135deg, #2b61a2 0%, #4facfe 50%, #2b61a2 100%)', border: '#e1ad01' },
        emerald: { background: 'linear-gradient(135deg, #00a64e 0%, #00ff73 50%, #00a64e 100%)', border: '#e1ad01' },
        leafgreen: { background: 'linear-gradient(135deg, #85c750 0%, #96e6a1 100%)', border: '#a2acb5' },
        firered: { background: 'linear-gradient(135deg, #e36439 0%, #f18e6d 100%)', border: '#a2acb5' },
        colosseum: { background: 'linear-gradient(135deg, #595654 0%, #3e3c3a 100%)', border: '#000000' },
        xd: { background: 'linear-gradient(135deg, #342377 0%, #6a5acd 50%, #e8268d 100%)', border: '#e8268d' },
        pearl: { background: 'linear-gradient(135deg, #b1685c 0%, #ffafbd 50%, #b1685c 100%)', border: '#fff' },
        diamond: { background: 'linear-gradient(135deg, #55a2b8 0%, #b2fefa 50%, #55a2b8 100%)', border: '#fff' },
        platinum: { background: 'linear-gradient(135deg, #bd8175 0%, #e8d5cc 50%, #bd8175 100%)', border: '#fff' },
        black: { background: 'linear-gradient(135deg, #111827 0%, #4b5563 100%)', border: '#e8268d' },
        white: { background: 'linear-gradient(135deg, #E5E7EB 0%, #FFFFFF 100%)', border: '#a2acb5' },
        x: { background: 'linear-gradient(135deg, #62bbad 0%, #84fab0 100%)', border: '#fff' },
        y: { background: 'linear-gradient(135deg, #ea604a 0%, #ff8a7a 100%)', border: '#fff' },
        sun: { background: 'linear-gradient(135deg, #f4ae1c 0%, #fbd786 50%, #f4ae1c 100%)', border: '#fff' },
        moon: { background: 'linear-gradient(135deg, #494596 0%, #6a11cb 100%)', border: '#fff' },
        eevee: { background: 'linear-gradient(135deg, #eec067 0%, #d39d38 100%)', border: '#fff' },
        pikachu: { background: 'linear-gradient(135deg, #efca45 0%, #f9ce14 100%)', border: '#fff' },
        sword: { background: 'linear-gradient(135deg, #0a9fda 0%, #2af5ff 100%)', border: '#fff' },
        shield: { background: 'linear-gradient(135deg, #e90a5f 0%, #ff4b2b 100%)', border: '#fff' },
        arceus: { background: 'linear-gradient(135deg, #93cc99 0%, #d2f1d5 100%)', border: '#fff' },
        scarlet: { background: 'linear-gradient(135deg, #e14336 0%, #ff6a5d 100%)', border: '#fff' },
        violet: { background: 'linear-gradient(135deg, #9c39a4 0%, #cf8bf3 100%)', border: '#fff' },
        za: { background: 'linear-gradient(135deg, #57b779 0%, #20bf55 100%)', border: '#fff' },
    };

    function accentForGame(g: GamesDto): { background: string; border: string } {
        const name = (g.name ?? '').toLowerCase();
        for (const key in ACCENTS) {
            if (name.includes(key)) return ACCENTS[key];
        }
        return { background: '#6366F1', border: '#e1ad01' };
    }

    function getTextColor(bg: string, gameName: string): string {
        const darkGames = ['blue', 'xd', 'black', 'moon', 'shield', 'violet', 'ruby', 'colosseum', 'red'];
        const name = gameName.toLowerCase();
        return darkGames.some(k => name.includes(k)) ? '#ffffff' : '#1a1a1a';
    }

    let flipped = false;

    function toggleFlip(e: MouseEvent) {
        e.stopPropagation();
        flipped = !flipped;
    }

    $: accent = accentForGame(game);
    $: textColor = getTextColor(accent.background, game.name ?? '');
    $: textShadow = textColor === '#ffffff'
        ? '1px 1px 3px rgba(0,0,0,0.8), 0px 0px 5px rgba(0,0,0,0.4)'
        : '0.5px 0.5px 0px rgba(255,255,255,0.7)';
    $: genDisplay = formatGenRange(game.generationsIncluded);
</script>

<div
        class="pokemon-card"
        class:is-flipped={flipped}
        role="button"
        tabindex="0"
        on:click={() => onSelect(game)}
        on:keydown={(e) => (e.key === 'Enter' || e.key === ' ') && onSelect(game)}
        style="--bg: {accent.background}; --border: {accent.border}; --text: {textColor}; --shadow: {textShadow};"
>
    <div class="card-inner">
        <div class="card-face card-front">
            <div class="card__header">
                <span class="card__name">{game.name}</span>
                <div class="card__hp">
                    <span class="hp-label">{m['card.gen']()}</span>
                    <span class="hp-value">{game.rulesetId ?? 100}</span>
                    <button class="flip-trigger" type="button" on:click={toggleFlip}>
                        <Info />
                    </button>
                </div>
            </div>

            <div class="card__stage">
                <div class="illustration-container">
                    {#if game.credits?.imageUrl}
                        <img class="illustration" src={`/nuzlucke${game.credits.imageUrl}`} alt={game.name} />
                    {:else}
                        <div class="illustration-placeholder">
                            <Info width="48" height="48" />
                        </div>
                    {/if}
                </div>
            </div>

            <div class="card__info-bar">
                {m['card.platform']()} {game.platform}
            </div>

            <div class="card__body">
                <div class="move">
                    <div class="move__header">
                        <Circle class="cost-icon" />
                        <span class="move__name">{m['card.creator']() || 'Creator'}</span>
                    </div>
                    <div class="move__description">{game.creator || 'Unknown'}</div>
                </div>

                <div class="move">
                    <div class="move__header">
                        <Circle class="cost-icon" />
                        <span class="move__name">{m['card.description']()}</span>
                    </div>
                    <div class="move__description">
                        {game.description || m['errors.description']()}
                    </div>
                </div>
            </div>

            <div class="card__footer">
                <div class="footer-stat">
                    <span>{m['card.romHack']()}</span>
                    {#if game.isRomHack}<Check class="icon"/>{:else}<Cross class="icon"/>{/if}
                </div>
                <div class="footer-stat">
                    <span>{m['card.includedGens']()}</span>
                    <span>{genDisplay}</span>
                </div>
                <div class="footer-stat">
                    <span>{m['card.region']()}</span>
                    <span>{game.regionName}</span>
                </div>
            </div>
        </div>

        <!-- What displays on the back of the card -->
        <div class="card-face card-back">
            <div class="card__header">
                <span class="card__name">{m['card.game_details']()}</span>
                <button class="flip-trigger" type="button" on:click={toggleFlip}>
                    <Cross />
                </button>
            </div>

            <div class="back-body">
                <div class="stats-grid">
                        <div class="stat-box">
                            <strong>{m['card.release_date']()}</strong>
                            <p>{game.releaseDate?.releaseDateEu || 'N/A'}</p>
                        </div>
                        <div class="stat-box">
                            <strong>{m['card.difficulty']()}</strong>
                            <p>{game.difficultyLevel || m['errors.no_difficulty']()}</p>
                        </div>
                        {#if game.isRomHack}
                        <div class="stat-box">
                            <strong>{m['card.has_fakemon']()}</strong>
                            <span class="status-val">
                                {#if game.hasFakemon}<Check width="14" class="pos"/>{:else}<Cross width="14" class="neg"/>{/if}
                                {game.hasFakemon ? 'Yes' : 'No'}
                            </span>
                        </div>
                            {/if}
                    <div class="stat-box">
                        <strong>{m['card.has_forms']()}</strong>
                        <span class="status-val">
                            {game.alternateForms || m['errors.none']()}
                        </span>
                    </div>
                </div>

                {#if game.isRomHack && game.qolFeatures?.length}
                    <div class="features-section">
                        <strong>{m['card.qol']()}</strong>
                        <div class="qol-container">
                            {#each game.qolFeatures as feature}
                                <span class="qol-chip">
                                    <Circle width="10" height="10" />
                                    {feature}
                                </span>
                            {/each}
                        </div>
                    </div>
                {/if}

                <div class="footer-details">
                    <div class="detail-line">
                        <strong>Region</strong>
                        <span>{game.regionName}</span>
                    </div>
                    <div class="detail-line">
                        <strong>Platform</strong>
                        <span>{game.platform}</span>
                    </div>
                    <!--{#if !game.isRomHack}-->
                    <!--    <div class="detail-line">-->
                    <!--        <strong>Release</strong>-->
                    <!--        <span>{game.releaseDate?.releaseDateEu || 'N/A'}</span>-->
                    <!--    </div>-->
                    <!--{/if}-->
                </div>

                <div class="back-placeholder">
                    <Info width="48" height="48" style="opacity: 0.1" />
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .pokemon-card {
        perspective: 1000px;
        position: relative;
        aspect-ratio: 1 / 1.6;
        min-height: 440px;
        cursor: pointer;
        background: none !important;
        border: none !important;
        padding: 0;
        outline: none;
        isolation: isolate;
    }

    .card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }

    .pokemon-card.is-flipped .card-inner {
        transform: rotateY(180deg);
    }

    .card-face {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        border-radius: 18px;
        padding: 12px;
        border: 6px solid var(--border);
        background: var(--bg);
        color: var(--text);
        display: flex;
        flex-direction: column;
        gap: 4px;
        box-sizing: border-box;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4), inset 0 0 20px rgba(0,0,0,0.1);
        overflow: hidden;
    }

    .card-back {
        transform: rotateY(180deg);
    }

    /* BACK FACE STYLES - Grid and Clean-up */
    .back-body {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding: 12px 8px;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }

    .stat-box {
        background: rgba(0, 0, 0, 0.15);
        padding: 8px;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        gap: 4px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        align-items: center;
    }

    .stat-box strong, .features-section strong, .detail-line strong {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.05rem;
        opacity: 0.8;
    }

    .status-val, .difficulty-val {
        display: flex;
        align-items: center;
        gap: 4px;
        font-weight: 800;
        font-size: 0.85rem;
    }

    .features-section {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .qol-container {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .qol-chip {
        display: flex;
        align-items: center;
        gap: 4px;
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        white-space: nowrap;
    }

    .footer-details {
        margin-top: auto;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .detail-line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.8rem;
        padding: 6px 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }

    .back-placeholder {
        display: flex;
        justify-content: center;
        padding-top: 8px;
    }

    :global(.pos) { color: #4ade80; }
    :global(.neg) { color: #f87171; }

    /* FRONT FACE DECORATIONS */
    .card-front::after, .card-back::after {
        content: '';
        position: absolute;
        inset: 0;
        z-index: 2;
        background-image: linear-gradient(125deg, transparent 35%, rgba(255, 255, 255, 0.3) 45%, rgba(255, 255, 255, 0.6) 50%, rgba(255, 255, 255, 0.3) 55%, transparent 65%);
        background-size: 300% 300%;
        background-position: 150% 0%;
        pointer-events: none;
        mix-blend-mode: color-dodge;
        transition: background-position 0.8s ease-in-out;
    }

    .pokemon-card:hover .card-face::after {
        background-position: -100% 100%;
    }

    .flip-trigger {
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 4px;
        color: inherit;
        display: flex;
        align-items: center;
        z-index: 10;
        transition: transform 0.2s ease;
    }

    .flip-trigger:hover { transform: scale(1.2); }

    /* SHARED CARD UI */
    .card__header { display: flex; justify-content: space-between; padding: 0 4px; align-items: center; z-index: 3; }
    .card__name { font-family: 'Arial Narrow', sans-serif; font-weight: 900; font-size: 1.25rem; text-transform: capitalize; text-shadow: var(--shadow); }
    .card__hp { display: flex; align-items: center; gap: 2px; color: #d32f2f; }
    .hp-label { font-size: 0.6rem; font-weight: bold; }
    .hp-value { font-size: 1.2rem; font-weight: 900; }
    .card__stage { border: 4px solid var(--border); background: #fdfdfd; box-shadow: 2px 2px 6px rgba(0,0,0,0.3), inset 0 0 10px rgba(0,0,0,0.1); overflow: hidden; min-height: 180px; display: flex; z-index: 3; }
    .illustration-container { width: 100%; aspect-ratio: 1.35 / 1; overflow: hidden; display: flex; justify-content: center; align-items: center; background: linear-gradient(45deg, #c0c0c0, #e8e8e8); }
    .illustration { width: 100%; height: 100%; object-fit: contain; background: #000; }
    .card__info-bar { background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(8px); font-size: 0.65rem; font-weight: bold; text-align: center; margin: 2px -4px; padding: 2px 0; border: 1px solid rgba(255,255,255,0.2); border-radius: 2px; color: var(--text); z-index: 3; }
    .card__body { flex: 1; display: flex; flex-direction: column; gap: 4px; padding: 4px 6px; overflow: hidden; z-index: 3; }
    .move { display: flex; flex-direction: column; gap: 1px; border-bottom: 1px solid rgba(0, 0, 0, 0.05); padding-bottom: 2px; }
    .move__header { display: flex; align-items: center; gap: 8px; }
    :global(.cost-icon) { width: 18px; height: 18px; filter: drop-shadow(1px 1px 1px rgba(0,0,0,0.2)); }
    .move__name { font-family: 'Arial Narrow', sans-serif; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 0.5px; text-shadow: var(--shadow); }
    .move__description { padding-left: 26px; font-size: 0.7rem; line-height: 1.1; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .card__footer { margin-top: auto; padding: 4px 8px; border-top: 1px solid rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.03); z-index: 3; }
    .footer-stat { display: flex; flex-direction: column; align-items: center; gap: 2px; font-size: 0.55rem; }
    .card__footer :global(svg) { width: 20px; height: 20px; filter: drop-shadow(1px 1px 1px rgba(0,0,0,0.2)); }

    @media (width >= 720px) { .pokemon-card { grid-column: span 4; } }
    @media (width >= 1020px) { .pokemon-card { grid-column: span 3; } }
</style>