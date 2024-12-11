import numpy as np
from divtools.graph.hexbin_graph import draw_hexbin

import logging
logger= logging.getLogger(__name__)



x = "x"
y = 'y'

data = np.random.random((2000, 2))
data = data.tolist()
draw_hexbin(x, y, data)

