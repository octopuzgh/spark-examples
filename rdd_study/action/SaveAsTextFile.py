#直接由Executor进行保存,不会将数据保存到Driver端

# rdd.saveAsTextFile(path)  # 将 RDD 保存为文本文件到分布式存储
import os
import shutil

from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[3]").setAppName("SaveAsTextFile")
    sc = SparkContext(conf = conf)
    rdd = sc.parallelize([1, 2, 3, 4, 5, 6])
    output_path = "/mnt/hgfs/share_files/pyspark_learn/out"
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
        print(f"已删除旧目录: {output_path}")
    rdd.saveAsTextFile(output_path)