import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Testing imports and versions...")

try:
    import numpy as np
    logger.info(f"NumPy version: {np.__version__}")
except ImportError as e:
    logger.error(f"Failed to import NumPy: {e}")

try:
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU usage
    import tensorflow as tf
    tf.config.set_visible_devices([], 'GPU')
    logger.info(f"TensorFlow version: {tf.__version__}")
except ImportError as e:
    logger.error(f"Failed to import TensorFlow: {e}")
