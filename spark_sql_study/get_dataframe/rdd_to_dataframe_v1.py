from pyspark.sql import SparkSession

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
    df = spark.createDataFrame(rdd2, ["name", "age"])
    df.printSchema()
    df.show()

    # sql
    df.createOrReplaceTempView("people")
    spark.sql("""
        select * 
        from people
        where age < 30
    """).show()