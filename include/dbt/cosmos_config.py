from cosmos.config import ProfileConfig, ProjectConfig, ExecutionConfig
from pathlib import Path
import os

profile_config = ProfileConfig(
    profile_name='bedsheets',
    target_name='dev',
    profiles_yml_filepath=Path('/usr/local/airflow/include/dbt/profiles.yml')
)

project_config = ProjectConfig(
    dbt_project_path='/usr/local/airflow/include/dbt/',
)

DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"

execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)