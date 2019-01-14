import sys 
sys.path.append('../')
from Modules import dataBase

import numpy as np
import network
import torch
import pickle
try:
        import matplotlib.pyplot as plt
        plot = True
except ImportError:
        plot = False

GPU = False

class Modele():

        def __init__(self, databasePath=None, batch_size=32, gpu=None):

                if gpu is None:
                        GPU = False
                else :
                        GPU = True

                self.model1 = network.Net().cuda()
                self.model2 = network.Net().cuda()

		if GPU:
                	torch.backends.cudnn.benchmark = True
                        torch.cuda.set_device(gpu)
			self.model1.cuda()
			self.model2.cuda()

                self.batch_size = batch_size

                self.databasePath = databasePath

                self.loadBatch()

                self.losses = []
                self.losses_test = []


        def loadBatch(self):
                # Load mini batch from file named batch_num


                if self.databasePath is None:

                        print("____ Loading batch at random: ")

                        self.X1 = [torch.randn(self.batch_size, 1, 80, 100)-1 for i in range(self.batch_size)]
                        self.X2 = [torch.randn(self.batch_size, 1, 80, 100)-1 for i in range(self.batch_size)]
                        self.L1 = [str(i) for i in range(self.batch_size)]
                        self.L2 = [str(j) for j in range(self.batch_size)]

                else:
                        print("____ Loading batches from file")

                        ## Construct and save database
                        D = dataBase.dataBase()
                        D.constructDatabase(self.databasePath)
                        self.batches = D.getBatches(self.batch_size)

                        self.testBatches = D.getTestSet(self.batch_size)

                        print("We have", len(self.batches), "batches for the training part.")





        def loss_test(self, y_pred1, y_pred2):
                # copute the loss for the final test part
                # use the MSE for now
                if len(y_pred1) != self.model1.dim_latent and len(y_pred2) != self.model2.dim_latent:
                        raise RuntimeError("y_pred1 and y_pred2 doesn't have same shape for test.")

                loss = 0
                for i in range(self.model1.dim_latent):
                        loss += (float(y_pred1[i]) - float(y_pred2[i]))**2

                return loss


        def eval(self, batches):
                # Evaluation fonction
                # return the meaned loss for batches

                loss = 0

                for batch in batches:
                        tmpLoss = 0

                        N1 = np.array(batch[0]).astype(float)
                        N1 = N1.reshape(self.batch_size, 1, N1.shape[1], N1.shape[2])
                        X1 = torch.FloatTensor(N1)

                        N2 = np.array(batch[1]).astype(float)
                        N2 = N2.reshape(self.batch_size, 1, N2.shape[1], N2.shape[2])
                        X2 = torch.FloatTensor(N2)

                        y_pred1 = self.model1.forward(X1)
                        y_pred2 = self.model2.forward(X2)


                        for i in range(min(len(y_pred1), len(y_pred2))):
                                tmpLoss += self.loss_test(y_pred1[i], y_pred2[i])

                        tmpLoss /= min(len(X1), len(X2))
                loss += tmpLoss

                return loss/len(batches)

        def save_weights(self, name):
                # save the weights of the model with the name name

                # Passer en .cpu()
                # et remettre en .cuda()

                pass


        def plot_losses(self):
                # plot the losses over time
                if plot == True:
                        loss, = plt.plot(np.array(self.losses), label='Loss on training')
                        lossTest, = plt.plot(np.array(self.losses_test), label='Loss on test')
                        plt.legend(handles=[loss, lossTest])
                        plt.show()
                else:
                        print("Impossible to plot, tkinter not available.")

        def is_over_fitting(self):
                # return True of False is the modele is overfitting
                # find an algorithm that do the job i.e. 

                # if self.losses_test is not inscreasing for T epochs
                # with a threshold of K

                return False

        def myloss(self, batch, alpha=0.7):

                s = torch.nn.CosineSimilarity(dim=0)
                X1, X2, L1, L2, indices = batch

                rank = 0

                for x in range(len(X1)):
                        for y in range(len(X2)):
                                if y != x:
                                        rank += max(0, alpha - s(X1[indices[x]], X2[x]) + s(X1[indices[x]], X2[y]))

                return rank

        def learn(self, EPOCHS, learning_rate=1e-7, momentum=0.9):

                print("_____ Training")
                #criterion = myloss()
                #optimizer = torch.optim.SGD(self.parameters(), lr=learning_rate, momentum=momentum)
                parameters = [p for p in self.model1.parameters()] + [p for p in self.model2.parameters()]

                optimizer = torch.optim.Adam(parameters, lr=learning_rate) ## if you can use +
                for t in range(EPOCHS):
                        # Make learn the two models with respects to x and y

                        for batch in self.batches:
                                N1 = np.array(batch[0]).astype(float)
                                N1 = N1.reshape(self.batch_size, 1, N1.shape[1], N1.shape[2])
                                X1 = torch.autograd.Variable(torch.FloatTensor(N1), requires_grad=True)
                                if GPU:
                                        X1.cuda()

                                N2 = np.array(batch[1]).astype(float)
                                N2 = N2.reshape(self.batch_size, 1, N2.shape[1], N2.shape[2])
                                X2 = torch.autograd.Variable(torch.FloatTensor(N2), requires_grad=True)
                                if GPU:
                                        X2.cuda()

                                y_pred1 = self.model1.forward(X1)
                                y_pred2 = self.model2.forward(X2)

                                L1 = batch[2]
                                L2 = batch[3]
                                indices = batch[4]

                                # Compute and print loss
                                loss = self.myloss((y_pred1, y_pred2, L1, L2, indices))
                                print(t, loss.item())

                                # Zero gradients, perform a backward pass, and update the weights.
                                optimizer.zero_grad()
                                loss.backward()
                                optimizer.step()


                        # appending losses
                        self.losses.append(float(loss.item()))
                        self.losses_test.append(self.eval(self.testBatches))

                        if self.is_over_fitting():
                                # stop learning
                                return

                print(self.losses)
                print(self.losses_test)

                self.plot_losses()


