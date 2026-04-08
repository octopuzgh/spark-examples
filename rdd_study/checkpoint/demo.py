from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Checkpoint简单演示").getOrCreate()
sc = spark.sparkContext

# 1. 设置 checkpoint 目录（必须）
sc.setCheckpointDir("/tmp/spark_checkpoint")

# 2. 创建一个有血缘链的 RDD
rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd = rdd.map(lambda x: x * 2)      # [2,4,6,8,10]
rdd = rdd.filter(lambda x: x > 5)   # [6,8,10]
rdd = rdd.map(lambda x: x + 10)     # [16,18,20]

# 3. 在第一次 action 之前调用 checkpoint
rdd.checkpoint()

# 4. 查看 checkpoint 前的血缘
print("=== Checkpoint 前 ===")
print(f"是否已 checkpoint: {rdd.isCheckpointed()}")
print(f"血缘:\n{rdd.toDebugString()}")

# 5. 触发 action，真正执行 checkpoint
print("\n=== 触发 count()，执行 checkpoint ===")
count = rdd.count()
print(f"count 结果: {count}")

# 6. 查看 checkpoint 后的血缘（变短了）
print("\n=== Checkpoint 后 ===")
print(f"是否已 checkpoint: {rdd.isCheckpointed()}")
print(f"文件位置: {rdd.getCheckpointFile()}")
print(f"数据: {rdd.collect()}")
print(f"血缘（已截断）:\n{rdd.toDebugString()}")

spark.stop()


#
# === Checkpoint 前 ===
# 是否已 checkpoint: False
# 血缘:
# b'(2) PythonRDD[1] at RDD at PythonRDD.scala:58 []\n |  ParallelCollectionRDD[0] at readRDDFromFile at PythonRDD.scala:299 []'
#
# === 触发 count()，执行 checkpoint ===
# count 结果: 3
#
# === Checkpoint 后 ===
# 是否已 checkpoint: True
# 文件位置: file:/tmp/spark_checkpoint/e1782906-7a23-4a15-a715-854c28f3d3fe/rdd-1
# 数据: [16, 18, 20]
# 血缘（已截断）:
# b'(2) PythonRDD[1] at RDD at PythonRDD.scala:58 []\n |  ReliableCheckpointRDD[3] at count at /mnt/hgfs/share_files/pyspark_learn/src/rdd_study/checkpoint/demo.py:25 []'
