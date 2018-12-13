#Spark-Apriori
An implementation of apriori algorithm under spark platform.

##Usage
spark-submit -master spark://Ubuntu:7077 apriori.py input output min_sup

Note: input format should be the same as the test data.

##Configuration: Anaconda3 + Spark-2.4.0 + Pycharm
File-->Settings-->Project-->Project Structure: 

Add the .zip file in $SPARK_HOME/python/lib/ to Content Root
* pyspark.zip

* py4j-0.10.7-src.zip

#
Edit Configurations:

Add environment variables
* SPARK_HOME=/usr/local/spark-2.4.0

* PYTHONPATH=$SPARK_HOME/python

* PYSPARK_PYTHON=/home/xxx/anaconda3/bin/python