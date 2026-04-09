#直接由Executor进行计算,不需要返回结果到 Driver

# rdd.foreach(func)  # 对 RDD 中每个元素应用函数（主要用于副作用）
# stream.forEach(action)  // 对流中每个元素执行操作