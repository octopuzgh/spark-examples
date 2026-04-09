from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("Python Spark SQL basic example")
            .master("local[*]")
            .getOrCreate()
    )
    sc = spark.sparkContext
    #df=spark.read.json("../../resources/people.json")
    df = spark.read.format("json").load("../../../resources/people.json")
    df.printSchema()
    df.show()