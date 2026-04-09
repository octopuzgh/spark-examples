# rdd.coalesce(numPartitions, shuffle=False)  # 减少分区数（默认不 shuffle）
# shuffle: True 随机 shuffle，False 不 shuffle,True 的时候才能增加分区数
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("Coalesce")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
    print(rdd.glom().collect())
    print(rdd.coalesce(2).glom().collect())
# [[1, 2], [3, 4], [5, 6]]
# [[1, 2], [3, 4, 5, 6]]

