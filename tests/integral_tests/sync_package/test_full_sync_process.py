import os

from sync_package.sync_task import sync_folders


def test_full_sync_process(setup_temp_dirs_with_files, setup_temp_log_file):
    source, replica = setup_temp_dirs_with_files

    # Initial Sync
    sync_folders(str(source), str(replica), setup_temp_log_file)
    assert set(os.listdir(replica)) == {"file1.txt", "file2.txt"}

    # Update source and Sync again
    source.join("file3.txt").write("content3")
    os.remove(os.path.join(source, "file1.txt"))
    sync_folders(str(source), str(replica), setup_temp_log_file)

    assert set(os.listdir(replica)) == {"file2.txt", "file3.txt"}
