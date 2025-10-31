from modules.networks import ipc_send
import json

class NetworkLogSender:
    def __init__(self, port):
        self.host = "127.0.0.1"
        self.port = port

    def critical(self, message,tags=None):
        if tags is None:
            tags = {}
        log_template = {
            "level": "CRITICAL",
            "content": message,
            "tags": tags
        }
        msg = json.dumps(log_template)
        ipc_send(msg, self.host, self.port)

    def error(self, message,tags=None):
        if tags is None:
            tags = {}
        log_template = {
            "level": "ERROR",
            "content": message,
            "tags": tags
        }
        msg = json.dumps(log_template)
        ipc_send(msg, self.host, self.port)

    def warning(self, message,tags=None):
        if tags is None:
            tags = {}
        log_template = {
            "level": "WARNING",
            "content": message,
            "tags": tags
        }
        msg = json.dumps(log_template)
        ipc_send(msg, self.host, self.port)

    def info(self, message,tags=None):
        if tags is None:
            tags = {}
        log_template = {
            "level": "INFO",
            "content": message,
            "tags": tags
        }
        msg = json.dumps(log_template)
        ipc_send(msg, self.host, self.port)

    def debug(self, message,tags=None):
        if tags is None:
            tags = {}
        log_template = {
            "level": "DEBUG",
            "content": message,
            "tags": tags
        }
        msg = json.dumps(log_template)
        ipc_send(msg, self.host, self.port)