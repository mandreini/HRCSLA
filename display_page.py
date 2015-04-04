"""
Created on July, 2014
@author: ma56nin9 / Matt
Contact: ma56nin@hotmail.com
"""

import web
from sites import *

web.config.debug = True

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
