# Folder Synchronization Script

This script offers a robust solution to ensure that a replica directory is an exact reflection of a source directory. It
meticulously scans the two directories, comparing their contents to identify any discrepancies. Once recognized, the
script swiftly acts to copy, update, or delete files as required, ensuring data integrity and synchronization.

## Features & Highlights

- **Efficiency First**: Uses a fast hashing mechanism to detect changes, ensuring rapid synchronization even for large
  files and directories.
- **Comprehensive Logging**: Every action the script takes – from copying and updating files to addressing errors – is
  logged with a timestamp. This ensures traceability and aids in debugging.
- **Edge Case Management**: The script is crafted to handle system-reserved file and folder names, making it versatile
  across different operating systems.
- **Deep Directory Scanning**: Nested directories are no challenge. The script dives deep into hierarchical folders
  ensuring every file, no matter how nested, is synchronized.

## How to Run the Script

1. **Running the Script**:
    - Navigate to the directory where the script is located using the command line or terminal.
    - Run the script using the following command:
      ```bash
      python sync_folders.py [source_directory] [replica_directory] [log_file_path]
      ```

   Replace `[source_directory]`, `[replica_directory]`, and `[log_file_path]` with your actual paths.

3. **Reviewing Logs**:
    - Once the script has run, you can review the `[log_file_path]` to see a detailed account of the synchronization
      process.

## Testing

The script comes with both unit and integral tests to ensure its reliability and accuracy.

# Unit Tests

The module contains several unit tests to ensure the correctness of individual components. Below are the unit tests for the functions:

## Tests Overview:

- **test_fast_hash_basic:** This test ensures that the `fast_hash` function generates the correct hash for a basic file.
- **test_fast_hash_large_file:** This test confirms that the `fast_hash` function correctly hashes a large file.
- **test_fast_hash_content_change:** Validates that the hash value changes when the content of a file changes.
- **test_log_single_entry & test_log_multiple_entries:** These tests ensure that the logging mechanism correctly captures single and multiple log entries.
- **test_remove_entry:** Checks that an individual file can be removed correctly.
- **test_remove_extra_entries:** Verifies that extra files not present in the source but present in the replica can be removed.
- **test_is_files_are_identical:** Checks if two files with identical content are recognized as such.
- **test_copy_from_source_to_replica:** Validates that files from the source are correctly copied to the replica.
- **test_is_source_exists:** Ensures that the function correctly identifies if a source exists or not.
- **test_check_replica_exists:** Confirms that the function can determine if a replica exists and re-creates it if not.
- **test_get_directory_entries:** Checks if the function can correctly list the entries within a directory.

To run the unit tests:

```bash
python -m unittest path_to_unit_tests_file.py
```

## Integral Test

The `test_full_sync_process` function provides an integral test that checks the full synchronization process to ensure
that both the source and replica directories are accurately mirrored.

### Test Steps:

1. **Initial Sync**:
    - Syncs using predefined source files ("file1.txt" and "file2.txt").
    - Verifies that both directories have the same set of files.

2. **File Addition and Removal**:
    - Adds a new file, "file3.txt", to the source and deletes "file1.txt".
    - Syncs and verifies the changes in the replica.

3. **Content Update**:
    - Modifies the content of "file2.txt" in the source.
    - Syncs and checks the updated content in the replica.

4. **Subdirectory Handling**:
    - Creates a subdirectory in the source with "subfile.txt".
    - Syncs and ensures the replica also has this subdirectory and file.

5. **Removing Subdirectories**:
    - Removes the entire subdirectory created in the previous step from the source.
    - Syncs and ensures its removal in the replica.

6. **Deep Nested Directories**:
    - Creates nested directories within the source with "deep_file.txt" in the innermost level.
    - Syncs and ensures the replica replicates the same nested structure and file.

7. **Log Verification**:
    - Checks the log for synchronization actions such as copying, removal, and updating of files.


