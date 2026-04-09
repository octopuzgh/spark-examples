from pyspark.sql import SparkSession

from pyspark.sql.functions import desc
spark = SparkSession.builder.appName("duplicate").master("local[*]").getOrCreate()

# 准备数据
data = [
    (1, "张三", 25, "北京"),
    (2, "李四", 30, "上海"),
    (3, "张三", 25, "北京"),  # 完全重复
    (4, "王五", 28, "广州"),
    (5, "张三", 25, "北京"),  # 完全重复
    (6, "李四", 30, "深圳")   # 部分重复
]
df = spark.createDataFrame(data, ["id", "name", "age", "city"])
df.show()
# +---+----+---+----+
# | id|name|age|city|
# +---+----+---+----+
# |  1|张三| 25|北京|
# |  2|李四| 30|上海|
# |  3|张三| 25|北京|
# |  4|王五| 28|广州|
# |  5|张三| 25|北京|
# |  6|李四| 30|深圳|
# +---+----+---+----+

# ============ distinct()：去重（所有列相同） ============
df.distinct().show()
# +---+----+---+----+
# | id|name|age|city|
# +---+----+---+----+
# |  1|张三| 25|北京|
# |  2|李四| 30|上海|
# |  4|王五| 28|广州|
# |  6|李四| 30|深圳|
# +---+----+---+----+

# ============ dropDuplicates()：按指定列去重 ============
# 按 name 和 age 去重（保留第一次出现）
df.dropDuplicates(["name", "age"]).show()
# +---+----+---+----+
# | id|name|age|city|
# +---+----+---+----+
# |  1|张三| 25|北京|
# |  2|李四| 30|上海|
# |  4|王五| 28|广州|
# +---+----+---+----+

# 按 name 去重
df.dropDuplicates(["name"]).show()
# +---+----+---+----+
# | id|name|age|city|
# +---+----+---+----+
# |  1|张三| 25|北京|
# |  2|李四| 30|上海|
# |  4|王五| 28|广州|
# +---+----+---+----+

# 保留最后一次出现（用 orderBy 控制顺序）

df.orderBy(desc("id")).dropDuplicates(["name"]).show()
# +---+----+---+----+
# | id|name|age|city|
# +---+----+---+----+
# |  5|张三| 25|北京|
# |  6|李四| 30|深圳|
# |  4|王五| 28|广州|
# +---+----+---+----+

spark.stop()