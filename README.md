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

### Unit Tests

Unit tests are focused on individual components of the script, ensuring that functions like `fast_hash` and `log`
operate correctly. Examples include:

- Verifying the hash of a basic file.
- Confirming the hash of a large file.
- Detecting content changes by hashing.
- Logging single and multiple entries correctly.

To run the unit tests:

```bash
python -m unittest path_to_unit_tests_file.py
```

### Integral Tests

Integral tests ensure that the various components of the program work harmoniously together. For the Folder Synchronization Program, an integral test might involve:

1. Creating temporary directories with sample files to simulate the `source` and `replica`.
2. Running the `sync_folders` function to synchronize these folders.
3. Checking if:
   - Newly created files in the source are copied to the replica.
   - Updated files in the source replace outdated ones in the replica.
   - Deleted files in the source are removed from the replica.
   - Nested directories and their files are accurately mirrored in the replica.
4. Logging of all operations is checked in the specified log file.


