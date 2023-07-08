import math
import random
from collections import defaultdict
import pandas as pd

NUM_CLUSTERS = 3


def euclid_dist(z_one, z_two): # Calculate Euclidean Distance
    x_one, y_one = z_one
    x_two, y_two = z_two
    return math.sqrt((x_one - x_two)**2 + (y_one - y_two)**2)

def var_bar(z): # UNUSED
    print(1/len(z))
    print(sum(val for val in z))
    return (1/len(z) * sum(val for val in z))

def binomial_coefficient(n, r): # Calculate Binomial Coefficient
    return (math.factorial(n) / (math.factorial(r) * math.factorial(n - r)))

def total_possible_clusters(n): # n, m # Calculate Stirling Number of Second Kind
    return (1/math.factorial(NUM_CLUSTERS) * sum(((-1)**(NUM_CLUSTERS-i) * binomial_coefficient(NUM_CLUSTERS, i) * i**n) for i in range(1, NUM_CLUSTERS+1))) # NUM_CLUSTERS+1 as range is not inclusive


dataframe = pd.read_excel("Data Points.xlsx", header=2, usecols=['x-cord', 'y-cord']) # drop first 2 rows, and only take x and y cols

dataframe.dropna(inplace=True) # remove nan values from rows
dataframe = dataframe.astype({'x-cord': 'int', 'y-cord': 'int'}) # converts vals from float to int
x_vals = dataframe['x-cord'].tolist()
y_vals = dataframe['y-cord'].tolist()
dataPointTuple = list(zip(x_vals, y_vals)) # zip x and y lists to a list of tuples of x, y vals

total_clusters = total_possible_clusters(len(dataPointTuple))

centroids = random.sample(dataPointTuple, k=NUM_CLUSTERS) # .sample to choose unique values as nonunique values obviously would cause an error
print("Initial centroids", centroids)

stop = False
count = 0
while True:
    #print(centroids) # For Testing
    count+=1
    dict = defaultdict(list)
    for index, val in enumerate(dataPointTuple): # Calculate euclidean distance of points to n clusters' centroid, and seperate into shortest distance
        shortest = []
        for centroid_val in centroids:
            shortest.append(euclid_dist(val, centroid_val))
        min_val = min(shortest)
        min_index = shortest.index(min_val)
        dict[min_index].append((index, min_val))

    mean_indexes = []
    mean_compare = []
    for index, centroid_val in enumerate(centroids): # retreive indexes of points of shortest euclidean distance for each centroid
        mean_indexes.append((list(zip(*dict.get(index)))[0]))

    for index, val in enumerate(mean_indexes): # retreive (x,y) of points of shortest euclidean distance for each cluster, and calculate their mean for next centroid
        length = len(mean_indexes[index])
        mean_compare.append((sum(dataPointTuple[v][0] for v in val) / length, sum(dataPointTuple[v][1] for v in val) / length))

    if centroids == mean_compare or count > total_clusters: # In worst case, would eventually stop. Stirling Number of Second Kind
        for index, val in enumerate(mean_indexes):
            print(f"C{index+1} = {{{str([val+1 for val in mean_indexes[index]])[1:-1]}}}, |{len(mean_indexes[index])}|, and centroid {centroids[index]}")
        print("|C1| + |C2| + |C3| =", sum(len(x) for x in mean_indexes))
        print("Number of iterations:", count)
        break
    #print("centroids", count, " ", centroids) # For Testing
    #print("mean_compare", count, " ", mean_compare) # For Testing
    centroids = mean_compare