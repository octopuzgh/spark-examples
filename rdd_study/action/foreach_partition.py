#rdd.foreachPartition(func)  # 对每个分区的迭代器应用函数（主要用于副作用）
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("ForeachPartition")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
    rdd.foreachPartition(lambda x: print(list(x)))