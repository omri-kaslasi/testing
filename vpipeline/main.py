# main.py
import logging
from managers.logger_manager import LoggerManager

LoggerManager.init_logging()


from managers.pipeline_manager import PipelineManager
from cli.shell import VPShell


# 3) interactive loop (cmd2 handles argv automatically)
#    - If you pass args → runs as a one-shot CLI.
#    - If you pass nothing → starts the REPL.
if __name__ == "__main__":
    # 1) logging
    logger = logging.getLogger(__name__)
    logger.info("Starting vpipeline...")

    # 2) bootstrap once
    _pipeline = PipelineManager()
    _pipeline.sync_pipeline()

    VPShell().cmdloop()
