export type GamesDto = {
  name: string;
  creator: string;
  platform: string;
  generationsIncluded: number[];
  isRomHack: boolean;
  releaseDate: {
    releaseDateEu: string | null;
    releaseDateJp: string | null;
    releaseDateAu: string | null;
    releaseDateUs: string | null;
  };
  credits: {
    imageCredits: string | null;
    imageRights: string | null;
    imageUrl: string | null;
  };
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