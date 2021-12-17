from os import pipe
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from pyspark.ml import Pipeline, param
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.sql import SparkSession

from src.spark_helper import Spark
from configs import configs
    
class SparkMLib:
    def __init__(self):
        pass

    def get_tokenizer(self, inputCol, outputCol):
        inputCol = inputCol
        outputCol = outputCol
        tokernizer = Tokenizer(inputCol=inputCol, outputCol=outputCol)
        return tokernizer
    
    def get_model(self, model_name):
        if model_name == 'lr':
            model = LogisticRegression(maxIter=50)
            param = ParamGridBuilder()\
                .addGrid(model.regParam, [0.1, 0.01])\
                .addGrid(model.elasticNetParam, [0.0, 0.5, 1.0])
            return model, param
        elif model_name == 'rf':
            model = RandomForestClassifier(numTrees=10)
            param = ParamGridBuilder()\
                .addGrid(model.maxDepth, [2, 3, 4])\
                .addGrid(model.maxBins, [20, 40])
            return model, param
        else:
            print('model not found')
    
    def get_pipeline(self, model, tokenizer, paramGrid, cross_validation=False):
        hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
        pipeline = Pipeline(stages=[tokenizer, hashingTF, model])
        
        if cross_validation:
            cv = CrossValidator(estimator=pipeline, 
                                estimatorParamMaps=paramGrid, 
                                evaluator=MulticlassClassificationEvaluator(),
                                numFolds=3)
            return cv
        else:
            return pipeline
        
def main():
    pass
    
if __name__ == "__main__":
    main()