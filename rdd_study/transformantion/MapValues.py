# rdd.mapValues(func)  # 作用于 (K, V) 中的 V，保持 K 不变
from pyspark import SparkConf,SparkContext
if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("MapValues")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1), ("c", 1), ("b", 1)])
    print(rdd.mapValues(lambda x: x*10).collect())
# [('a', 10), ('b', 10), ('a', 10), ('c', 10), ('b', 10)]