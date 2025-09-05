import numpy as np 
import random
import tools 

class Network :
    def __init__(self,architecture,weight_lower_bound,weight_upper_bound):
        """This class represents the neural network
        Parameters:
        -weight_lower_bound: The minimum value a random weight can assume
        -weight_upper_bound: The maximum value a random weight can assume
        """
        self.architecture = architecture 
        "An array containing the number of neurons for each layer"
        self.weights = tools.init_weights(self.architecture,weight_lower_bound,weight_upper_bound)
        "A matrix of matrices containing the weights of each layer to layer connection"
        self.biases = tools.init_biases(self.architecture,weight_lower_bound,weight_upper_bound)
        "An array of arrays containing the biases of each neuron"
 
    def predict(self,input):
        """Return the output of the neural network
        Parameters:
        -input : An array with as many elements as the neurons of the first layer
        """
        return tools.multilinear_multiplication(self.weights,self.biases,input)
     
    def error(self,input,output):
        """Return the output of the error function of the network to an expected output
        Parameters:
        -input: An array with as many elements as the neurons of the first layer
        -output: An expected output as an array with as many elements as the neurons of the last layer
        """
        error_root = np.subtract(self.predict(input), output)
        return np.multiply(error_root, error_root)
    
    def dw_prediction_error(self,i,j,k,n,input,output):
        """Return the partial derivate for a given weight of the error function of the network to an expected output for a single neuron
        Parameters:
        -i,j,k: The index of the weight
        -n: The index of the chose output neuron  
        -input: An array with as many elements as the neurons of the first layer
        -output: An expected output as an array with as many elements as the neurons of the last layer
        """
        actual_error = self.error(input,output)
        self.weights = tools.modify_single_weight(self.weights,tools.h(),i,j,k) #increment the weight
        after_increment_error = self.error(input, output)
        self.weights = tools.modify_single_weight(self.weights,-tools.h(),i,j,k) #decrement the weight
        err_dw = (after_increment_error[n]-actual_error[n])/tools.h() #partial derivation of the error function to the weight 
        return err_dw
    
    def db_prediction_error(self,i,j,n,input,output):
        """Return the partial derivate for a given bias of the error function of the network to an expected output for a single neuron
        Parameters:
        -i,j: The index of the bias
        -n: The index of the chosen output neuron  
        -input: An array with as many elements as the neurons of the first layer
        -output: An expected output as an array with as many elements as the neurons of the last layer
        """
        actual_error = self.error(input,output)
        self.biases = tools.modify_single_bias(self.biases,tools.h(),i,j) #increment the bias
        after_increment_error = self.error(input, output)
        self.biases = tools.modify_single_bias(self.biases,-tools.h(),i,j) #decrement the bias
        err_db = (after_increment_error[n]-actual_error[n])/tools.h() #partial derivation of the error function to the bias
        return err_db
    

    def train(self,dataset,batch_size,learning_rate):
        """This function train the network given a specific dataset
        Parameters:
        -dataset: An array of [input, output] arrays 
        -batch_size: The size of the batch to perform the mini stochastic gradient descent as an integer
        -learning_rate: The learning rate of the netweork during the training as a float  
        """ 
        training_dataset = tools.divide_dataset_in_batches(dataset,batch_size) #divide the dataset in batches
        self.backpropagation(training_dataset,learning_rate) #perform the back propagation algorithm

    def backpropagation(self,dataset,learning_rate):
        """This function perform the backpropagation algorithm given a specific dataset
        Parameters:
        -dataset: An array of [input, output] arrays 
        -learning_rate: The learning rate of the network during the training as a float  
        """ 
        minimization_biases = tools.init__zero_biases_copy(self.architecture) #generate a matrix of matrices of zeros to stock the derivate error (Dbias)
        minimization_weights = tools.init_zero_weights_copy(self.architecture) #generate an array of arrays of zero to stock the derivate error (Dweight)
        for b in range(len(dataset)):
            for e in range(len(dataset[b])):
                for n in range(len(self.weights[len(self.weights)-1][0])):
                    for i in range(len(self.weights)):
                        for j in range(len(self.weights[i])):
                            for k in range(len(self.weights[i][j])):
                                dw_error = self.dw_prediction_error(i,j,k,n,dataset[b][e][0],dataset[b][e][1])
                                minimization_weights = tools.modify_single_weight(minimization_weights,-dw_error*learning_rate,i,j,k)
            for e in range(len(dataset[b])):
                    for n in range(len(self.weights[len(self.weights)-1][0])):
                        for i in range(len(self.biases)):
                            for j in range(len(self.biases[i])):
                                db_error = self.db_prediction_error(i,j,n,dataset[b][e][0],dataset[b][e][1],)
                                minimization_biases = tools.modify_single_bias(minimization_biases,-db_error*learning_rate,i,j)
            self.weights = tools.update_weights(self.weights,minimization_weights) #update the weights
            self.biases = tools.update_biases(self.biases,minimization_biases) #update the biases
            minimization_biases = tools.init__zero_biases_copy(self.architecture) #generate a matrix of matrices of zeros to stock the derivate error (Dbias)
            minimization_weights = tools.init_zero_weights_copy(self.architecture) #generate an array of arrays of zero to stock the derivate error (Dweight)
 


