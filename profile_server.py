import sys
from sync.server import Server
import logging
s = Server(logging.CRITICAL)
logger = logging.getLogger(__name__)
import cProfile

try:
    #print("Starting...")
    # run the new command using the given tracer
    cProfile.run('s.start()', 'stats.txt') 
except:
    pass

