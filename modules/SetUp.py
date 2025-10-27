import os
from BasicSystem import LogSystem

@LogSystem.logger.catch()
def make_directory():
    if not os.path.exists("./logs"):
        LogSystem.logger.debug("Creating logs directory")
        os.makedirs("./logs")
    if not os.path.exists("./dumps"):
        LogSystem.logger.debug("Creating dumps directory")
        os.mkdir("./dumps")

def basic_setup():
    LogSystem.logger.debug("Setting up basic file structure")
    make_directory()