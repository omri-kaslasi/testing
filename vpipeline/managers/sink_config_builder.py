import tomlkit
import json
from pathlib import Path


class SinkConfigBuilder:
    @staticmethod
    def build_from_json(json_path: Path):
        with open(json_path, encoding='utf-8') as f:
            config = json.load(f)
        doc = tomlkit.document()
        # Add sources
        sources_table = tomlkit.table()
        for src_name, src_conf in config.get("sources", {}).items():
            t = tomlkit.table()
            for k, v in src_conf.items():
                t[k] = v
            sources_table[src_name] = t
        doc["sources"] = sources_table
        # Add sinks
        sinks_table = tomlkit.table()
        for sink_name, sink_conf in config.get("sinks", {}).items():
            t = tomlkit.table()
            for k, v in sink_conf.items():
                if isinstance(v, dict):
                    # Nested dicts (e.g., encoding)
                    for subk, subv in v.items():
                        if k == "encoding" and subk == "codec":
                            t['encoding.codec'] = subv
                        else:
                            t[f'{k}.{subk}'.replace(f'"', f'')] = subv
                else:
                    t[k] = v
            sinks_table[sink_name] = t
        doc["sinks"] = sinks_table
        return doc