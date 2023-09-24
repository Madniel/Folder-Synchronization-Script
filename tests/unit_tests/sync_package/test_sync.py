import os
import shutil
import tempfile
import time

from sync_folders.sync_folders import log, fast_hash, get_directory_entries, check_replica_exists, is_source_exists, \
    copy_from_source_to_replica, is_files_are_identical, remove_extra_entries, remove_entry


def test_fast_hash_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "exemplary_file.txt")

        with open(file_path, 'w') as file:
            file.write("content")

        expected_xxhash = '6c5b191a31c5a9fc'
        assert fast_hash(file_path) == expected_xxhash


def test_fast_hash_large_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        large_file_path = os.path.join(tmpdir, "large_file.txt")
        with open(large_file_path, 'w') as file:
            for _ in range(10000):
                file.write("Exemplary line.\n")

        first_hash_ground_truth = '242b2a4200cb42ff'
        first_hash = fast_hash(large_file_path)
        assert first_hash == first_hash_ground_truth


def test_fast_hash_content_change():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test_file.txt")
        with open(file_path, 'w') as file:
            file.write("Original content.")

        original_hash = fast_hash(file_path)

        with open(file_path, 'w') as file:
            file.write("Modified content.")

        modified_hash = fast_hash(file_path)
        assert original_hash != modified_hash


def test_log_single_entry(exemplary_log_file):
    log("Test message", exemplary_log_file)

    with open(exemplary_log_file, "r") as file:
        lines = file.readlines()
        assert "Test message" in lines[-1]


def test_log_multiple_entries(exemplary_log_file):
    log("First message", exemplary_log_file)
    time.sleep(1)
    log("Second message", exemplary_log_file)

    with open(exemplary_log_file, "r") as file:
        lines = file.readlines()
        assert "First message" in lines[-2]
        assert "Second message" in lines[-1]


def test_remove_entry(temporary_directories_with_files, exemplary_log_file):
    source, replica = temporary_directories_with_files

    # Create a file in replica that's not in source, then remove it
    test_file = replica.join("test_remove.txt")
    test_file.write("content")

    file_entry = next(os.scandir(str(replica)))
    remove_entry(file_entry, str(test_file), exemplary_log_file)

    assert not test_file.exists()
    with open(exemplary_log_file, 'r') as log:
        assert f"Removed '{test_file}'" in log.read()


def test_remove_extra_entries(temporary_directories_with_files, exemplary_log_file):
    source, replica = temporary_directories_with_files

    test_file = replica.join("extra_file.txt")
    test_file.write("extra_content")

    source_files = get_directory_entries(str(source))
    replica_files = get_directory_entries(str(replica))

    remove_extra_entries(source_files, replica_files, str(replica), exemplary_log_file)

    assert not test_file.exists()


def test_is_files_are_identical(temporary_directories_with_files):
    source, replica = temporary_directories_with_files
    file1_path = source.join("file1.txt")
    replica_file1_path = replica.join("file1.txt")

    shutil.copy2(file1_path, replica_file1_path)

    assert is_files_are_identical(str(file1_path), str(replica_file1_path))


def test_copy_from_source_to_replica(temporary_directories_with_files, exemplary_log_file):
    source, replica = temporary_directories_with_files
    source_files = get_directory_entries(str(source))

    copy_from_source_to_replica(source_files, str(replica), exemplary_log_file)

    assert replica.join("file1.txt").exists()
    assert replica.join("file2.txt").exists()


def test_is_source_exists(temporary_directories_with_files, exemplary_log_file):
    source, _ = temporary_directories_with_files

    assert is_source_exists(str(source), exemplary_log_file)
    assert not is_source_exists("/nonexistent_path", exemplary_log_file)


def test_check_replica_exists(temporary_directories_with_files):
    _, replica = temporary_directories_with_files

    # Remove the replica and then check it
    shutil.rmtree(replica)
    assert not os.path.exists(replica)

    check_replica_exists(str(replica))
    assert os.path.exists(replica)


def test_get_directory_entries(temporary_directories_with_files):
    source, _ = temporary_directories_with_files
    number_entries_ground_truth = 2

    entries = get_directory_entries(str(source))
    assert len(entries) == number_entries_ground_truth
    assert "file1.txt" in entries
    assert "file2.txt" in entries
