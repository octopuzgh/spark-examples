# rdd.countByKey()  # 统计每个 key 出现的次数，返回 dict
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("CountByKey")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1), ("c", 1)])
    key = rdd.countByKey()
    print(key)
    # defaultdict(<class 'int'>, {'a': 2, 'b': 1, 'c': 1})
