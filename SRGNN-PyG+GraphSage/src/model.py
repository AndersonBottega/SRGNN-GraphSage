# -*- coding: utf-8 -*-
"""
Created on 4/4/2019
@author: RuihongQiu
"""


import math
import torch
import torch.nn as nn
from InOutGGNN import InOutGGNN

from MeanSAGEConv import MeanSAGEConv
from MaxSAGEConv import MaxSAGEConv
from LSTMSAGEConv import LSTMSAGEConv

class Embedding2Score(nn.Module):
    def __init__(self, hidden_size):
        super(Embedding2Score, self).__init__()
        self.hidden_size = hidden_size
        self.W_1 = nn.Linear(self.hidden_size, self.hidden_size)
        self.W_2 = nn.Linear(self.hidden_size, self.hidden_size)
        self.q = nn.Linear(self.hidden_size, 1)
        self.W_3 = nn.Linear(2 * self.hidden_size, self.hidden_size)

    def forward(self, node_embedding, item_embedding_table, batch, num_count):
        sections = torch.bincount(batch)
        v_i = torch.split(node_embedding, tuple(sections.cpu().numpy()))    # split whole x back into graphs G_i
        v_n_repeat = tuple(nodes[-1].view(1, -1).repeat(nodes.shape[0], 1) for nodes in v_i)    # repeat |V|_i times for the last node embedding

        # Eq(6)
        alpha = self.q(torch.sigmoid(self.W_1(torch.cat(v_n_repeat, dim=0)) + self.W_2(node_embedding)))    # |V|_i * 1
        s_g_whole = num_count.view(-1, 1) * alpha * node_embedding    # |V|_i * hidden_size
        s_g_split = torch.split(s_g_whole, tuple(sections.cpu().numpy()))    # split whole s_g into graphs G_i
        s_g = tuple(torch.sum(embeddings, dim=0).view(1, -1) for embeddings in s_g_split)

        # Eq(7)
        v_n = tuple(nodes[-1].view(1, -1) for nodes in v_i)
        s_h = self.W_3(torch.cat((torch.cat(v_n, dim=0), torch.cat(s_g, dim=0)), dim=1))
        
        # Eq(8)
        z_i_hat = torch.mm(s_h, item_embedding_table.weight.transpose(1, 0))
        
        return z_i_hat


class GNNModel(nn.Module):
    """
    Args:
        hidden_size: the number of units in a hidden layer.
        n_node: the number of items in the whole item set for embedding layer.
    """
    def __init__(self, hidden_size, n_node, metodo):
        super(GNNModel, self).__init__()
        self.hidden_size, self.n_node = hidden_size, n_node
        self.embedding = nn.Embedding(self.n_node, self.hidden_size)

        if(metodo == 'GGNN'):
            self.gated = InOutGGNN(self.hidden_size, num_layers=1)
        elif(metodo == 'Mean'):
            self.gated = MeanSAGEConv(self.hidden_size, out_channels=self.hidden_size)
        elif(metodo == 'Max'):
            self.gated = MaxSAGEConv(self.hidden_size, out_channels=self.hidden_size)
        elif(metodo == 'LSTM'):
            self.gated = LSTMSAGEConv(self.hidden_size, out_channels=self.hidden_size)
        else:
            self.gated = InOutGGNN(self.hidden_size, num_layers=1)

        self.e2s = Embedding2Score(self.hidden_size)
        self.loss_function = nn.CrossEntropyLoss()
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1.0 / math.sqrt(self.hidden_size)
        for weight in self.parameters():
            weight.data.uniform_(-stdv, stdv)

    def forward(self, data):
        x, edge_index, batch, edge_count, in_degree_inv, out_degree_inv, sequence, num_count = \
            data.x - 1, data.edge_index, data.batch, data.edge_count, data.in_degree_inv, data.out_degree_inv,\
            data.sequence, data.num_count

        embedding = self.embedding(x).squeeze()
        hidden = self.gated(embedding, edge_index, [edge_count * in_degree_inv, edge_count * out_degree_inv])

        return self.e2s(hidden, self.embedding, batch, num_count)
