# rdd.glom()  # 将每个分区中的元素合并成一个列表
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("Glom")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
    print(rdd.glom().collect())
# [[1, 2], [3, 4], [5, 6]]