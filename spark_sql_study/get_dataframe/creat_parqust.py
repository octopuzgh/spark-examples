from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# 创建 SparkSession
spark = SparkSession.builder \
    .appName("GeneratePeopleParquet") \
    .master("local[*]") \
    .getOrCreate()

# 数据
data = [
    ("张三", 25, "北京", 15000),
    ("李四", 30, "上海", 18000),
    ("王五", 28, "广州", 12000),
    ("赵六", 35, "深圳", 25000),
    ("周婷", 22, "北京", 10000),
    ("吴迪", 29, "上海", 16000),
    ("郑爽", 27, "广州", 11000),
    ("林晨", 31, "深圳", 22000),
    ("郭峰", 33, "北京", 20000),
    ("唐雅", 26, "上海", 14000)
]

# 定义 Schema
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("salary", IntegerType(), True)
])

# 创建 DataFrame
df = spark.createDataFrame(data, schema=schema)

# 显示数据
print("原始数据：")
df.show()

# 方法1：使用 coalesce(1) 合并为单分区（推荐）
df.coalesce(1).write.mode("overwrite").parquet("../../../resources/people.parquet")



print("✅ 已生成单个 Parquet 文件: people.parquet")



spark.stop()