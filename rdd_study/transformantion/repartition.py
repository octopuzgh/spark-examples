# rdd.repartition(numPartitions)  # 重新分区（增加或减少分区数）
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("Repartition")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
    print(rdd.glom().collect())
    print(rdd.repartition(2).glom().collect())
# [[1, 2], [3, 4], [5, 6]]
# [[5, 6], [1, 2, 3, 4]]
