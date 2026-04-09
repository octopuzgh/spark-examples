from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("Python Spark SQL basic example")
            .master("local[*]")
            .getOrCreate()
    )
    SC = spark.sparkContext


    df = spark.read.schema("name STRING,age INT,city STRING,salary INT").csv("../../../resources/people.csv",sep=",",header=True)

    df.printSchema()
    df.show()