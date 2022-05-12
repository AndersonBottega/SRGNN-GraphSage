'''
Implementação adaptada deste site:
https://github.com/dmlc/dgl/blob/master/python/dgl/nn/pytorch/conv/sageconv.py
'''
import numpy as np
import torch
from torch.nn import Sequential as Seq, Linear, ReLU
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import remove_self_loops, add_self_loops

from typing import Union, Tuple
from torch_geometric.typing import OptPairTensor, Adj, Size

from torch import Tensor
import torch.nn.functional as F
from torch_sparse import SparseTensor, matmul
from torch_geometric.nn.dense.linear import Linear

class LSTMSAGEConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super(LSTMSAGEConv, self).__init__()
        self.lstm = torch.nn.LSTM(in_channels, out_channels, batch_first=True)
        self.update_lstm = torch.nn.LSTM(in_channels + out_channels, in_channels, bias=False)

    def forward(self, x: Union[Tensor, OptPairTensor], edge_index: Adj,
                size: Size = None) -> Tensor:
        #print("x: ", x)
        # x has shape [N, in_channels]
        # edge_index has shape [2, E]

        edge_index, _ = remove_self_loops(edge_index)
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))

        return self.propagate(edge_index, size=(x.size(0), x.size(0)), x=x)

    #def message(self, x_j):
    def message(self, x_j: Tensor) -> Tensor:
        # x_j has shape [E, in_channels]
        #print("x_j: ", x_j)
        #for a in x_j:
        #    print("a", a)
        x_j = x_j.unsqueeze(1)
        inputs = [a for a in x_j]
        #print("inputs: ", inputs)
        #print("x_j.size: ", x_j.size())
        x_j, hidden = self.lstm(x_j)
        x_j = x_j.squeeze(1)
        #print("x_j self.lstm: ", x_j)
        #print("hidden: ", hidden)

        return x_j

    def update(self, aggr_out, x):
        # aggr_out has shape [N, out_channels]
        #print(aggr_out)
        #print(x)
        aggr_out = aggr_out.squeeze(0)
        #print("aggr_out: ", aggr_out)
        new_embedding = torch.cat([aggr_out, x], dim=1)
        #print("new_embedding concat", new_embedding)
        new_embedding = new_embedding.unsqueeze(1)
        #print("new_embedding un", new_embedding)
        new_embedding, hiddem = self.update_lstm(new_embedding)
        #print("new_embedding up: ", new_embedding)

        return new_embedding.squeeze(1)

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.in_channels,
                                   self.out_channels)
