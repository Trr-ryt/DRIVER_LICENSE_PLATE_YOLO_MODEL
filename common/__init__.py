import queue
import numpy as np
DATA_QUEUE_SIZE = 0  # 0 means infinite size
data_queue: queue.Queue[np.ndarray] = queue.Queue(DATA_QUEUE_SIZE)