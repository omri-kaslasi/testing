
import logging
from logging.config import dictConfig
from utils.config import LOG_FILE
LOG_FILE.parent.mkdir(exist_ok=True)

class LoggerManager:
    @staticmethod
    def init_logging(level: str = 'INFO'):
        dictConfig({
            'version': 1,
            'formatters': {
                'json': {
                    '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                    'fmt': '%(asctime)s %(levelname)s %(name)s %(message)s',
                }
            },
            'handlers': {
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': str(LOG_FILE),
                    'formatter': 'json',
                    'level': level,
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'json',
                    'level': level,
                },
            },
            'root': {'handlers': ['file', 'console'], 'level': level},
        })
