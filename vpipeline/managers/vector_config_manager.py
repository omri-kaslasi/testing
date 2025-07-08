
import logging, datetime
from pathlib import Path
from typing import List
import tomlkit
from utils.file_loader import save_toml
from managers.sink_config_builder import SinkConfigBuilder
from utils.config import FILTER_OUT_PORT, FILTER_IN_PORT, CONF_DIR
# Ensure the logging is set up
logger = logging.getLogger(__name__)


class VectorConfigManager:
    @staticmethod
    def list_configs() -> List[Path]:
        return sorted(CONF_DIR.glob('*.toml'))

    @staticmethod
    def read_config(name: str) -> str:
        return open(CONF_DIR / name, encoding='utf-8').read()

    @staticmethod
    def write_config(name: str, doc):
        save_toml(CONF_DIR / name, doc)
        logger.info('Wrote config %s', CONF_DIR / name)


    @staticmethod
    def build_frontend(sources):
        doc = tomlkit.document()
        doc.add(tomlkit.comment('Generated ' + datetime.datetime.utcnow().isoformat()))
        src_table = tomlkit.table()
        for s in sources:
            t = tomlkit.table()
            t['type'] = 'socket'; t['mode'] = 'tcp'
            t['address'] = f'0.0.0.0:{s.frontend_port}'
            t['encoding'] = 'json'
            src_table[s.id] = t
        doc['sources'] = src_table
        sink_table = tomlkit.table()
        for s in sources:
            sk = tomlkit.table()
            sk['type'] = 'vector'; sk['address'] = f'vector-filter-{s.id.replace("_","-")}:{FILTER_IN_PORT}'
            sk['inputs'] = [s.id]
            sink_table[f'to_{s.id}'] = sk
        doc['sinks'] = sink_table
        return doc

    @staticmethod
    def build_filter(source, initiatives):
        doc = tomlkit.document()
        doc.add(tomlkit.comment(f'Filter node for {source.id.replace("_","-")}'))
        srcs = tomlkit.table()
        base = tomlkit.table()
        base['type'] = 'vector'; base['address'] = f'0.0.0.0:{FILTER_IN_PORT}'
        srcs['in'] = base
        doc['sources'] = srcs
        transforms = tomlkit.table()
        last = 'in'

        # Create parser transform
        tr = tomlkit.table()
        tr['type'] = 'remap'
        tr['inputs'] = [last]
        tr['source'] = source.parse_vrl
        key = f'{source.id}'
        transforms[key] = tr
        last = key

        for ini in initiatives:
            tr = tomlkit.table()
            tr['type'] = 'filter'
            tr['inputs'] = [last]
            tr['condition'] = ini.vrl
            key = f'{ini.id}'
            transforms[key] = tr
            last = key
        doc['transforms'] = transforms
        sinks = tomlkit.table()
        out = tomlkit.table()
        out['type'] = 'vector'; out['inputs'] = [last]; out['address'] = f'vector-sink:{FILTER_OUT_PORT}'
        sinks['out'] = out
        doc['sinks'] = sinks
        return doc

    @staticmethod
    def build_sink(destination):
        sink_doc = SinkConfigBuilder.build_from_json(destination)
        return sink_doc

    @staticmethod
    def hot_reload():
        logger.info('Vector hot-reload requested (noop)')
