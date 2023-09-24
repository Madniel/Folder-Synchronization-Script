import os
import shutil

from sync_folders.sync_folders import sync_folders

def test_full_sync_process(temporary_directories_with_files, exemplary_log_file):
    source, replica = temporary_directories_with_files

    # Step 1: Initial Sync
    sync_folders(str(source), str(replica), str(exemplary_log_file))
    assert set(os.listdir(replica)) == {"file1.txt", "file2.txt"}

    # Step 2: Modify source content - Add & Delete Files
    source.join("file3.txt").write("content3")
    os.remove(os.path.join(source, "file1.txt"))
    sync_folders(str(source), str(replica), str(exemplary_log_file))
    assert set(os.listdir(replica)) == {"file2.txt", "file3.txt"}

    # Step 3: Modify content of existing file in source
    source.join("file2.txt").write("updated_content2")
    sync_folders(str(source), str(replica), str(exemplary_log_file))
    with open(replica.join("file2.txt"), 'r') as f:
        assert f.read() == "updated_content2"

    # Step 4: Add subdirectories in the source
    sub_dir = source.mkdir("subdir")
    sub_dir.join("subfile.txt").write("Sub directory content")
    sync_folders(str(source), str(replica), str(exemplary_log_file))
    assert "subfile.txt" in os.listdir(replica.join("subdir"))

    # Step 5: Remove subdirectory from source
    shutil.rmtree(os.path.join(source, "subdir"))
    sync_folders(str(source), str(replica), str(exemplary_log_file))
    assert "subdir" not in os.listdir(replica)

    # Step 6: Testing nested directory structures
    nested_dir = source.mkdir("nested_dir1").mkdir("nested_dir2").mkdir("nested_dir3")
    nested_dir.join("deep_file.txt").write("Deep Nested Content")
    sync_folders(str(source), str(replica), str(exemplary_log_file))
    deep_path = os.path.join(replica, "nested_dir1", "nested_dir2", "nested_dir3", "deep_file.txt")
    assert os.path.exists(deep_path)

    # Step 7: Check the log messages
    with open(exemplary_log_file, "r") as f:
        logs = f.read()
        assert "Copied" in logs
        assert "Removed" in logs
        assert "Updated" in logs  # If your log function logs updates, include this check

