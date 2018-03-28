from math import *

class EuropeanCallOption:
    def put_BinomialTree(self, header, price):
        # Fill with put_BinomialTree function

        # Price is a list of lists
        N=0
        if len(price)!=0:
            N=len(price)-1

        if N > 9 :# if tree is too big, refuse to print anything
            #print(header + "\n")
            #print("BinomialTree has " + str(N) + " levels: too many to print!\n")
            return
        print(header + '\n\n')

        print( "BinomialTree with " + str(N) + " time steps:\n\n")
        for i in range(N+1):
            print("Stock:  ", end="")
            for j in range(len(price[i])):
                print('{:>8}'.format('%.2f') % price[i][j]['stockPrice'], end="")

            print("\n")
            print("Option: ", end="")

            for j in range(len(price[i])):
                print('{:>8}'.format('%.2f') % price[i][j]['optionPrice'], end="")

            print("\n\n")

        print("\n")

    def __init__(self, s0, k,  rfr, v, et):
        self._S0 = s0
        self._K = k
        self._r = rfr
        self._sigma = v
        self._T = et

    # Calculate the Price of the option
    #  using the binomial tree method
    def binomialPrice(self, numIntervals):
        # Fill with binomialPrice function
        # time interval length
        deltaT  = self._T / numIntervals
        # factor by which stock price might rise at each step
        u = exp(self._sigma * sqrt(deltaT))
        # factor by which stock price might fall at each step
        d = 1 / u
        # risk-free interest rate factor for one time interval
        a= exp(self._r * deltaT)
        # RN probability of an up move in stock price
        p= (a - d) / (u - d)
        # RN probability of a down move in stock price
        q= 1.0 - p

        # put_BinomialTree("Initial, empty binomialTree:", binomialTree);

        # Build the shape of the binomialTree, by pushing
        # successively longer vector<Price> values (initially
        # all elements 0.0)

        binomialTree = list()
        for i in range(numIntervals+1):
            vInterval = []
            for j in range(i+1):
                vInterval += [{'stockPrice': 0, 'optionPrice': 0}]
            binomialTree = binomialTree + [vInterval]


        self.put_BinomialTree("After filled in with all 0.0:", binomialTree);

        # Fill the stockPrice component of the binomialTree
        for i in range(numIntervals+1):
            for j in range(i+1):
                binomialTree[i][j]['stockPrice'] = self._S0 * pow(u, j) * pow(d, i-j)
        self.put_BinomialTree("After filled in with stock prices:", binomialTree);

        # Fill the optionPrices at the terminal nodes
        for j in range(numIntervals+1):
            binomialTree[numIntervals][j]['optionPrice'] = max(binomialTree[numIntervals][j]['stockPrice'] - self._K ,0.0);

        self.put_BinomialTree("After filled in with terminal option values:", binomialTree);

        # Now work backwards, filling optionPrices in the rest of the tree
        for i in range(numIntervals-1,-1, -1):
            for j in range(i+1):
                binomialTree[i][j]['optionPrice'] = exp(-self._r * deltaT)*(p * binomialTree[i+1][j+1]['optionPrice'] + q* binomialTree[i+1][j]['optionPrice'])

        self.put_BinomialTree("After filled in with all option values:", binomialTree)

        # Return the time 0 call price
        return binomialTree[0][0]['optionPrice']




ec1 = EuropeanCallOption (50.0, # current stockprice, S0
50.0, # option strike price, K
0.10, # risk - free rate
0.40, # stock price volatility
0.4167) # expiration time T(5 months)

print("Call price, with " + str(5) + " intervals: " + str(ec1.binomialPrice(5)) + "\n")
N =[5, 10, 20, 50, 100, 200, 500, 1000]

for i in range(len(N)):
    print("Call price, with " + str(N[i]) + " intervals: "+ str(ec1.binomialPrice(N[i])) + "\n")
