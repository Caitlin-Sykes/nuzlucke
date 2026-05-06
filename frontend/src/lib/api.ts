import { Configuration, GamesControllerApi } from '../generated/api';

const config = new Configuration({
    basePath: '/nuzlucke',
    // Only for dev, look into this when in production
    credentials: 'omit',
});

// Export instances so you don't have to 'new' them in every component
export const gamesApi = new GamesControllerApi(config);