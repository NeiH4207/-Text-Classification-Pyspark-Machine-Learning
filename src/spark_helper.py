
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import Row, SQLContext
from pyspark.sql.types import *

class Spark():
    def __init__(self, config=None):
        if config is not None:
            self.connect(config)
    
    def connect(self, config):
        self.sc = SparkContext(appName=config['app_name'])
        self.sqlContext = SQLContext(self.sc)
        print("Spark Context Created")
        return True
        
    def close(self):
        self.sc.stop()
        return True
    
    def query(self, query):
        return self.sc.sql(query)
    
    def read_csv(self):
        return self.sc.read.csv(self.config.data_path + self.config.data_file, 
                                   sep=',',
                                   header=True) 
        
    def get_column_names(self, data):
        return Row(data.columns.values.tolist())
    
    def parallelize(self, data):
        column_name = self.get_column_names(data)
        _data = self.sc.parallelize(data.values.tolist())
        return _data.map(lambda r: column_name(*r)).toDF()
    def pandas_to_df(self, df):
        return self.sqlContext.createDataFrame(df)
    
    def load_hdfs(self, table_name, path):
        self.sc.read.load(path, format="csv", header=True, inferSchema=True).createOrReplaceTempView(table_name)
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
        self.sc.catalog.dropTempView(table_name)
        return True
    
    def get_table(self, table_name):
        return self.sc.table(table_name)
    
    def get_table_names(self):
        return self.sc.catalog.listTables()
    
    def get_table_schema(self, table_name):
        return self.sc.table(table_name).schema
    