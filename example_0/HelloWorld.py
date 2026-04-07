# coding=utf-8
import os
import shutil

from pyspark import SparkConf, SparkContext
if __name__ == "__main__":
    conf = SparkConf().setMaster("local[2]").setAppName("HelloWorld")
    sc = SparkContext(conf = conf)

    # 创建RDD
    lines = sc.textFile("/mnt/hgfs/share_files/pyspark_learn/resources/words.txt")
    # 处理RDD
    counts = (lines.flatMap(lambda x: x.split(' '))# 将每行数据进行分词
            .map(lambda x: (x, 1))# 将分词后的数据进行转换
            .reduceByKey(lambda a, b: a + b))# 对转换后的数据进行聚合
    output = counts.collect()
    output_path = "/mnt/hgfs/share_files/pyspark_learn/out"
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
        print(f"已删除旧目录: {output_path}")
    counts.saveAsTextFile(output_path)

    for (word, count) in output:
        print("%s: %i" % (word, count))