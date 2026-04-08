import time

from pyspark import StorageLevel, SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf().setMaster("local[*]").setAppName("MapPartitions")
    sc = SparkContext(conf = conf)
    # rdd = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
    # # 各种持久化级别
    # rdd.cache()   # 默认,内存缓存
    # rdd.persist(StorageLevel.MEMORY_ONLY)           # 纯内存
    # rdd.persist(StorageLevel.MEMORY_ONLY_2)         # 纯内存+2个副本
    # rdd.persist(StorageLevel.MEMORY_AND_DISK)       # 内存+磁盘
    # rdd.persist(StorageLevel.MEMORY_AND_DISK_2)     # 内存+磁盘+2个副本
    # rdd.persist(StorageLevel.MEMORY_AND_DISK_DESER) # 序列化+磁盘
    # rdd.persist(StorageLevel.DISK_ONLY)             # 纯磁盘
    # rdd.persist(StorageLevel.OFF_HEAP)              # 堆外内存
    # rdd.unpersist()                                 # 取消缓存
    # 模拟一个计算代价高的 RDD：生成1000万条数据，每条做复杂运算
    print("=" * 50)
    print("生成大数据量 RDD（模拟耗时计算）...")
    print("=" * 50)

    big_rdd = sc.parallelize(range(1, 10000001)) \
        .map(lambda x: (x % 1000, x ** 2 - x ** 1.5 + x ** 0.5))

    # ========== 场景1：不使用缓存，两次操作 ==========
    print("\n【场景1】不使用缓存，两次 count()")

    start = time.time()
    count1 = big_rdd.count()
    print(f"第一次 count() 结果: {count1}, 耗时: {time.time() - start:.2f} 秒")

    start = time.time()
    count2 = big_rdd.count()
    print(f"第二次 count() 结果: {count2}, 耗时: {time.time() - start:.2f} 秒")
    # 第二次会重新计算整个 RDD，因为没缓存

    # ========== 场景2：使用缓存 ==========
    print("\n" + "=" * 50)
    print("【场景2】使用 cache()，三次 count()")
    print("=" * 50)

    # 重新生成 RDD（避免上面已经算过的干扰）
    big_rdd_cached = sc.parallelize(range(1, 10000001)) \
        .map(lambda x: (x % 1000, x ** 2 - x ** 1.5 + x ** 0.5))

    # 关键：缓存
    big_rdd_cached.cache()

    # 触发第一次计算（同时把数据存入缓存）
    start = time.time()
    count1_cached = big_rdd_cached.count()
    print(f"第一次 count() 结果: {count1_cached}, 耗时: {time.time() - start:.2f} 秒")

    # 第二次 count() 直接从缓存读
    start = time.time()
    count2_cached = big_rdd_cached.count()
    print(f"第二次 count() 结果: {count2_cached}, 耗时: {time.time() - start:.2f} 秒")

    # 第三次 count() 直接从缓存读
    start = time.time()
    count2_cached = big_rdd_cached.count()
    print(f"第三次 count() 结果: {count2_cached}, 耗时: {time.time() - start:.2f} 秒")


# ==================================================
# 生成大数据量 RDD（模拟耗时计算）...
# ==================================================
#
# 【场景1】不使用缓存，两次 count()
# 第一次 count() 结果: 10000000, 耗时: 2.73 秒
# 第二次 count() 结果: 10000000, 耗时: 2.13 秒
#
# ==================================================
# 【场景2】使用 cache()，三次 count()
# ==================================================
# 第一次 count() 结果: 10000000, 耗时: 4.19 秒(写入缓存需要时间)
# 第二次 count() 结果: 10000000, 耗时: 0.77 秒
# 第三次 count() 结果: 10000000, 耗时: 0.75 秒