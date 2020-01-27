
# %%
import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils


class TestDataSet(Dataset):
    def __init__(self):
        pass

    def __len__(self):
        return 4

    def __getitem__(self, idx):
        return idx

mydata=TestDataSet()
print(mydata[1])



# %%
a=np.array([[1,2],[3,4],[5,6]])
print(a)
print(a-1)

print(a-[[1],[2],[3]])


# %%
