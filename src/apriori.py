import os
import shutil
import sys

from pyspark import SparkContext

DEBUG = 1


def Dprint(info):
    if DEBUG:
        print(info)


def generate_next_c(f_k, k):
    next_c = [var1 | var2 for index, var1 in enumerate(f_k) for var2 in f_k[index + 1:] if
              list(var1)[:k - 2] == list(var2)[:k - 2]]
    return next_c


def generate_f_k(sc, c_k, shared_itemset, sup):
    def get_sup(x):
        x_sup = len([1 for t in shared_itemset.value if x.issubset(t)])
        if x_sup >= sup:
            return x, x_sup
        else:
            return ()

    f_k = sc.parallelize(c_k).map(get_sup).filter(lambda x: x).collect()
    return f_k


def apriori(sc, f_input, f_output, min_sup):
    # read the raw data
    data = sc.textFile(f_input)
    # count the total number of samples
    n_samples = data.count()
    # min_sup to frequency
    sup = n_samples * min_sup
    # split sort
    itemset = data.map(lambda line: sorted([int(item) for item in line.strip().split(' ')]))
    # share the whole itemset with all workers
    shared_itemset = sc.broadcast(itemset.map(lambda x: set(x)).collect())
    # store for all freq_k
    frequent_itemset = []

    # prepare candidate_1
    k = 1
    c_k = itemset.flatMap(lambda x: set(x)).distinct().collect()
    c_k = [{x} for x in c_k]

    # when candidate_k is not empty
    while len(c_k) > 0:
        # generate freq_k
        Dprint("C{}: {}".format(k, c_k))
        f_k = generate_f_k(sc, c_k, shared_itemset, sup)
        Dprint("F{}: {}".format(k, f_k))

        frequent_itemset.append(f_k)
        # generate candidate_k+1
        k += 1
        c_k = generate_next_c([set(item) for item in map(lambda x: x[0], f_k)], k)

    # output the result to file system
    sc.parallelize(frequent_itemset, numSlices=1).saveAsTextFile(f_output)
    sc.stop()


if __name__ == "__main__":
    if os.path.exists(sys.argv[2]):
        shutil.rmtree(sys.argv[2])
    apriori(SparkContext(appName="Spark Apriori"), sys.argv[1], sys.argv[2], float(sys.argv[3]))
    # apriori(SparkContext(appName="Spark Apriori"), "../data/test.dat", "../result/test", 0.5)
    # apriori(SparkContext(appName="Spark Apriori"), "../data/chess.dat", "../result/chess", 0.8)
    # apriori(SparkContext(appName="Spark Apriori"), "../data/mushroom.dat", "../result/mushroom", 0.8)
    # apriori(SparkContext(appName="Spark Apriori"), "../data/connect.dat", "../result/connect", 0.9)
