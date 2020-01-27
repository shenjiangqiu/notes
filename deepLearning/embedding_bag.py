#%%
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
import torch.tensor as tensor
#%%
# an Embedding module containing 10 tensors of size 3  
embedding_sum = nn.EmbeddingBag(10, 3, mode='sum')  
# a batch of 2 samples of 4 indices each  
input = torch.LongTensor([0,1,2,3,4])  
print(embedding_sum.weight)
offsets = torch.LongTensor([0,4])  
out=embedding_sum(input, offsets)  
print(out)

# %%
