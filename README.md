# 📁 Folder Synchronization Script

Ensure your replica directory perfectly mirrors the source directory with this robust script. Dive deep into directories, manage edge cases, and keep a meticulous log of every action.

## 🌟 Features & Highlights

- 🚀 **Efficiency First**: Leverage the power of fast hashing for rapid synchronization, suitable for extensive datasets.
- 📝 **Comprehensive Logging**: Trace every step with timestamped logs. Debugging has never been easier.
- 💡 **Edge Case Management**: Versatility across OSs by addressing system-reserved names.
- 📂 **Deep Directory Scanning**: Navigate complex hierarchical structures with ease.

## 🚀 Getting Started

### 1. Running the Script

Navigate to the script's directory and execute:

```bash
python run_sync_folders.py [source_directory] [replica_directory] [synchronization_interval_in_seconds] [log_file_path]
```

> Replace `[source_directory]`, `[replica_directory]`, and `[log_file_path]` with your paths.
> Replace '[synchronization_interval_in_seconds]' with time.

### 2. Dive into Logs

After synchronization, inspect the `[log_file_path]` for a granular breakdown of the process.

## 🛠️ Testing

Quality is our top priority. Dive into the reliability checks with unit and integral tests.

### Unit Tests

For the enthusiasts, here's a rundown of the test scenarios:

#### 📋 Tests Overview:

- **Basic Hashing** (`test_fast_hash_basic`): Validates the hash generated for a standard file.
- **Handling Large Files** (`test_fast_hash_large_file`): Tests the hashing capability for vast files.
- **Content Alteration** (`test_fast_hash_content_change`): Ensures the hash reflects content modifications.
- **Logging Single Entries** (`test_log_single_entry`): Verifies correct logging of individual entries.
- **Logging Multiple Entries** (`test_log_multiple_entries`): Checks the logging of consecutive messages.
- **Entry Removal** (`test_remove_entry`): Asserts the ability to remove specific files.
- **Cleaning Extras** (`test_remove_extra_entries`): Validates removal of extra files not present in the source.
- **Content Identity Check** (`test_is_files_are_identical`): Confirms the recognition of two identical files.
- **Replication Process** (`test_copy_from_source_to_replica`): Ensures precise copying from source to replica.
- **Source Existence** (`test_is_source_exists`): Tests the accurate identification of a source's presence.
- **Replica Existence & Creation** (`test_check_replica_exists`): Validates the detection of a replica's existence and its re-creation if missing.
- **Directory Listing** (`test_get_directory_entries`): Asserts the correct listing of directory entries.

Run the tests with:

```bash
python -m unittest path_to_unit_tests_file.py
```

### Integral Test

For a holistic check, the `test_full_sync_process` tests the end-to-end synchronization.

#### 🔍 Test Steps:

1. **Initial Sync**: Matches the predefined source files, ensuring both the source and replica directories possess the exact set of files.
2. **File Dynamics**: Validates additions ("file3.txt") and deletions ("file1.txt") in the source to ensure they accurately reflect in the replica.
3. **Content Evolution**: Syncs any content modifications from the source, like changes in "file2.txt", ensuring the replica reflects these updates.
4. **Subdirectory Handling**: Verifies the script's ability to handle new subdirectories and synchronize contained files like "subfile.txt".
5. **Removing Subdirectories**: Ensures that deleted subdirectories in the source, and their contents, are also removed from the replica.
6. **Deep Nested Directories**: Evaluates the script's efficiency with intricate nested directory structures, ensuring "deep_file.txt" in the source's innermost directory is mirrored in the replica.
7. **Log Verification**: Validates accurate logging of all synchronization actions, from copying and deleting to content updates.
