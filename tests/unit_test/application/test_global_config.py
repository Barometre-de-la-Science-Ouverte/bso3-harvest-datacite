import json
import os
from dotenv import load_dotenv

# Project path
PROJECT_DIRNAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), "application")

# debug level
DEBUG_LEVEL = 1
# destination folder ovh

# Output file suffixes
COMPRESSION_SUFFIX = '.gz'
METADATA_SUFFIX = '.json'
PUBLICATION_SUFFIX = '.pdf'
SOFTCITE_SUFFIX = '.software.json'
GROBID_SUFFIX = '.tei.xml'

# folder in OVH
DATACITE_DUMP = 'datacite'
RAW_DATACITE_DUMP = 'raw'
PROCESSED_DATACITE_DUMP = 'processed'

# folder in project
RAW_DUMP_FOLDER_NAME = ""
PROCESSED_DUMP_FOLDER_NAME = "test_dois"
GLOBAL_AFFILIATION_FILE_NAME = "global_affiliations.csv"
DETAILED_AFFILIATION_FILE_NAME = "detailed_affiliations.csv"


def get_harvester_config() -> dict:
    load_environment_variables()

    test_config_harvester = {'swift': {}}

    # Add env var secrets & pwd for swift - ovh
    test_config_harvester['swift']['os_username'] = os.getenv('OS_USERNAME2')
    test_config_harvester['swift']['os_password'] = os.getenv('OS_PASSWORD2')
    test_config_harvester['swift']['os_user_domain_name'] = os.getenv('OS_USER_DOMAIN_NAME')
    test_config_harvester['swift']['os_project_domain_name'] = os.getenv('OS_PROJECT_DOMAIN_NAME')
    test_config_harvester['swift']['os_project_name'] = os.getenv('OS_PROJECT_NAME')
    test_config_harvester['swift']['os_project_id'] = os.getenv('OS_PROJECT_ID')
    test_config_harvester['swift']['os_region_name'] = os.getenv('OS_REGION_NAME')
    test_config_harvester['swift']['os_auth_url'] = os.getenv('OS_AUTH_URL')
    # ovh folder
    test_config_harvester['datacite_container'] = DATACITE_DUMP
    test_config_harvester['raw_datacite_container'] = RAW_DATACITE_DUMP
    test_config_harvester['processed_datacite_container'] = PROCESSED_DATACITE_DUMP

    test_config_harvester['is_level_debug'] = DEBUG_LEVEL
    # local dump folder
    test_config_harvester['raw_dump_folder_name'] = os.path.join(PROJECT_DIRNAME, RAW_DUMP_FOLDER_NAME)
    test_config_harvester['processed_dump_folder_name'] = os.path.join(PROJECT_DIRNAME, PROCESSED_DUMP_FOLDER_NAME)
    test_config_harvester['global_affiliation_file_name'] = os.path.join(
        test_config_harvester['processed_dump_folder_name'],
        GLOBAL_AFFILIATION_FILE_NAME)
    test_config_harvester['detailed_affiliation_file_name'] = os.path.join(
        test_config_harvester['processed_dump_folder_name'],
        DETAILED_AFFILIATION_FILE_NAME)

    print(f"config_harvester {test_config_harvester}")

    return test_config_harvester


def load_environment_variables() -> None:
    try:
        load_dotenv()
    except Exception as e:
        print(f'File .env not found: {str(e)}')


test_config_harvester = get_harvester_config()