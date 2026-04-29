export type GamesDto = {
  name: string;
  platform: string;
  generationsIncluded: number[];
  rulesetId: number;
  isRomHack: boolean;
  releaseDate: {
    releaseDateEu: string | null;
    releaseDateJp: string | null;
    releaseDateAu: string | null;
    releaseDateUs: string | null;
  };
  credits: {
    gameRights: string | null;
    gameCreator: string | null;
  };
  illustration: {
    imageUrl: string | null;
    imageAuthor: string | null;
    imageRights: string | null;
    imageSource: string | null;
  };
  regionName: string;
  description: string;
  isRomHackOf: string;
  hasFakemon: boolean;
  difficultyLevel: string;
  alternateForms: string;
  qolFeatures: string[];


};

const API_BASE = '/nuzlucke';
export async function getAvailableGames(): Promise<GamesDto[]> {
  const res = await fetch(`${API_BASE}/games/available`, {
    headers: { Accept: 'application/json' }
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Failed to load games (${res.status})${text ? `: ${text}` : ''}`);
  }

  return (await res.json()) as GamesDto[];
}