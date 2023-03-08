from django.shortcuts import render
from .models import TableA

from google.cloud import bigquery
import pandas as pd

credential_path = "E:\Ramnagar\project-bps-326409-846c39e5abe4.json"
import os   
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# Create your views here.

# from google.cloud import bigquery
# import pandas as pd

# sql = "SELECT * FROM GoogleAds"
# query_job2 = client.query(sql)
# df_prevp = query_job2.to_dataframe()



def index(request):
    
    return render(request, "index.html") 



def import_data_from_TableA(request):

    # get data from TableA from google Cloud to dataframe
    
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig()
    job_config.use_legacy_sql = True
    
    
    sql = "SELECT visitID, Date FROM [project-bps-326409.bpsDB.TableA] LIMIT 100"
    query_job2 = client.query(sql, job_config=job_config)
    df = query_job2.to_dataframe()


    for index, rw in df.iterrows():

        t1 = TableA(rw["visitID"], rw["Date"])
        t1.save()
        

    d = {}
    d['name'] = "Data imported to local database table TableA" 
    return render(request, "create_table.html", {'d':d}) 


def create_table(tabel_name):
    
    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_id = "project-bps-326409.bpsDB.{0}".format(tabel_name)


    sql = """
        CREATE OR REPLACE TABLE {0} as
        SELECT visitID, Date
        FROM 
        bigquery-public-data.google_analytics_sample.ga_sessions_20170101 
        limit 100
    """.format(table_id)

    # Start the query, passing in the extra configuration.
    query_job = client.query(sql)  # Make an API request.
    query_job.result()  # Wait for the job to complete.

    return table_id



def make_tableA(request):
    
    d = {}
    d['name'] = "Created table " + create_table('TableA')
    return render(request, "create_table.html", {'d':d}) 


def make_table_googleAds(request):
    
    d = {}
    d['name'] = create_table('GoogleAds')
    return render(request, "create_table.html", {'d':d}) 


def alter_googleads_table(request):

    client = bigquery.Client()

    tabel_name = 'GoogleAds'
    table_id = "project-bps-326409.bpsDB.{0}".format(tabel_name)


    sql = """
        ALTER TABLE {0} ADD COLUMN ROAS DECIMAL
        
    """.format(table_id)

    # Start the query, passing in the extra configuration.
    query_job = client.query(sql)  # Make an API request.
    query_job.result()  # Wait for the job to complete.

    d = {}
    d['name'] = "Columns added in "+table_id
    return render(request, "create_table.html", {'d':d})



def calculate_cpa(total_cost, total_conversions):

    # Average cost per action (CPA) is calculated by dividing
    # the total cost of conversions by the total number of conversions. 

    cpa = 0

    if  total_conversions > 0:
        cpa = total_cost / total_conversions
    
    return cpa


def update_metrics_in_google_ads_table(request):

    
    client = bigquery.Client()
    tabel_name = 'GoogleAds'
    table_id = "project-bps-326409.bpsDB.{0}".format(tabel_name)


    # get data from GoogleAds to dataframe
    # sql = "SELECT * FROM {0}".format(table_id)
    # query_job2 = client.query(sql)
    # df = query_job2.to_dataframe()


    #  get totl coversions and total cost
    cpa = calculate_cpa(6, 2)

    sql = """
        UPDATE TABLE {0} SET CPA = 2  
    """.format(table_id)
    
    # Update the table with the calculated cpa data
    job_config = bigquery.QueryJobConfig()
    job_config.use_legacy_sql = True
    
    query_job = client.query(sql, job_config=job_config)
    
    query_job.result()  

    d = {}
    d['name'] = "updated data in "+table_id
    return render(request, "create_table.html", {'d':d})



