import pytest
from parsect.utils.amazon_s3 import S3Util
import parsect.constants as constants
import os
import json
import pathlib

PATHS = constants.PATHS
AWS_CRED_DIR = PATHS["AWS_CRED_DIR"]
TESTS_DIR = PATHS["TESTS_DIR"]


@pytest.fixture
def setup_s3_util():
    aws_config_filename = os.path.join(AWS_CRED_DIR, "aws_s3_credentials.json")
    util = S3Util(aws_cred_config_json_filename=aws_config_filename)
    return util


class TestS3Util:
    def test_credentials_file_not_empty(self, setup_s3_util):
        aws_util = setup_s3_util
        config_filename = aws_util.aws_cred_config_json_filename
        with open(config_filename, "r") as fp:
            cred = json.load(fp)

        assert cred["aws_access_key_id"] is not None
        assert cred["aws_access_secret"] is not None
        assert cred["region"] is not None

    def test_credentials_not_empty(self, setup_s3_util):
        aws_util = setup_s3_util
        aws_credentials = aws_util.credentials
        assert aws_credentials.access_key is not None
        assert aws_credentials.access_secret is not None
        assert aws_credentials.region is not None
        assert aws_credentials.bucket_name is not None

    def test_s3_connects_succesfully(self, setup_s3_util):
        aws_util = setup_s3_util
        try:
            aws_util.get_client()
        except:
            pytest.fail("Failed to get s3 client")

    def test_s3_resource_gets_successfully(self, setup_s3_util):
        aws_util = setup_s3_util
        try:
            aws_util.get_resource()
        except:
            pytest.fail("Failed to get s3 resource")

    def test_s3_bucket_names(self, setup_s3_util):
        """
        Test whether s3 has expected buckets
        """
        aws_util = setup_s3_util
        client = aws_util.s3_client
        bucket_names = []
        for bucket_dict in client.list_buckets().get("Buckets"):
            bucket_name = bucket_dict["Name"]
            bucket_names.append(bucket_name)

        assert "parsect-models" in bucket_names

    def test_upload_file_doesnot_raise_error(self, setup_s3_util):
        aws_util = setup_s3_util
        dummy_path = pathlib.Path(TESTS_DIR, "utils", "dummy_file.txt")
        with open(dummy_path, "w") as fp:
            fp.write("dummy line \n")

        aws_util.upload_file(str(dummy_path), dummy_path.name)

    def test_upload_with_directory(self, setup_s3_util):
        aws_util = setup_s3_util
        dummy_file_path = pathlib.Path(TESTS_DIR, "utils", "dummy_file.txt")
        with open(dummy_file_path, "w") as fp:
            fp.write("dummy line \n")

        aws_util.upload_file(str(dummy_file_path), f"dummy_folder/dummy_file.txt")

    def test_upload_folder(self, setup_s3_util):
        aws_util = setup_s3_util
        dummy_folder = str(pathlib.Path(TESTS_DIR, "utils", "dummy_folder"))

        aws_util.upload_folder(dummy_folder, base_folder_name=dummy_folder)

    def test_download_file(self, setup_s3_util):
        util = setup_s3_util
        try:
            util.download_file("dummy_file.txt", "dummy_file.txt")
        except:
            pytest.fail(f"Failed to download file dummy_file.txt")

    def test_download_folder(self, setup_s3_util):
        util = setup_s3_util
        try:
            util.download_folder("dummy_folder")
        except:
            pytest.fail(f"Could not downlaod dummy_folder from s3")

    def test_download_debug_random(self, setup_s3_util):
        """Test whether a dummy model folder can be downloaded"""
        util = setup_s3_util
        try:
            util.download_folder("debug_bow_random")
        except:
            pytest.fail(f"Could not download debug_bow_random folder from s3")
