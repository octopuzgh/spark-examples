from pyspark.sql import SparkSession
if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("Python Spark SQL basic example")
            .master("local[*]")
            .getOrCreate()
    )
    SC = spark.sparkContext


    df = spark.read.csv("example",sep=",",header=False)
    df2 = df.toDF("name", "age", "city")
    df2.printSchema()
    df2.show()
    #sql
    df2.createTempView("people")
    spark.sql("""
        select * 
        from people 
        where name='张三'
        
    """).show()
    #dsl
    df2.filter(df2.name == "张三").show()
