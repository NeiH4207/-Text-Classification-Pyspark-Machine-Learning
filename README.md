# PySparkML_20211

### Install Python Lib
```sh
conda activate 'your environment'
pip install -r requirements.txt
```

## Datasource

### Creditcard

https://www.kaggle.com/pierra/credit-card-dataset-svm-classification/data

### Movie classification

https://www.kaggle.com/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

Note: `store the dataset in 'data/' folder before starting`

### Crawl reviews Amazon Web

```sh
cd amazon-python-scrapy-scraper
scrapy crawl amazon -o ../data/review_dataset.csv
```