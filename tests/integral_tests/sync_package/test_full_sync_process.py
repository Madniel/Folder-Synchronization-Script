import os
import shutil

from sync_folders.sync_folders import sync_folders

def test_full_sync_process(temporary_directories_with_files, exemplary_log_file):
    source, replica = temporary_directories_with_files
    exemplary_files = {"file1.txt", "file2.txt"}

    sync_folders(str(source), str(replica), exemplary_log_file)
    files_in_directory = set(os.listdir(replica))
    assert files_in_directory == exemplary_files

    source.join("file3.txt").write("content3")
    exemplary_files = {"file2.txt", "file3.txt"}
    os.remove(os.path.join(source, "file1.txt"))
    sync_folders(str(source), str(replica), exemplary_log_file)
    files_in_directory = set(os.listdir(replica))
    assert files_in_directory == exemplary_files

    source.join("file2.txt").write("updated_content")
    sync_folders(str(source), str(replica), exemplary_log_file)
    with open(replica.join("file2.txt"), 'r') as file:
        assert file.read() == "updated_content"

    sub_dir = source.mkdir("subdir")
    sub_dir.join("subfile.txt").write("Sub directory content")
    sync_folders(str(source), str(replica), exemplary_log_file)
    assert "subfile.txt" in os.listdir(replica.join("subdir"))

    shutil.rmtree(os.path.join(source, "subdir"))
    sync_folders(str(source), str(replica), exemplary_log_file)
    assert "subdir" not in os.listdir(replica)

    nested_dir = source.mkdir("nested_dir1").mkdir("nested_dir2").mkdir("nested_dir3")
    nested_dir.join("deep_file.txt").write("Deep Nested Content")
    sync_folders(str(source), str(replica), exemplary_log_file)
    deep_path = os.path.join(replica, "nested_dir1", "nested_dir2", "nested_dir3", "deep_file.txt")
    assert os.path.exists(deep_path)

    with open(exemplary_log_file, "r") as f:
        logs = f.read()
        assert "Copied" in logs
        assert "Removed" in logs
        assert "Updated" in logs

