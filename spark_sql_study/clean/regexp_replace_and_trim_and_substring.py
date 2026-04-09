from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, ltrim, rtrim, regexp_replace, substring, length, upper, lower, initcap, \
    when

spark = SparkSession.builder.appName("string").master("local[*]").getOrCreate()

# 准备数据
data = [
    (1, "  张三  ", " 138-0013-8001 ", "hello@example.com", "2024-01-15"),
    (2, "李四", "138-0013-8002", "李四@example", "2024/01/20"),
    (3, "  王五  ", " 138-0013-8003 ", "wang@", "20240125"),
    (4, "赵六", "abc", "invalid", "2024-01-30")
]
df = spark.createDataFrame(data, ["id", "name", "phone", "email", "date"])
df.show()
# +---+--------+---------------+-----------------+----------+
# | id|    name|          phone|            email|      date|
# +---+--------+---------------+-----------------+----------+
# |  1|  张三  | 138-0013-8001 |hello@example.com|2024-01-15|
# |  2|     李四|  138-0013-8002|      李四@example|2024/01/20|
# |  3|  王五  | 138-0013-8003 |          wang@|  20240125|
# |  4|     赵六|           abc|          invalid|2024-01-30|
# +---+--------+---------------+-----------------+----------+

# ============ trim()：去除首尾空格 ============
df.withColumn("name_clean", trim(col("name"))).show()
# +---+--------+---------------+-----------------+----------+-----------+
# | id|    name|          phone|            email|      date|name_clean|
# +---+--------+---------------+-----------------+----------+-----------+
# |  1|  张三  | 138-0013-8001 |hello@example.com|2024-01-15|       张三|
# |  2|     李四|  138-0013-8002|      李四@example|2024/01/20|       李四|
# |  3|  王五  | 138-0013-8003 |          wang@|  20240125|       王五|
# |  4|     赵六|           abc|          invalid|2024-01-30|       赵六|
# +---+--------+---------------+-----------------+----------+-----------+

# ltrim()：去除左边空格
df.withColumn("name_left", ltrim(col("name"))).show()

# rtrim()：去除右边空格
df.withColumn("name_right", rtrim(col("name"))).show()

# ============ regexp_replace()：正则替换 ============
# 去除手机号中的横线
df.withColumn("phone_clean", regexp_replace(col("phone"), "-", "")).show()
# +---+---+---------------+-----------------+----------+-----------+
# | id|name|          phone|            email|      date|phone_clean|
# +---+---+---------------+-----------------+----------+-----------+
# |  1|张三| 138-0013-8001 |hello@example.com|2024-01-15|13800138001|
# |  2|李四|  138-0013-8002|      李四@example|2024/01/20|13800138002|
# |  3|王五| 138-0013-8003 |          wang@|  20240125|13800138003|
# |  4|赵六|           abc|          invalid|2024-01-30|        abc|
# +---+---+---------------+-----------------+----------+-----------+

# 去除所有非数字字符（保留数字）
df.withColumn("phone_digits", regexp_replace(col("phone"), "[^0-9]", "")).show()
# +---+---+---------------+-----------------+----------+-----------+
# | id|name|          phone|            email|      date|phone_digits|
# +---+---+---------------+-----------------+----------+-----------+
# |  1|张三| 138-0013-8001 |hello@example.com|2024-01-15|  13800138001|
# |  2|李四|  138-0013-8002|      李四@example|2024/01/20|  13800138002|
# |  3|王五| 138-0013-8003 |          wang@|  20240125|  13800138003|
# |  4|赵六|           abc|          invalid|2024-01-30|            |
# +---+---+---------------+-----------------+----------+-----------+

# 替换邮箱中的 @ 为 [at]
df.withColumn("email_obfuscated", regexp_replace(col("email"), "@", "[at]")).show()

# ============ substring()：截取字符串 ============
# 截取手机号后4位
df.withColumn("phone_last4", substring(col("phone"), -4, 4)).show()
# 注意：substring 位置从1开始，负数表示从末尾倒数

# 截取姓名第一个字
df.withColumn("first_char", substring(col("name"), 1, 1)).show()
# +---+---+------+
# | id|name|first_char|
# +---+---+------+
# |  1|张三|  张|
# |  2|李四|  李|
# |  3|王五|  王|
# |  4|赵六|  赵|
# +---+---+------+

# ============ 其他常用字符串函数 ============
df.select(
    col("name"),
    length(col("name")).alias("name_len"),      # 长度
    upper(col("name")).alias("name_upper"),     # 大写
    lower(col("name")).alias("name_lower"),     # 小写
    initcap(col("name")).alias("name_cap")      # 首字母大写
).show()
# +----+--------+----------+----------+--------+
# |name|name_len|name_upper|name_lower|name_cap|
# +----+--------+----------+----------+--------+
# |  张三|       3|      张三|      张三|    张三|
# |  李四|       3|      李四|      李四|    李四|
# |  王五|       3|      王五|      王五|    王五|
# |  赵六|       3|      赵六|      赵六|    赵六|
# +----+--------+----------+----------+--------+

# ============ 综合清洗示例 ============
df_cleaned = df \
    .withColumn("name", trim(col("name"))) \
    .withColumn("phone", regexp_replace(col("phone"), "[^0-9]", "")) \
    .withColumn("phone", when(length(col("phone")) == 11, col("phone")).otherwise(None)) \
    .withColumn("email", when(col("email").rlike("^[^@]+@[^@]+\\.[^@]+$"), col("email")).otherwise(None)) \
    .filter(col("name").isNotNull() & col("name").notEqual(""))

df_cleaned.show()
# +---+----+-----------+-----------------+----------+
# | id|name|      phone|            email|      date|
# +---+----+-----------+-----------------+----------+
# |  1|张三|13800138001|hello@example.com|2024-01-15|
# |  3|王五|13800138003|             null|  20240125|
# +---+----+-----------+-----------------+----------+

spark.stop()