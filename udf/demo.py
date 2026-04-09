from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, IntegerType

# 创建 SparkSession
spark = SparkSession.builder \
    .appName("UDF Example") \
    .master("local[*]") \
    .getOrCreate()

# 准备数据
data = [
    ("张三", 25, "北京"),
    ("李四", 30, "上海"),
    ("王五", 28, "广州"),
    ("赵六", 35, "深圳")
]
df = spark.createDataFrame(data, ["name", "age", "city"])
df.show()
# +----+---+----+
# |name|age|city|
# +----+---+----+
# |张三| 25|北京|
# |李四| 30|上海|
# |王五| 28|广州|
# |赵六| 35|深圳|
# +----+---+----+

# ============ 方式1：注册 UDF ============
# 定义一个普通 Python 函数
def age_group(age):
    if age < 30:
        return "青年"
    else:
        return "中年"

# 注册为 UDF
age_group_udf = udf(age_group, StringType())

# 使用 UDF
df.withColumn("age_group", age_group_udf(col("age"))).show()
# +----+---+----+---------+
# |name|age|city|age_group|
# +----+---+----+---------+
# |张三| 25|北京|     青年|
# |李四| 30|上海|     中年|
# |王五| 28|广州|     青年|
# |赵六| 35|深圳|     中年|
# +----+---+----+---------+

# ============ 方式2：使用装饰器（推荐） ============
@udf(StringType())
def age_group_v2(age):
    if age < 30:
        return "青年"
    elif age < 40:
        return "中年"
    else:
        return "老年"

df.withColumn("age_group", age_group_v2(col("age"))).show()

# ============ 方式3：处理多个列 ============
@udf(StringType())
def greeting(name, city):
    return f"你好，我是{name}，来自{city}"

df.withColumn("greeting", greeting(col("name"), col("city"))).show()
# +----+---+----+----------------------+
# |name|age|city|              greeting|
# +----+---+----+----------------------+
# |张三| 25|北京|你好，我是张三，来自北京|
# |李四| 30|上海|你好，我是李四，来自上海|
# |王五| 28|广州|你好，我是王五，来自广州|
# |赵六| 35|深圳|你好，我是赵六，来自深圳|
# +----+---+----+----------------------+

# ============ 方式4：返回整数类型 ============
@udf(IntegerType())
def double_age(age):
    return age * 2

df.withColumn("age_double", double_age(col("age"))).show()
# +----+---+----+---------+
# |name|age|city|age_double|
# +----+---+----+---------+
# |张三| 25|北京|       50|
# |李四| 30|上海|       60|
# |王五| 28|广州|       56|
# |赵六| 35|深圳|       70|
# +----+---+----+---------+

# ============ 复杂示例：判断手机号段 ============
data2 = [
    ("张三", "13800138001"),
    ("李四", "18800138002"),
    ("王五", "19900138003"),
    ("赵六", "1234567890")
]
df2 = spark.createDataFrame(data2, ["name", "phone"])

@udf(StringType())
def phone_carrier(phone):
    if not phone or len(phone) != 11:
        return "无效号码"
    if phone.startswith("13"):
        return "中国联通"
    elif phone.startswith("18"):
        return "中国移动"
    elif phone.startswith("19"):
        return "中国电信"
    else:
        return "未知运营商"

df2.withColumn("carrier", phone_carrier(col("phone"))).show()
# +----+-----------+--------+
# |name|      phone| carrier|
# +----+-----------+--------+
# |张三|13800138001|中国联通|
# |李四|18800138002|中国移动|
# |王五|19900138003|中国电信|
# |赵六|1234567890|无效号码|
# +----+-----------+--------+

# ============ 注册为临时函数（用于 SQL） ============
spark.udf.register("age_group_sql", age_group, StringType())

df.createOrReplaceTempView("people")
spark.sql("""
    SELECT name, age, city, age_group_sql(age) as age_group
    FROM people
""").show()
# +----+---+----+---------+
# |name|age|city|age_group|
# +----+---+----+---------+
# |张三| 25|北京|     青年|

# |李四| 30|上海|     中年|
# |王五| 28|广州|     青年|
# |赵六| 35|深圳|     中年|
# +----+---+----+---------+

spark.stop()