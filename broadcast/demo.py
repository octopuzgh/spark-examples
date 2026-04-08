from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("广播变量").getOrCreate()
sc = spark.sparkContext

# 模拟小表数据（部门映射）
dept_map = {1: "技术部", 2: "产品部", 3: "运营部"}

# 广播变量：把小表发到所有 Executor
broadcast_dept = sc.broadcast(dept_map)

# 大表数据（员工）
emp_list = [(1, "张三", 1), (2, "李四", 2), (3, "王五", 1)]
rdd = sc.parallelize(emp_list)

# 使用广播变量 join（避免 shuffle）
result = rdd.map(lambda x: (x[0], x[1], broadcast_dept.value.get(x[2])))

print(result.collect())
# 输出: [(1, '张三', '技术部'), (2, '李四', '产品部'), (3, '王五', '技术部')]

spark.stop()