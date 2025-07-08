
import logging
from pathlib import Path
from typing import Dict, List
from entities.source import Source
from utils.file_loader import load_json

DATA_DIR = Path('data/sources')

class SourceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._sources: Dict[str, Source] = {}
        self._load_all()

    def list_sources(self) -> List[Source]:
        return list(self._sources.values())

    def get_source(self, source_id: str) -> Source | None:
        return self._sources.get(source_id)

    def list_sources_rich(self):
        from rich.table import Table
        table = Table(title='Sources')
        table.add_column('ID'); table.add_column('Name'); table.add_column('Type'); table.add_column('Port')
        for s in self.list_sources():
            table.add_row(s.id, s.name, s.type, str(s.filter_port or '—'))
        return table

    # internal helpers
    def _load_all(self):
        for fp in DATA_DIR.glob('*.json'):
            self._sources[fp.stem] = Source(**load_json(fp))
        self.logger.debug('Loaded %d sources', len(self._sources))

