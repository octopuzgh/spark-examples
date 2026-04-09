from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("ParquetToDataFrame")
            .master("local[*]")
            .getOrCreate()
    )
    SC = spark.sparkContext


    df = spark.read.parquet("../../../resources/people.parquet/people.parquet")

    df.printSchema()
    df.show()