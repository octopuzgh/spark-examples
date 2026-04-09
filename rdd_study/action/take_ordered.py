# rdd.takeOrdered(num, key=None)  # 返回 RDD 中最小的 num 个元素
# num: 采样的元素个数
# key: 排序的 key 函数


# stream.sorted().limit(num).collect(Collectors.toList())  # 取最小的 num 个
# stream.sorted(comparator).limit(num).collect(Collectors.toList())