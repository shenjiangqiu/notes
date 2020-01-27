# learn pytorch
## learn data_loader
1. define a dataset class, define ```__len__(self)```  and ```__getitem__(self,index)``` function.
2. define a ```dataloader(dataset,batchsize)```
3. using ```enumerate(dataload)``` to get a batch of data ,shape:```(batchsize,data_real_shape)```
   
## embedding bags:
class EmbeddingBag(num_embeddings, embedding_dim, max_norm=None, norm_type=2., scale_grad_by_freq=False, mode='mean', sparse=False, _weight=None)
Computes sums or means of 'bags' of embeddings, without instantiating the intermediate embeddings.

For bags of constant length and no :attr:per_sample_weights, this class

    * with `mode="sum"` is equivalent to :class:`~torch.nn.Embedding` followed by `torch.sum(dim=0)`,  
    * with `mode="mean"` is equivalent to :class:`~torch.nn.Embedding` followed by `torch.mean(dim=0)`,  
    * with `mode="max"` is equivalent to :class:`~torch.nn.Embedding` followed by `torch.max(dim=0)`.  
However, :class:~torch.nn.EmbeddingBag is much more time and memory efficient than using a chain of these operations.

EmbeddingBag also supports per-sample weights as an argument to the forward pass. This scales the output of the Embedding before performing a weighted reduction as specified by mode. If :attr:per_sample_weights is passed, the only supported mode is "sum", which computes a weighted sum according to :attr:per_sample_weights.

Args:

    num_embeddings (int): size of the dictionary of embeddings  
    embedding_dim (int): the size of each embedding vector  
    max_norm (float, optional): If given, each embedding vector with norm larger than :attr:`max_norm`  
                                is renormalized to have norm :attr:`max_norm`.  
    norm_type (float, optional): The p of the p-norm to compute for the :attr:`max_norm` option. Default `2`.  
    scale_grad_by_freq (boolean, optional): if given, this will scale gradients by the inverse of frequency of  
                                            the words in the mini-batch. Default `False`.  
                                            Note: this option is not supported when `mode="max"`.  
    mode (string, optional): `"sum"`, `"mean"` or `"max"`. Specifies the way to reduce the bag.  
                             `"sum"` computes the weighted sum, taking :attr:`per_sample_weights`  
                             into consideration. `"mean"` computes the average of the values  
                             in the bag, `"max"` computes the max value over each bag.  
                             Default: `"mean"`  
    sparse (bool, optional): if `True`, gradient w.r.t. :attr:`weight` matrix will be a sparse tensor. See  
                             Notes for more details regarding sparse gradients. Note: this option is not  
                             supported when `mode="max"`.  
Attributes:

    weight (Tensor): the learnable weights of the module of shape `(num_embeddings, embedding_dim)`  
                     initialized from :math:`\mathcal{N}(0, 1)`.  
Inputs: :attr:input (LongTensor), :attr:offsets (LongTensor, optional), and

    :attr:`per_index_weights` (Tensor, optional)  

    - If :attr:`input` is 2D of shape `(B, N)`,  

      it will be treated as `B` bags (sequences) each of fixed length `N`, and  
      this will return `B` values aggregated in a way depending on the :attr:`mode`.  
      :attr:`offsets` is ignored and required to be `None` in this case.  

    - If :attr:`input` is 1D of shape `(N)`,  

      it will be treated as a concatenation of multiple bags (sequences).  
      :attr:`offsets` is required to be a 1D tensor containing the  
      starting index positions of each bag in :attr:`input`. Therefore,  
      for :attr:`offsets` of shape `(B)`, :attr:`input` will be viewed as  
      having `B` bags. Empty bags (i.e., having 0-length) will have  
      returned vectors filled by zeros.  

    per_sample_weights (Tensor, optional): a tensor of float / double weights, or None  
        to indicate all weights should be taken to be `1`. If specified, :attr:`per_sample_weights`  
        must have exactly the same shape as input and is treated as having the same  
        :attr:`offsets`, if those are not `None`. Only supported for `mode='sum'`.  
Output shape: (B, embedding_dim)

Examples:

        # an Embedding module containing 10 tensors of size 3  
        embedding_sum = nn.EmbeddingBag(10, 3, mode='sum')  
        # a batch of 2 samples of 4 indices each  
        input = torch.LongTensor([1,2,4,5,4,3,2,9])  
        offsets = torch.LongTensor([0,4])  
        embedding_sum(input, offsets)  
    tensor([[-0.8861, -5.4350, -0.0523],  
            [ 1.1306, -2.5798, -1.0044]])  
