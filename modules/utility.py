import os


def get_cpu_count():
    return int(os.cpu_count())