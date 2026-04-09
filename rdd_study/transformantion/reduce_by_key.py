# rdd.reduceByKey(func)  # (K, V) -> (K, V) 按key聚合
# 自带聚合函数，效率比groupByKey高
# coding=utf-8


from pyspark import SparkConf, SparkContext
if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("ReduceByKey")
    sc = SparkContext(conf = conf)

    rdd=sc.parallelize([("a", 1), ("b", 1), ("a", 1), ("c", 1), ("b", 1)])
    print(rdd.reduceByKey(lambda a, b: a + b).collect())

# [('b', 2), ('c', 1), ('a', 2)]