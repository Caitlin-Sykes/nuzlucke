import { paraglideVitePlugin } from '@inlang/paraglide-js'
import { defineConfig, loadEnv } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const backendBase = env.VITE_BACKEND_BASE_URL ?? 'http://localhost:8081';

  return {
    plugins: [paraglideVitePlugin({ project: './project.inlang', outdir: './src/generated/paraglide' }),svelte()],
    envDir: '../',
    server: {
      proxy: {
        '/nuzlucke': {
          target: backendBase,
          changeOrigin: true,
          secure: false
        }
      }
    }
  };
});