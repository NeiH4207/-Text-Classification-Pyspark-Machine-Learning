# Configurations for Spark MLlib

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = dotdict(value)
            self[key] = value

configs = {
    'spark': dotdict({
        'master': 'local[*]',
        'app_name': 'Spark MLlib',
        'spark_home': '/usr/local/spark',
        'spark_log_level': 'WARN',
        'spark_log_file': 'spark.log',
        'spark_log_max_size': '10240',
        'spark_log_max_retained_size': '10240',
        'spark_log_enable_compression': 'true',
        'spark_log_compression_codec': 'snappy',
        'spark_log_file_max_backups': '10',
        'spark_log_file_max_retained_size': '10240',
        'data_path': 'data/',
        'data_file': 'IMDB.csv',
    })
}