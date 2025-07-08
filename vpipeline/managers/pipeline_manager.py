
import logging
from managers.source_manager import SourceManager
from managers.initiative_manager import InitiativeManager
from managers.vector_config_manager import VectorConfigManager
from pathlib import Path

class PipelineManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.source_mgr = SourceManager()
        self.initiative_mgr = InitiativeManager(self.source_mgr)

    def sync_pipeline(self):
        self.logger.info('Sync pipeline')
        self._rebuild_configs()
        VectorConfigManager.hot_reload()

    def apply_initiative(self, initiative_id, source_id):
        src = self.source_mgr.get_source(source_id)
        if not src:
            self.logger.error('Source not found'); return
        ini = next((i for i in self.initiative_mgr.list_initiatives() if i.id == initiative_id), None)
        if not ini:
            self.logger.error('Initiative not found'); return
        rel = self.initiative_mgr.get_relevant(src.id) + [ini]
        filter_doc = VectorConfigManager.build_filter(src, rel)
        VectorConfigManager.write_config(f'filter-{src.id.replace("_","-")}.toml', filter_doc)
        VectorConfigManager.hot_reload()

    def _rebuild_configs(self):
        frontend = VectorConfigManager.build_frontend(self.source_mgr.list_sources())
        VectorConfigManager.write_config('frontend.toml', frontend)
        for src in self.source_mgr.list_sources():
            rel = self.initiative_mgr.get_relevant(src.id)
            fdoc = VectorConfigManager.build_filter(src, rel)
            VectorConfigManager.write_config(f'filter-{src.id.replace("_","-")}.toml', fdoc)
        sink = VectorConfigManager.build_sink(Path("data/sinks/splunk_console.json"))
        VectorConfigManager.write_config('sink.toml', sink)
