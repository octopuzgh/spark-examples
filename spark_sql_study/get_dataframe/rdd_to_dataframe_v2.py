from struct import Struct
from xml.dom.minicompat import StringTypes

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType

if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("RddToDataFrame")
            .master("local[*]")
            .getOrCreate()
    )
    SC = spark.sparkContext
    rdd = SC.textFile("../../../resources/people.txt")
    rdd2 = (rdd
            .map(lambda x: x.split(","))
            .map(lambda x: (x[0], int(x[1]))))
    schema = (StructType()
              .add("name", StringType(), True)
              .add("age", IntegerType(), True))
    df = spark.createDataFrame(rdd2, schema)
    df.printSchema()
    df.show()
