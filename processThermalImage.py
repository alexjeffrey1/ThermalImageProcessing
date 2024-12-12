

# import os
# from zipfile import ZipFile
# import shutil
# from struct import unpack
# from otherfunctions import *
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.ndimage.filters import gaussian_filter
# from mpl_toolkits.axes_grid1 import make_axes_locatable

# from unitconversion import *
# from scipy import ndimage


import readis2 #.read_is2_new as readis2

filename='data\\test_data\\IR_00002.IS2'

data = readis2.read_is2_new(filename)

readis2.plot_ir(data)

print('complete')