# PySpark for Machine Learning
from spark_helper import Spark
from configs import configs

def main():
    spark = Spark(configs['spark'])
    spark.connect()
    data = spark.read_csv()
    print(data[:2])
    spark.close()
    
if __name__ == "__main__":
    main()