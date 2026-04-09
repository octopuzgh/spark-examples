from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = (
        SparkSession.builder
            .appName("窗口函数")
            .master("local[*]")
            .getOrCreate()
    )
    SC = spark.sparkContext
    df = spark.read.json("../../resources/people.json")
    df.createTempView("people")

    # 窗口函数
    spark.sql("""
            select *, 
                   row_number() over(partition by city order by salary desc) as rank,
                   avg(salary) over(partition by city) as avg_city_salary
            from people
        """).show()

    spark.stop()
    # +---+----+----+------+----+---------------+
    # | age | city | name | salary | rank | avg_city_salary |
    # +---+----+----+------+----+---------------+
    # | 30 | 上海 | 李四 | 18000 | 1 | 16000.0 |
    # | 29 | 上海 | 吴迪 | 16000 | 2 | 16000.0 |
    # | 26 | 上海 | 唐雅 | 14000 | 3 | 16000.0 |
    # | 33 | 北京 | 郭峰 | 20000 | 1 | 15000.0 |
    # | 25 | 北京 | 张三 | 15000 | 2 | 15000.0 |
    # | 22 | 北京 | 周婷 | 10000 | 3 | 15000.0 |
    # | 28 | 广州 | 王五 | 12000 | 1 | 11500.0 |
    # | 27 | 广州 | 郑爽 | 11000 | 2 | 11500.0 |
    # | 35 | 深圳 | 赵六 | 25000 | 1 | 23500.0 |
    # | 31 | 深圳 | 林晨 | 22000 | 2 | 23500.0 |
    # +---+----+----+------+----+---------------+
