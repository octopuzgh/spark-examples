# rdd1.intersection(rdd2)  # 返回两个 RDD 的交集
from pyspark import SparkConf,SparkContext
if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("Intersection")
    sc = SparkContext(conf = conf)
    rdd1 = sc.parallelize([1, 2, 3, 4])
    rdd2 = sc.parallelize([3, 4, 5, 6])
    print(rdd1.intersection(rdd2).collect())
# [4, 3]