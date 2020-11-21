import numpy
import scipy.special
import random
from constants import *

class NNet:
    def __init__(self, numInput, numHidden, numOutput):
        self.numInput = numInput
        self.numHidden = numHidden
        self.numOutput = numOutput

        self.weightsInputHidden = numpy.random.uniform(-0.5, 0.5, size=(self.numHidden, self.numInput))
        self.weightsHiddenOutput = numpy.random.uniform(-0.5, 0.5, size=(self.numOutput, self.numHidden))

        self.activationFunction = lambda x: scipy.special.expit(x)

    def getOutputs(self, inputs):
        numpyInputs = numpy.array(inputs, ndmin=2).T
        multiplicationInputsHidden = numpy.dot(self.weightsInputHidden, numpyInputs)
        finalMultiplicationInputsHidden = self.activationFunction(multiplicationInputsHidden)

        multiplicationHiddenOutput = numpy.dot(self.weightsHiddenOutput, finalMultiplicationInputsHidden)
        finalMultiplicationHiddenOutput = self.activationFunction(multiplicationHiddenOutput)

        return finalMultiplicationHiddenOutput

    def modifyWeights(self):
        NNet.modifyArray(self.weightsInputHidden)
        NNet.modifyArray(self.weightsHiddenOutput)

    def create_mixed_weights(self, net1, net2):
        self.weightsInputHidden = NNet.mixArrays(net1.weightsInputHidden,  net2.weightsInputHidden)
        self.weightsHiddenOutput = NNet.mixArrays(net1.weightsHiddenOutput,  net2.weightsHiddenOutput)

    @staticmethod
    def modifyArray(array):
        for x in numpy.nditer(array, op_flags=['readwrite']):
            if random.random() < MUTATION_MODIFY_CHANCE:
                x[...] = numpy.random.random_sample() - 0.5

    @staticmethod
    def mixArrays(array1, array2):
        totalEntries = array1.size
        numRows = array1.shape[0]
        numCols = array1.shape[1]

        numToTake = totalEntries - (int(totalEntries * MUTATION_ARRAY_MIX_PERCENT))
        idx = numpy.random.choice(numpy.arange(totalEntries), numToTake, replace=False)
        print("idx: ", idx)

        res = numpy.random.rand(numRows, numCols)

        for row in range(0, numRows):
            for col in range(0, numCols):
                index = row * numCols + col
                if index in idx:
                    res[row][col] = array1[row][col]
                else:
                    res[row][col] = array2[row][col]

        return res

def tests():
    array1 = numpy.random.uniform(-0.5, 0.5, size=(3, 3))
    array2 = numpy.random.uniform(-0.5, 0.5, size=(3, 3))

    print('array1 size', array1.size, sep='\n')
    print('array1', array1, sep='\n')

    print()

    NNet.modifyArray(array1)
    print('array1 modified', array1, sep='\n')

    print()

    print('array2', array2, sep='\n')

    print()

    mixed = NNet.mixArrays(array1, array2)
    print('mixed arrays', mixed, sep='\n')



if __name__ == "__main__":
    tests()
