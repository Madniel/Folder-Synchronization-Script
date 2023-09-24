import os
import tempfile
import time

from sync_folders.sync_folders import log, fast_hash


def test_fast_hash_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "exemplary_file.txt")

        with open(file_path, 'w') as f:
            f.write("content")

        expected_xxhash = '6c5b191a31c5a9fc'
        assert fast_hash(file_path) == expected_xxhash


def test_fast_hash_large_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        large_file_path = os.path.join(tmpdir, "large_file.txt")
        with open(large_file_path, 'w') as file:
            for _ in range(10000):  # writing 10000 lines
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
