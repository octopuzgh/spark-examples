from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, to_timestamp, cast
from pyspark.sql.types import IntegerType, DoubleType, StringType

spark = SparkSession.builder.appName("cast").master("local[*]").getOrCreate()

# 准备数据
data = [
    ("1", "25", "2024-01-15", "2024-01-15 10:30:00", "3.14"),
    ("2", "30", "2024/01/20", "2024-01-20 15:45:00", "2.71"),
    ("3", "abc", "invalid", "invalid", "not_number")
]
df = spark.createDataFrame(data, ["id", "age", "date_str", "timestamp_str", "pi_str"])
df.printSchema()
# root
#  |-- id: string (nullable = true)
#  |-- age: string (nullable = true)
#  |-- date_str: string (nullable = true)
#  |-- timestamp_str: string (nullable = true)
#  |-- pi_str: string (nullable = true)

# ============ cast()：类型转换 ============
# 字符串转整数
df.withColumn("age_int", col("age").cast(IntegerType())).show()
# +---+---+----------+-------------------+--------+-------+
# | id|age|  date_str|      timestamp_str|   pi_str|age_int|
# +---+---+----------+-------------------+--------+-------+
# |  1| 25|2024-01-15|2024-01-15 10:30:00|    3.14|     25|
# |  2| 30|2024/01/20|2024-01-20 15:45:00|    2.71|     30|
# |  3|abc|   invalid|           invalid|not_number|   null|  ← abc 无法转换，变成 null
# +---+---+----------+-------------------+--------+-------+

# 字符串转小数
df.withColumn("pi_double", col("pi_str").cast(DoubleType())).show()
# +---+---+----------+-------------------+--------+------------------+
# | id|age|  date_str|      timestamp_str|   pi_str|        pi_double|
# +---+---+----------+-------------------+--------+------------------+
# |  1| 25|2024-01-15|2024-01-15 10:30:00|    3.14|              3.14|
# |  2| 30|2024/01/20|2024-01-20 15:45:00|    2.71|              2.71|
# |  3|abc|   invalid|           invalid|not_number|              null|
# +---+---+----------+-------------------+--------+------------------+

# 链式转换
df.withColumn("age_int", col("age").cast("int")).withColumn("pi_float", col("pi_str").cast("float"))

# ============ to_date()：字符串转日期 ============
# 自动识别格式
df.withColumn("date", to_date(col("date_str"))).show()
# +---+---+----------+-------------------+--------+----------+
# | id|age|  date_str|      timestamp_str|   pi_str|      date|
# +---+---+----------+-------------------+--------+----------+
# |  1| 25|2024-01-15|2024-01-15 10:30:00|    3.14|2024-01-15|
# |  2| 30|2024/01/20|2024-01-20 15:45:00|    2.71|      null|  ← 格式不匹配
# |  3|abc|   invalid|           invalid|not_number|      null|
# +---+---+----------+-------------------+--------+----------+

# 指定格式转换
df.withColumn("date", to_date(col("date_str"), "yyyy/MM/dd")).show()
# +---+---+----------+-------------------+--------+----------+
# | id|age|  date_str|      timestamp_str|   pi_str|      date|
# +---+---+----------+-------------------+--------+----------+
# |  1| 25|2024-01-15|2024-01-15 10:30:00|    3.14|      null|
# |  2| 30|2024/01/20|2024-01-20 15:45:00|    2.71|2024-01-20|
# |  3|abc|   invalid|           invalid|not_number|      null|
# +---+---+----------+-------------------+--------+----------+

# ============ to_timestamp()：字符串转时间戳 ============
df.withColumn("timestamp", to_timestamp(col("timestamp_str"))).show()
# +---+---+----------+-------------------+--------+-------------------+
# | id|age|  date_str|      timestamp_str|   pi_str|          timestamp|
# +---+---+----------+-------------------+--------+-------------------+
# |  1| 25|2024-01-15|2024-01-15 10:30:00|    3.14|2024-01-15 10:30:00|
# |  2| 30|2024/01/20|2024-01-20 15:45:00|    2.71|2024-01-20 15:45:00|
# |  3|abc|   invalid|           invalid|not_number|               null|
# +---+---+----------+-------------------+--------+-------------------+

spark.stop()