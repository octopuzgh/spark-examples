#写出Dataframe
from pyspark.sql import SparkSession
if __name__ == '__main__':
    spark = SparkSession.builder.appName("writeDataFrame").master("local[*]").getOrCreate()
    SC = spark.sparkContext
    df = spark.read.json("../../../resources/people.json")
    # df.write.csv("../../resources/people", mode="overwrite")
    # df.write.json("../../resources/people", mode="overwrite")
    # df.write.parquet("../../resources/people", mode="overwrite")
    # df.write.orc("../../resources/people", mode="overwrite")
    df.write.format("orc").save("../../../resources/people.orc", mode="overwrite")
