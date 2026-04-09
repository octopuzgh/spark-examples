from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType

if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("Python Spark SQL basic example")
            .master("local[*]")
            .getOrCreate()
    )

    sc = spark.sparkContext
    schema=(
        StructType().add("data", StringType(), True))
    df=(
        spark.read.format("text")
        .schema(schema= schema)
        .load("../../../resources/people.txt"))
    df.printSchema()
    df.show()
