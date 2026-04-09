from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("Python Spark SQL basic example")
            .master("local[*]")
            .getOrCreate()
    )
    SC = spark.sparkContext
    df = spark.read.schema("name STRING,age INT,city STRING,salary INT").json("../../../resources/people.json")
    # 注册成表
    df.createTempView("people_1")
    df.createOrReplaceTempView("people_2")
    df.createGlobalTempView("people_3")
    spark.sql("""
        select * 
        from people_1
        where age > 30
    """).show()
    spark.sql("""
        select *
        from people_2
        where city = "北京"
    """).show()
    spark.sql("""
        select * 
        from global_temp.people_3
        where age > 25
    """).show()

