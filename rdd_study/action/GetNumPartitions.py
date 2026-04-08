from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("GetNumPartitions")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
    print(rdd.getNumPartitions())