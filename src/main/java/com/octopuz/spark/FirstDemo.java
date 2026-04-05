package com.octopuz.spark;

import org.apache.spark.sql.SparkSession;

public class FirstDemo {
    public static void main(String[] args) {
        SparkSession spark = SparkSession.builder()
                .appName("FirstDemo")
                .master("local[*]")
                .getOrCreate();

        System.out.println("Spark 版本: " + spark.version());
        System.out.println("Spark 启动成功！");

        spark.stop();
    }
}