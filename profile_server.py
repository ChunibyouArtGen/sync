import cProfile
import logging
import sys

from sync.server import Server

s = Server(logging.CRITICAL)
logger = logging.getLogger(__name__)

try:
    # print("Starting...")
    # run the new command using the given tracer
    cProfile.run("s.start()", "stats.txt")
except:
    pass
