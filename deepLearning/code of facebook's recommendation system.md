# code of facebook's system
## generate_random_data
input data structure:
```python
return (  
nbatches,#int(np.ceil((data_size * 1.0) / mini_batch_size))  
lX,#list of Xt  
lS_offsets,#list of lS_emb_offsets  
lS_indices,#list of lS_emb_indices  
lT,#list of P  
)
```
```python
def generate_uniform_input_batch(
    m_den,
    ln_emb,
    n,
    num_indices_per_lookup,
    num_indices_per_lookup_fixed,
):
    # dense feature
    Xt = torch.tensor(ra.rand(n, m_den).astype(np.float32))

    # sparse feature (sparse indices)
    lS_emb_offsets = []
    lS_emb_indices = []
    # for each embedding generate a list of n lookups,
    # where each lookup is composed of multiple sparse indices
    for size in ln_emb:
        lS_batch_offsets = []
        lS_batch_indices = []
        offset = 0
        for _ in range(n):
            # num of sparse indices to be used per embedding (between
            if num_indices_per_lookup_fixed:
                sparse_group_size = np.int64(num_indices_per_lookup)
            else:
                # random between [1,num_indices_per_lookup])
                r = ra.random(1)
                sparse_group_size = np.int64(
                    np.round(max([1.0], r * min(size, num_indices_per_lookup)))
                )
            # sparse indices to be used per embedding
            r = ra.random(sparse_group_size)
            sparse_group = np.unique(np.round(r * (size - 1)).astype(np.int64))
            # reset sparse_group_size in case some index duplicates were removed
            sparse_group_size = np.int64(sparse_group.size)
            # store lengths and indices
            lS_batch_offsets += [offset]
            lS_batch_indices += sparse_group.tolist()
            # update offset for next iteration
            offset += sparse_group_size
        lS_emb_offsets.append(torch.tensor(lS_batch_offsets))
        lS_emb_indices.append(torch.tensor(lS_batch_indices))

    return (Xt, lS_emb_offsets, lS_emb_indices)
```
get item
```python
    def __getitem__(self, index):

        if isinstance(index, slice):
            return [
                self[idx] for idx in range(
                    index.start or 0, index.stop or len(self), index.step or 1
                )
            ]

        # WARNING: reset seed on access to first element
        # (e.g. if same random samples needed across epochs)
        if self.reset_seed_on_access and index == 0:
            self.reset_numpy_seed(self.rand_seed)

        # number of data points in a batch
        n = min(self.mini_batch_size, self.data_size - (index * self.mini_batch_size))

        # generate a batch of dense and sparse features
        if self.data_generation == "random":
            (X, lS_o, lS_i) = generate_uniform_input_batch(
                self.m_den,
                self.ln_emb,
                n,
                self.num_indices_per_lookup,
                self.num_indices_per_lookup_fixed
            )
        elif self.data_generation == "synthetic":
            (X, lS_o, lS_i) = generate_synthetic_input_batch(
                self.m_den,
                self.ln_emb,
                n,
                self.num_indices_per_lookup,
                self.num_indices_per_lookup_fixed,
                self.trace_file,
                self.enable_padding
            )
        else:
            sys.exit(
                "ERROR: --data-generation=" + self.data_generation + " is not supported"
            )

        # generate a batch of target (probability of a click)
        T = generate_random_output_batch(n, self.num_targets, self.round_targets)

        return (X, lS_o, lS_i, T)
```
get random data
```python
def generate_uniform_input_batch(
    m_den,
    ln_emb,
    n,
    num_indices_per_lookup,
    num_indices_per_lookup_fixed,
):
    # dense feature
    Xt = torch.tensor(ra.rand(n, m_den).astype(np.float32))# 2*4 size

    # sparse feature (sparse indices)
    lS_emb_offsets = []
    lS_emb_indices = []
    # for each embedding generate a list of n lookups,
    # where each lookup is composed of multiple sparse indices
    for size in ln_emb:# 4,3,2
        lS_batch_offsets = []
        lS_batch_indices = []
        offset = 0
        for _ in range(n):# 2
            # num of sparse indices to be used per embedding (between
            if num_indices_per_lookup_fixed:
                sparse_group_size = np.int64(num_indices_per_lookup)
            else:
                # random between [1,num_indices_per_lookup])
                r = ra.random(1)
                sparse_group_size = np.int64(
                    np.round(max([1.0], r * min(size, num_indices_per_lookup)))
                )
            # sparse indices to be used per embedding
            r = ra.random(sparse_group_size)
            sparse_group = np.unique(np.round(r * (size - 1)).astype(np.int64))
            # reset sparse_group_size in case some index duplicates were removed
            sparse_group_size = np.int64(sparse_group.size)
            # store lengths and indices
            lS_batch_offsets += [offset]
            lS_batch_indices += sparse_group.tolist()
            # update offset for next iteration
            offset += sparse_group_size
        lS_emb_offsets.append(torch.tensor(lS_batch_offsets))
        lS_emb_indices.append(torch.tensor(lS_batch_indices))

    return (Xt, lS_emb_offsets, lS_emb_indices)
```