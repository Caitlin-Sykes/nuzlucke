import logging
import os
import re


class Loaders:
    """Class for loading data from files."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_base_moves(self, filepath):
        """Extracts starting moves from a Pokémon's base stats .asm file.
        :param filepath: Path to the base stats file.
        :return: List of starting moves
        """
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    # we want the learn set and the line that has db
                    if 'db' in line and 'level 1 learnset' in line:
                        # strip comments from it
                        data_part = line.split(';')[0]
                        # remove db
                        moves_raw = data_part.replace('db', '').strip()
                        # we split by commas
                        moves = [m.strip().lower().replace('_', '-') for m in moves_raw.split(',')]
                        # we ignore if there is no move
                        return [m for m in moves if m != 'no-move' and m != '']
        except Exception as e:
            self.logger.error(f"Error reading base moves from {filepath}: {e}")
        return []

    
    def load_all_base_stats(self, base_stats_dir):
        """Loads all base stats from a folder.
         :param base_stats_dir: Path to the folder containing base stats files.
         :return: Dictionary of base stats data."""
        base_db = {}
    
        # for every asm file in the base_stats_folder
        for file in os.listdir(base_stats_dir):
            if file.endswith('.asm'):
                species = file.replace('.asm', '').upper()
                moves = self.load_base_moves(os.path.join(base_stats_dir, file))
                base_db[species] = moves
    
                # Alias for Nidoran (NIDORANM -> NIDORAN_M)
                if 'NIDORAN' in species:
                    alias = species.replace('NIDORANM', 'NIDORAN_M').replace('NIDORANF', 'NIDORAN_F')
                    base_db[alias] = moves
    
        print(f"Successfully loaded {len(base_db)} Pokemon move sets.")
        return base_db


    def load_moves(self, filepath):
        """
      Loads moves data from a file.
      :param filepath: Path to the moves file.
      :return: Dictionary of moves data.
      """
        db = {}
    
        with open(filepath, 'r') as f:
            content = f.read()
        blocks = re.split(r'(\w+)EvosMoves:', content)
        for i in range(1, len(blocks), 2):
            species = blocks[i].strip().upper()
            data = blocks[i + 1]
            db[species] = []
            sections = data.split('db 0', 1)
            if len(sections) < 2: continue
            matches = re.findall(r'db\s+(\d+)\s*,\s*([A-Z0-9_]+)', sections[1])
            for level, move in matches:
                db[species].append((int(level), move.lower().replace('_', '-')))
        return db

    def load_trainer_constants(self, filepath):
        """Maps trainer IDs to Data labels (e.g., 1 -> YoungsterData).
        :param filepath: Path to the trainer constants file.
        :return: Dictionary of trainer IDs to Data labels.
        """
        id_map = {}
        current_id = 0
        if not os.path.exists(filepath): return id_map
        with open(filepath, 'r') as f:
            for line in f:
                match = re.search(r'trainer_const\s+([A-Z0-9_]+)', line)
                if match:
                    name = match.group(1)
                    formatted = "".join([p.capitalize() for p in name.split('_')]) + "Data"
                    id_map[current_id] = formatted
                    current_id += 1
        return id_map
    
    