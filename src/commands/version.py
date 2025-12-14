from src.modules import *

class CommandManifest:
    NAME = 'version'
    DESCRIPTION = 'Returns the current Git commit hash.'
    ARGS = []
    FLAGS = []

    @staticmethod
    def execute(args=None, flags=None, stdin=None):
        message = env.getCommitHash()
        return message