import numpy as np
from numba import cuda
import Constants as const
import Dm3Reader3 as dm3
import ImageSupport as imsup
import GUI as gui

cuda.select_device(0)
dev = cuda.get_current_device()
print('CUDA device in use: ' + dev.name.decode())

# Reading dm3 image files

imgList = imsup.ImageList()
idxInFocus = const.numInFocus - 1
idxTemp = const.numInFocus

for idx in range(0, const.nFiles):
    fPath = const.inputDir + const.serName + str(idx+1) + '.dm3'
    print('Reading file "' + fPath + '"')
    imgData = dm3.ReadDm3File(fPath)
    imgMatrix = imsup.PrepareImageMatrix(imgData, const.dimSize)
    img = imsup.ImageWithBuffer(const.dimSize, const.dimSize, imsup.Image.cmp['CAP'], imsup.Image.mem['CPU'])
    img.LoadAmpData(np.sqrt(imgMatrix).astype(np.float32))
    img.numInSeries = idx + 1
    imgList.append(img)

imgList.UpdateLinks()

gui.RunEwrWindow(imgList[0], const.gridDim)