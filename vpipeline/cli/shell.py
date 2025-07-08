# cli/shell.py
from __future__ import annotations
import cmd2
from cmd2 import Cmd, with_argparser
import argparse
from rich import print as rprint

from managers.pipeline_manager import PipelineManager
from managers.vector_config_manager import VectorConfigManager

# single shared orchestrator
_pipeline = PipelineManager()


class VPShell(Cmd):
    """Interactive shell for vpipeline."""
    prompt = "vpipeline> "
    intro = "Welcome to vpipeline!  Type ? or help to list commands."

    # ------------------------------------------------------------------ #
    #  sync  ------------------------------------------------------------ #
    sync_parser = argparse.ArgumentParser()
    @with_argparser(sync_parser)
    def do_sync(self, _):
        """Scan for new sources, rebuild configs, hot-reload Vector."""
        _pipeline.sync_pipeline()
        self.poutput("[green]Pipeline synced[/]")

    # ------------------------------------------------------------------ #
    #  sources group ---------------------------------------------------- #
    sources_parser = argparse.ArgumentParser()
    sources_sub = sources_parser.add_subparsers(dest="action", required=True)

    src_list = sources_sub.add_parser("list")
    src_show = sources_sub.add_parser("show")
    src_show.add_argument("source_id")

    @with_argparser(sources_parser)
    def do_sources(self, args):
        """sources list | sources show <id>"""
        if args.action == "list":
            rprint(_pipeline.source_mgr.list_sources_rich())
        elif args.action == "show":
            src = _pipeline.source_mgr.get_source(args.source_id)
            if src:
                rprint(src.model_dump_json(indent=2))
            else:
                self.perror(f"Source '{args.source_id}' not found")

    # ------------------------------------------------------------------ #
    #  initiatives group ------------------------------------------------ #
    ini_parser = argparse.ArgumentParser()
    ini_sub = ini_parser.add_subparsers(dest="action", required=True)

    ini_rel = ini_sub.add_parser("relevant")
    ini_rel.add_argument("--source", dest="source_id")

    ini_impl = ini_sub.add_parser("implemented")
    ini_impl.add_argument("source_id")

    ini_apply = ini_sub.add_parser("apply")
    ini_apply.add_argument("initiative_id")
    ini_apply.add_argument("source_id")

    @with_argparser(ini_parser)
    def do_initiatives(self, args):
        """initiatives relevant|implemented|apply …"""
        if args.action == "relevant":
            rel = _pipeline.initiative_mgr.get_relevant(args.source_id)
            rprint(_pipeline.initiative_mgr.rich_table(rel))

        elif args.action == "implemented":
            impl = _pipeline.initiative_mgr.get_implemented(args.source_id)
            rprint(_pipeline.initiative_mgr.rich_table(impl))

        elif args.action == "apply":
            _pipeline.apply_initiative(args.initiative_id, args.source_id)

    # ------------------------------------------------------------------ #
    #  configs group ---------------------------------------------------- #
    cfg_parser = argparse.ArgumentParser()
    cfg_sub = cfg_parser.add_subparsers(dest="action", required=True)

    cfg_list = cfg_sub.add_parser("list")
    cfg_show = cfg_sub.add_parser("show")
    cfg_show.add_argument("name")

    @with_argparser(cfg_parser)
    def do_configs(self, args):
        """configs list | configs show <name>"""
        if args.action == "list":
            for p in VectorConfigManager.list_configs():
                self.poutput(p)
        elif args.action == "show":
            try:
                txt = VectorConfigManager.read_config(args.name)
                self.poutput(txt)
            except FileNotFoundError:
                self.perror(f"Config '{args.name}' not found")

    # ------------------------------------------------------------------ #
    #  allow shell-style ! commands (optional)
    def default(self, line):
        """Unknown command → try OS shell."""
        return self.do_shell(line)
