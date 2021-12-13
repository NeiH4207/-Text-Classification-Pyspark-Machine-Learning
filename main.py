# PySpark for Machine Learning

from pyspark.sql import SparkSession
from hdfs import Config
from configs import configs

class Spark():
    def __init__(self, config):
        self.config = config
    
    def connect(self):
        self.spark = SparkSession.builder.appName(self.config.app_name).getOrCreate()
        return self.spark
        
    def close(self):
        self.spark.stop()
        return True
    
    def query(self, query):
        return self.spark.sql(query)
    
    def read_csv(self):
        return self.spark.read.csv(self.config.data_path + self.config.data_file, 
                                   header=True)
    
    def load_hdfs(self, table_name, path):
        self.spark.read.load(path, format='csv', header=True, inferSchema=True).createOrReplaceTempView(table_name)
        return True
    
    def write(self, df, path):
        df.write.csv(path)
        return True
    
    def show(self, df):
        df.show()
        return True
    
    def create_table(self, df, table_name):
        df.createOrReplaceTempView(table_name)
        return True
    
    def drop_table(self, table_name):
        self.spark.catalog.dropTempView(table_name)
        return True
    
    def get_table(self, table_name):
        return self.spark.table(table_name)
    
    def get_table_names(self):
        return self.spark.catalog.listTables()
    
    def get_table_schema(self, table_name):
        return self.spark.table(table_name).schema
    
def main():
    spark = Spark(configs['spark'])
    spark.connect()
    data = spark.read_csv()
    print(data[:2])
    spark.close()
    
if __name__ == "__main__":
    main()