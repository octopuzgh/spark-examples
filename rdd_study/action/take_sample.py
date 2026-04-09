# rdd.takeSample(withReplacement, num, seed=None)
# withReplacement: 是否放回相同位置的抽取，如果本来就有两个一样的，即使选择不放回，那么也可能会有重复的元素
# num: 采样的元素个数
# seed: 随机数种子
# from pyspark import SparkContext# from pyspark import SparkContext# 从 RDD 中随机采样 num 个元素
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("TakeSample")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(rdd.takeSample(True, 7))
    print(rdd.takeSample(False, 7))
    # [3, 3, 1, 7, 10, 3, 1]
    # [6, 10, 1, 9, 8, 7, 4]
