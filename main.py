# PySpark for Machine Learning
from src.spark_helper import Spark
from configs import configs
from src.data_helper import Processor
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from src.spark_mlib import SparkMLib

def main():
    proc = Processor()
    spark = Spark()
    spark.connect(configs['spark'])
    smlib = SparkMLib()
    data = pd.read_csv(configs['data-path'] + configs['data-file'], nrows=100)
    
    ''' preprocessing '''
    data['review'] = data['review'].apply(lambda x: proc.finalpreprocess(x))
    one_hot_labels = proc.one_hot_encode(data['sentiment'].unique())
    data['label'] = data['sentiment'].apply(lambda x: one_hot_labels[x])
    
    ''' visualize data '''
    # plt.figure(figsize = (8,4), dpi = 100)
    # sns.countplot(data = data, x = 'label')
    # # plt.xticks(rotation = 90)
    # plt.show()
    print(data.head(65))
    data = spark.pandas_to_df(data)
    
    train, test = data.randomSplit([0.8, 0.2], seed=12345)
    ''' Create model and pipeline '''
    model, pramGrid = smlib.get_model('lr')
    tokenizer = smlib.get_tokenizer('review', 'words')
    pipeline = smlib.get_pipeline(model, tokenizer, pramGrid)
    pipeline.fit(train)
    predictions = model.transform(test) 
    spark.close()
    
if __name__ == "__main__":
    main()