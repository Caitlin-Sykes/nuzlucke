<script>
    import * as m from "../generated/paraglide/messages.js";
</script>

<header>
    <div class="title-bar">
        <div class="title-group">
            <h1>{m['home.title']()}</h1>
            <span class="separator main-sep">||</span>
        </div>

        <nav class="links">
            <h2>{m['home.nav.new']()}</h2>
            <span class="separator">:</span>
            <h2>{m['home.nav.load']()}</h2>
            <span class="separator">:</span>
            <h2>{m['home.nav.settings']()}</h2>
        </nav>
    </div>
</header>

<style>
    header {
        display: flex;
        justify-content: center;
        width: 100%;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }

    .title-bar {
        background: #4ade80;
        border-radius: 0 0 25px 25px;
        height: 55px;
        padding: 0 30px;
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .title-group, .links {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Shared separator style to keep it DRY */
    .separator {
        color: white;
        font-weight: 900;
        opacity: 0.7;
        user-select: none;
    }

    .main-sep {
        font-size: 1.4rem;
        margin-left: 5px;
    }

    h1 {
        margin: 0;
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 1.7rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }

    h2 {
        margin: 0;
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        cursor: pointer;
        white-space: nowrap;
        transition: opacity 0.2s;
    }

    h2:hover {
        opacity: 0.8;
        text-decoration: underline;
        text-underline-offset: 4px;
    }
</style>