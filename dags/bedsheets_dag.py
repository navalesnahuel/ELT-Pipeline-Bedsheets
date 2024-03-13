from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from include.dbt.cosmos_config import project_config, profile_config, execution_config
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from cosmos.constants import LoadMode, TestBehavior
from astro.sql.table import Table, Metadata
from airflow.decorators import dag, task
from astro.constants import FileType
from datetime import datetime
from astro import sql as aql
from astro.files import File
import os

queries = {
    'categories': 'SELECT * FROM public.categories;',
    'customers': 'SELECT * FROM public.customers;',
    'materials': 'SELECT * FROM public.materials;',
    'orders': 'SELECT * FROM public.orders;',
    'products': 'SELECT * FROM public.products;',
    'sizes': 'SELECT * FROM public.sizes;'
}


@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['bedsheets'],
)

def bedsheets():
    postgres_to_gcs = {}
    gcs_to_raw = {}

    create_bucket = GCSCreateBucketOperator(
        task_id ='create_bucket',
        bucket_name='bedsheets-data',
        storage_class="STANDARD",
        location="US",
        project_id="project-412401",
        gcp_conn_id="gcp",
    )

    for table, query in queries.items():
        postgres_to_gcs[table] = PostgresToGCSOperator(
            task_id=f'extract_{table}_data',
            sql=query,
            bucket='bedsheets-data',
            filename=f'{table}.csv',
            export_format='CSV',
            postgres_conn_id='postgres_default',
            gcp_conn_id='gcp',
        )


    create_bedsheets_ds = BigQueryCreateEmptyDatasetOperator(
        task_id='create_bedsheets_ds',
        dataset_id='raw_bedsheets',
        gcp_conn_id='gcp',
    )
    
    for table in ['categories', 'customers', 'materials', 'orders', 'products', 'sizes']:
        gcs_to_raw[table] = aql.load_file(
            task_id=f'gcs_{table}_to_raw',
            input_file=File(
                f'gs://bedsheets-data/{table}.csv',
                conn_id='gcp',
                filetype=FileType.CSV,
            ),
            output_table=Table(
                name=f'raw_{table}',
                conn_id='gcp',
                metadata=Metadata(schema='raw_bedsheets')
            ),
            use_native_support=False,
        )
        

    dbt_task = DbtTaskGroup(
        group_id="transform_data",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            test_behavior=TestBehavior.AFTER_EACH,
            select=['path:models/']
        )
    )

    for table, task in postgres_to_gcs.items():
        create_bucket >> task >> create_bedsheets_ds >> gcs_to_raw[table] >> dbt_task

bedsheets()
