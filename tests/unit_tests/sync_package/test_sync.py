import os

from sync_package.sync_task import log, sync_folders, md5


def test_md5(setup_temp_dirs_with_files, setup_temp_log_file):
    source, _ = setup_temp_dirs_with_files
    file_path = os.path.join(source, "file1.txt")

    # MD5 hash for "content1" is '1ce10b4343b9f5b048a3e7d2fc210fa1'
    assert md5(file_path, setup_temp_log_file) == '1ce10b4343b9f5b048a3e7d2fc210fa1'


def test_log(setup_temp_log_file):
    log_file_path = setup_temp_log_file
    log("Test message", log_file_path)

    with open(log_file_path, "r") as f:
        lines = f.readlines()
        assert "Test message" in lines[-1]


def test_sync_folders(setup_temp_dirs_with_files, setup_temp_log_file):
    source, replica = setup_temp_dirs_with_files
    sync_folders(str(source), str(replica), setup_temp_log_file)

    # Check if the replica has the files from source
    assert set(os.listdir(replica)) == {"file1.txt", "file2.txt"}

    with open(os.path.join(replica, "file1.txt"), "r") as f:
        assert f.read() == "content1"
    with open(os.path.join(replica, "file2.txt"), "r") as f:
        assert f.read() == "content2"
