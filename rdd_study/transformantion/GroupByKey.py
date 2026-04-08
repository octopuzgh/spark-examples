# rdd.groupByKey()  # 按 key 分组，返回 (K, Iterable[V])
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("GroupByKey")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1), ("c", 1), ("b", 1)])
    collect = rdd.groupByKey()
    print( collect.map(lambda x: (x[0], list(x[1]))).collect())
    # [('b', [1, 1]), ('c', [1]), ('a', [1, 1])]
