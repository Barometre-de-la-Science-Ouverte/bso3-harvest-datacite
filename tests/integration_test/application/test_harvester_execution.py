from time import sleep
from unittest import TestCase

from datetime import datetime

from os import getenv

from subprocess import run

from adapters.databases.postgres_session import PostgresSession
from adapters.databases.harvest_state_repository import HarvestStateRepository
from adapters.databases.harvest_state_table import HarvestStateTable

from application.harvester import Harvester


class TestHarvester(TestCase):
    harvest_state_repository = None
    postgres_session = None

    @classmethod
    def setUpClass(self):
        host: str = getenv("DB_POSTGRES_HOST")
        port: int = getenv("DB_POSTGRES_PORT")
        username: str = getenv("DB_POSTGRES_USER")
        password: str = getenv("DB_POSTGRES_PASSWORD")
        database_name: str = getenv("DB_POSTGRES_NAME")

        self.postgres_session: PostgresSession = PostgresSession(host, port, username, password, database_name)
        self.harvest_state_repository: HarvestStateRepository = HarvestStateRepository(self.postgres_session)

        self.target_directory: str = "test_download_directory"

        self.harvester: Harvester = Harvester(self.harvest_state_repository)

    def setUp(self):
        # create tables
        HarvestStateTable.createTable(self.postgres_session.getEngine())

    def tearDown(self):
        # drop tables
        HarvestStateTable.dropTable(self.postgres_session.getEngine())

        # delete files downloaded
        cmd = ["rm", "-rf", self.target_directory]

        run(cmd)

    def test_launching_download_with_thread(self):
        # Given
        start_date: datetime = datetime.strptime("2019-05-01", "%Y-%m-%d")
        end_date: datetime = datetime.strptime("2019-05-01 00:59:59", "%Y-%m-%d %H:%M:%S")
        interval: str = "minute"

        harvest_state_expected: HarvestStateTable = HarvestStateTable(start_date, end_date, "done", self.target_directory, 1, 0, 60, False, interval)

        # When
        downloaded: bool = self.harvester.download(self.target_directory, start_date, end_date, interval, use_thread=True)[0]

        sleep(60)

        results = self.harvest_state_repository.get()

        print(f"results {results}")

        # Then
        self.assertIs(downloaded, True)
        self.assertEqual(results[0], harvest_state_expected)

    def test_launching_download_without_thread(self):
        # Given
        start_date: datetime = datetime.strptime("2019-05-01", "%Y-%m-%d")
        end_date: datetime = datetime.strptime("2019-05-01 00:59:59", "%Y-%m-%d %H:%M:%S")
        interval: str = "minute"

        harvest_state_expected: HarvestStateTable = HarvestStateTable(start_date, end_date, "done", self.target_directory, 1, 0, 60, False, interval)

        # When
        print(f" self target dir {self.target_directory}")

        downloaded: bool = self.harvester.download(self.target_directory, start_date, end_date, interval, use_thread=False)[0]
        results = self.harvest_state_repository.get()

        print(f"results {results}")

        # Then
        self.assertIs(downloaded, True)
        self.assertEqual(results[0], harvest_state_expected)
