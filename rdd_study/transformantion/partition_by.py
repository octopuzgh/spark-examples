# rdd.partitionBy(numPartitions, partitionFunc=None)  # 按 key 重新分区
# numPartitions: 分区数,不能大于 SparkContext 中设置的最大分区数
# partitionFunc: 分区函数
from pyspark import SparkConf,SparkContext

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[5]").setAppName("PartitionBy")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([("a", 1),("ab", 1), ("bb", 1), ("ab", 1), ("ccc", 1), ("b", 1)], 2)
    collect = (rdd.map(lambda x: (x[0], x[1]*10))
                .reduceByKey(lambda a, b: a + b))
    print(collect.partitionBy(3, lambda x: len(x)).collect())
    print("各分区数据：")
    for i in range(3):
        items = collect.partitionBy(3, lambda x: len(x)).glom().collect()[i]
        print(f"分区 {i}: {items}")
# [('ccc', 10), ('b', 10), ('a', 10), ('ab', 20), ('bb', 10)]
# 各分区数据：
# 分区 0: [('ccc', 10)]
# 分区 1: [('b', 10), ('a', 10)]
# 分区 2: [('ab', 20), ('bb', 10)]
