from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("RddToDataFrame")
            .master("local[*]")
            .getOrCreate()
    )
    SC = spark.sparkContext
    df = spark.read.schema("name STRING,age INT,city STRING,salary INT").json("../../../resources/people.json")

    df.select("name","age").show()

    # filter
    df.filter(df.age > 30).show()
    # where
    df.where(df.age > 30).show()
    # group By
    df.groupBy("city").count().show() 