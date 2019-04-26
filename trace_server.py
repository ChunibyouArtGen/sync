import logging
import sys
import trace

from sync.server import Server

s = Server(logging.CRITICAL)
logger = logging.getLogger(__name__)


# create a Trace object, telling it what to ignore, and whether to
# do tracing or line-counting or both.
tracer = trace.Trace(
    ignoredirs=[sys.prefix, sys.exec_prefix],
    trace=0,
    count=0,
    countfuncs=1,
    countcallers=1,
    timing=True,
)
try:
    # print("Starting...")
    # run the new command using the given tracer
    tracer.run("s.start()")
except:
    pass
# make a report, placing output in the current directory
r = tracer.results()
r.write_results(show_missing=True, summary=True, coverdir="./coverage")
# import ipdb; ipdb.set_trace()
