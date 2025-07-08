import jmespath
import logging
from pathlib import Path
from typing import Dict, List
from entities.initiative import OptimizationInitiative
from utils.file_loader import load_json
from rich.table import Table
from utils.config import DATA_DIR

class InitiativeManager:
    def __init__(self, source_mgr):
        self.logger = logging.getLogger(__name__)
        self._source_mgr = source_mgr
        self._initiatives: Dict[str, OptimizationInitiative] = {}
        self._load_all()

    def list_initiatives(self) -> List[OptimizationInitiative]:
        return list(self._initiatives.values())

    def get_relevant(self, source_id: str | None = None) -> List[OptimizationInitiative]:
        sources = [self._source_mgr.get_source(source_id)] if source_id else self._source_mgr.list_sources()
        rel = []
        for ini in self.list_initiatives():
            src = next((s for s in sources if s and s.id == ini.data_source), None)
            if src and self._is_relevant(ini, src):
                rel.append(ini)
        return rel

    def get_implemented(self, source_id: str) -> List[OptimizationInitiative]:
        return []

    def rich_table(self, initiatives: List[OptimizationInitiative]):
        t = Table(title=f'Initiatives ({len(initiatives)})')
        t.add_column('ID'); t.add_column('Name'); t.add_column('Source')
        for i in initiatives:
            t.add_row(i.id, i.name, i.data_source)
        return t

    def _is_relevant(self, ini: OptimizationInitiative, src):
        try:
            return bool(jmespath.search(ini.relevancy_rule, src.model_dump()))
        except Exception as exc:
            self.logger.warning('Bad relevancy rule in %s: %s', ini.id, exc)
            return False

    def _load_all(self):
        self.logger.debug('Loaded %d initiatives', len(self._initiatives))
        for fp in DATA_DIR.glob('*.json'):
            ini = OptimizationInitiative(**load_json(fp))
            self._initiatives[ini.id] = ini
