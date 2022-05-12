# SRGNN-GraphSage
Adaptação do método SR-GNN com a técnica GraphSage. 
Neste trabalho é realizado a adaptação do método SR-GNN com a técnica GraphSage, também utilizamos diferentes agregadores: Mean, Max e LSTM.
Este algoritmo é utilizado na dissertação: Sistemas de Recomendação Sequencial Baseados em Abordagens de Graph Neural Network. Desenvolvida na Universidade Federal do Paraná (UFPR). (A dissertação será disponibilizada após a finalização do mestrado).

Referências para o desenvolvimento deste algoritmo:
SR-GNN: Session-based Recommendation with Graph Neural Networks.
Wu, S., Tang, Y., Zhu, Y., Wang, L., Xie, X. e Tan, T. (2019). Session-based recommendation with graph neural networks. Proceedings of the AAAI Conference on Artificial Intelligence, 33(01):346–353.
Algritmo original disponível em: https://github.com/CRIPAC-DIG/SR-GNN
Algoritmo utilizado como base para este trabalho disponível em: https://github.com/lfywork/SRGNN_PyG

GraphSage: Inductive representation learning on large graphs.
Hamilton, W. L., Ying, R. e Leskovec, J. (2017). Inductive representation learning on large graphs. Em Proceedings of the 31st International Conference on Neural Information Processing Systems, página 1025–1035, Red Hook - USA.

A teoria dos agregadores e os agregadores originais estão disponíveis no trabalho do GraphSage.
Agoritmos base para os agregadores: Mean, Max e LSTM.
Algoritmo base para o agregador Mean disponível em: https://pytorch-geometric.readthedocs.io/en/latest/_modules/torch_geometric/nn/conv/sage_conv.html
Algoritmo base para o agregador Max disponível em: https://towardsdatascience.com/hands-on-graph-neural-networks-withpytorch-pytorch-geometric-359487e221a8
Algoritmo base para o agregador LSTM disponível em: https://pytorch.org/tutorials/beginner/nlp/sequence_models_tutorial.html

O método GGNN disponível neste algoritmo é o método original do SR-GNN, que foi mantido para comparação com os demais agregadores.
