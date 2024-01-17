import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt

datos, metadatos = tfds.load('fashion_mnist', as_supervised=True, with_info=True)
