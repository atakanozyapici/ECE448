# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
"""
This is the main entry point for MP6. You should only modify code
within this file and neuralnet_part1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network

        @param lrate: The learning rate for the model.
        @param loss_fn: A loss function defined in the following way:
            @param yhat - an (N,out_size) tensor
            @param y - an (N,) tensor
            @return l(x,y) an () tensor that is the mean loss
        @param in_size: Dimension of input
        @param out_size: Dimension of output

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size
        We recommend setting the lrate to 0.01 for part 1

        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        # self.conv1 = nn.Conv2d(3, 6, 5)
        # self.pool = nn.MaxPool2d(2, 2)
        # self.conv2 = nn.Conv2d(6, 16, 5)
        # self.fc1 = nn.Linear(16 * 5 * 5, 120)
        # self.fc2 = nn.Linear(120, 84)
        # self.fc3 = nn.Linear(84, 10)
        self.features = nn.Sequential(
            nn.Conv2d(3,6,5),
            nn.ReLU(inplace = True),
            nn.MaxPool2d(2,2),
            nn.Conv2d(6,16,5),
            nn.ReLU(inplace = True),
            nn.MaxPool2d(2,2)
        )
        self.classifier = nn.Sequential(
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU(inplace = True),
            nn.Linear(120, 84),
            nn.ReLU(inplace = True),
            nn.Linear(84, 2)
        )

        self.lrate = lrate




    def forward(self, x):
        """ A forward pass of your neural net (evaluates f(x)).

        @param x: an (N, in_size) torch tensor

        @return y: an (N, out_size) torch tensor of output from the network
        """
        x = x.view(-1,3,32,32)
        x = self.features(x)
        x = x.view(-1, 16 * 5 * 5)     
        x = self.classifier(x)
        return x

    def step(self, x, y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """


        ###
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(self.parameters(), lr=self.lrate, momentum=1)
        # running_loss = 0.0
        # print(x.size())
        # optimizer.zero_grad()
        output = self.forward(x)
        # print(y)
        loss = self.loss_fn(output, y)
        loss.backward()
        optimizer.step()
        # print(output)
        # running_loss += loss.item()
        #
        #
        # for i in range(len(x)):
        #     data = x[i]
        #     label = y[i:i+1]
        #     # print(data)
        #     # print(label)
        #
        #     optimizer.zero_grad()
        #
        #     # input = torch.randn(3, 5, requires_grad=True)
        #     # print(input)
        #     # target = torch.empty(3, dtype=torch.long).random_(5)
        #     # print(target)
        #     # loss = self.loss_fn(input, target)
        #     # print(loss)
        #
        #     print(data.size())
        #     output = self.forward(data)
        #     print(output)
        #     print(label)
        #     loss = self.loss_fn(output, label)
        #     loss.backward()
        #     optimizer.step()
        #     running_loss += loss.item()
        # print(loss.detach().cpu().numpy())
        # print(loss)
        return loss.item()


def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of iterations of training
    @param batch_size: The size of each batch to train on. (default 100)

    # return all of these:

    @return losses: Array of total loss at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: A NeuralNet object

    # NOTE: This must work for arbitrary M and N
    """
    # find out how to get in_size, out_size
    net = NeuralNet(0.001, nn.CrossEntropyLoss(), train_set.size()[1], 2)
    loss_array = np.zeros(n_iter)
    means = train_set.mean(dim=1, keepdim=True)
    stds = train_set.std(dim=1, keepdim=True)
    train_set = (train_set - means) / stds
    for i in range(n_iter):
        # print(i)
        ind = (i*batch_size) % train_set.size()[0]
        loss_array[i] = net.step(train_set[ind: ind+batch_size],train_labels[ind: ind+batch_size])

    yhats = np.zeros(len(dev_set))
    means = dev_set.mean(dim=1, keepdim=True)
    stds = dev_set.std(dim=1, keepdim=True)
    dev_set = (dev_set - means) / stds
    for ind in range(len(dev_set)):
        # print(dev_set[i])
        temp_val = net(dev_set[ind])

        if(temp_val[1] >= temp_val[0]):
            val = 1
        else:
            val = 0
        yhats[ind] =val

    return loss_array,yhats,net
