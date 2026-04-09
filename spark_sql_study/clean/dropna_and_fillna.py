from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder.appName("clean").master("local[*]").getOrCreate()

# 准备数据
data = [
    (1, "张三", 25, None),
    (2, "李四", None, "北京"),
    (3, None, 30, "上海"),
    (4, "王五", None, None),
    (5, None, None, None)
]
df = spark.createDataFrame(data, ["id", "name", "age", "city"])
df.show()
# +---+----+----+----+
# | id|name| age|city|
# +---+----+----+----+
# |  1|张三|  25|null|
# |  2|李四|null|北京|
# |  3|null|  30|上海|
# |  4|王五|null|null|
# |  5|null|null|null|
# +---+----+----+----+

# ============ dropna()：删除包含空值的行 ============
# 删除任何列有空值的行
df.dropna().show()
# 指定列检查：只有当这些列有空值时才删除
df.dropna(subset=["age", "city"]).show()
# +---+----+---+----+
# | id|name|age|city|
# +---+----+---+----+
# |  2|李四|?? |北京|  ← age 为 null，被删
# |  3|null| 30|上海|
# |  4|王五|?? |?? |  ← 都删
# +---+----+---+----+

# 阈值：至少要有 3 个非空值才保留
df.dropna(thresh=3).show()
# +---+----+---+----+
# | id|name|age|city|
# +---+----+---+----+
# |  1|张三| 25|null|  ← 有3个非空 (id,name,age)
# |  2|李四|null|北京|  ← 有3个非空 (id,name,city)
# |  3|null| 30|上海|  ← 有3个非空 (id,age,city)
# +---+----+---+----+

# ============ fillna()：填充空值 ============
# 统一填充
df.fillna("未知").show()
# +---+----+---+----+
# | id|name|age|city|
# +---+----+---+----+
# |  1|张三| 25|未知|
# |  2|李四|未知|北京|
# |  3|未知| 30|上海|
# |  4|王五|未知|未知|
# |  5|未知|未知|未知|
# +---+----+---+----+

# 按列填充不同值
df.fillna({"name": "匿名", "age": 0, "city": "未知城市"}).show()
# +---+----+---+--------+
# | id|name|age|    city|
# +---+----+---+--------+
# |  1|张三| 25|未知城市|
# |  2|李四|  0|     北京|
# |  3|匿名| 30|     上海|
# |  4|王五|  0|未知城市|
# |  5|匿名|  0|未知城市|
# +---+----+---+--------+

# ============ na.fill()：fillna 的别名 ============
df.na.fill(0).show()

# 填充特定列
df.na.fill("未知", subset=["city"]).show()

spark.stop()