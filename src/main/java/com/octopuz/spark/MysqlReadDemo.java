package com.octopuz.spark;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

public class MysqlReadDemo {
    public static void main(String[] args) {
        SparkSession spark = SparkSession.builder()
                .appName("MysqlReadDemo")
                .master("local[*]")
                .getOrCreate();

        // 读取虚拟机 MySQL 数据
        Dataset<Row> df = spark.read()
                .format("jdbc")
                .option("url", "jdbc:mysql://192.168.152.131:3306/employee_performance")
                .option("dbtable", "employee")
                .option("user", "octopuz_remote")
                .option("password", "Octopuz@123")
                .option("driver", "com.mysql.cj.jdbc.Driver")
                .load();

        System.out.println("=== 员工数据 ===");
        df.show();

        // 统计各部门人数
        df.createOrReplaceTempView("emp");
        Dataset<Row> result = spark.sql(
                "SELECT department, COUNT(*) as count " +
                "FROM emp " +
                "GROUP BY department"
        );
        System.out.println("=== 部门人数统计 ===");
        result.show();

        spark.stop();
    }
}