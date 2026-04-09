# rdd.mapPartitions(func, preservesPartitioning=False)
# 对每个分区的迭代器应用函数，返回新的 RDD
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("MapPartitions")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
    print(rdd.mapPartitions(lambda x: [sum(x)]).collect())