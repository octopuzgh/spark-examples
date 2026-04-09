from pyspark.sql import SparkSession

# 创建 SparkSession
spark = (
    SparkSession.builder
    .appName("读员工表")
    .getOrCreate())

# 读取 employee 表
df = (
    spark.read.format("jdbc")
    .option("url", "jdbc:mysql://192.168.152.131:3306/employee_performance?useSSL=false") \
    .option("driver", "com.mysql.cj.jdbc.Driver")
    .option("dbtable", "employee")
    .option("user", "octopuz_remote")
    .option("password", "Octopuz@123")
    .load())

# 显示数据
print("员工表数据：")
df.show()

# 打印表结构
print("表结构：")
df.printSchema()

# 统计行数
print(f"总行数: {df.count()}")

spark.stop()
# 员工表数据：
# +---+------+-------+----------+------------+----------+--------------------+-------------------+-------------------+
# | id|emp_no|   name|department|    position| hire_date|               email|         created_at|         updated_at|
# +---+------+-------+----------+------------+----------+--------------------+-------------------+-------------------+
# |  1|  1001|   张三|    技术部|  Java工程师|2023-01-15|zhangsan@company.com|2026-03-28 16:22:11|2026-03-28 16:22:11|
# |  2|  1002|   李四|    技术部|  前端工程师|2023-02-20|    lisi@company.com|2026-03-28 16:22:11|2026-03-28 16:22:11|
# |  3|  1003|   王五|    市场部|    市场专员|2023-03-10|  wangwu@company.com|2026-03-28 16:22:11|2026-03-28 16:22:11|
# |  4|  1004|   赵六|    技术部|  测试工程师|2023-04-05| zhaoliu@company.com|2026-03-28 16:22:11|2026-03-28 16:22:11|
# |  5|  1005|   陈七|    市场部|    市场经理|2023-01-20|  chenqi@company.com|2026-03-28 16:22:11|2026-03-28 16:22:11|
# |  6|  1006|   刘八|    销售部|    销售专员|2023-05-12|   liuba@company.com|2026-03-28 16:22:11|2026-03-28 16:22:11|
# |  7|  1007|   周九|    销售部|    销售经理|2023-03-18| zhoujiu@company.com|2026-03-28 16:22:11|2026-03-28 16:22:11|
# |  8|  1008|   吴十|    技术部|      架构师|2022-11-01|   wushi@company.com|2026-03-28 16:22:11|2026-03-28 16:22:11|
# | 13|  0057|octopuz|    技术部|ai数据工程师|2026-03-31|     zupotco@163.com|2026-03-31 10:50:44|2026-03-31 11:08:40|
# | 14|  1009|   孙九|    技术部|  后端工程师|2024-01-10|  sunjiu@company.com|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 15|  1010|   周十|    技术部|  前端工程师|2024-01-15| zhoushi@company.com|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 16|  1011| 吴十一|    技术部|  运维工程师|2024-02-01| wushiyi@company.com|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 17|  1012| 郑十二|    技术部|大数据工程师|2024-02-10|zhengshier@compan...|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 18|  1013| 王十三|    市场部|    市场专员|2024-02-15|wangshisan@compan...|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 19|  1014| 李十四|    市场部|    品牌专员|2024-03-01| lishisi@company.com|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 20|  1015| 张十五|    市场部|    活动策划|2024-03-10|zhangshiwu@compan...|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 21|  1016| 刘十六|    销售部|    销售专员|2024-03-15|liushiliu@company...|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 22|  1017| 陈十七|    销售部|    销售专员|2024-04-01|chenshiqi@company...|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 23|  1018| 林十八|    销售部|    销售经理|2024-04-10|linshiba@company.com|2026-04-03 17:25:08|2026-04-03 17:25:08|
# | 24|  1019| 黄十九|    产品部|    产品助理|2024-04-15|huangshijiu@compa...|2026-04-03 17:25:08|2026-04-03 17:25:08|
# +---+------+-------+----------+------------+----------+--------------------+-------------------+-------------------+
# only showing top 20 rows
# 表结构：
# root
#  |-- id: long (nullable = true)
#  |-- emp_no: string (nullable = true)
#  |-- name: string (nullable = true)
#  |-- department: string (nullable = true)
#  |-- position: string (nullable = true)
#  |-- hire_date: date (nullable = true)
#  |-- email: string (nullable = true)
#  |-- created_at: timestamp (nullable = true)
#  |-- updated_at: timestamp (nullable = true)
#
# 总行数: 30
