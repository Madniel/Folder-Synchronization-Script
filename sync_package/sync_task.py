import argparse
import hashlib
import os
import shutil
import time
from datetime import datetime

from utils.decorator import exception_handler


@exception_handler
def md5(fname: str) -> str:
    """
    Calculate MD5 hash of a file.

    Args:
    - fname: Path to the file for which MD5 hash needs to be calculated.

    Returns:
    - str: MD5 hash of the file content.
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


@exception_handler
def sync_folders(source: str, replica: str, log_file: str) -> None:
    """
    Synchronize the contents of the source folder to the replica folder.

    Args:
    - source: Path to the source directory.
    - replica: Path to the replica directory.
    - log_file: Path to the log file.

    This function ensures that after its execution, the contents of the
    replica folder match exactly with the source folder. Any extra files
    or directories in the replica that don't exist in source are removed.
    """

    # 1. Ensure that the source folder exists
    if not os.path.exists(source):
        log(f"Source directory '{source}' does not exist!", log_file)
        return

    # 2. If the replica doesn't exist, create it
    if not os.path.exists(replica):
        os.makedirs(replica)

    # 3. Create a list of files and directories in both source and replica
    source_files_set = set(os.listdir(source))
    replica_files_set = set(os.listdir(replica))

    # 4. Remove files/directories in replica not present in source
    for item in replica_files_set - source_files_set:
        item_path = os.path.join(replica, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
        log(f"Removed '{item_path}'", log_file)

    # 5. Copy files from source to replica
    for item in source_files_set:
        source_item_path = os.path.join(source, item)
        replica_item_path = os.path.join(replica, item)

        if os.path.isdir(source_item_path):
            # If the item is a directory, recursively sync it
            if not os.path.exists(replica_item_path):
                os.makedirs(replica_item_path)
            sync_folders(source_item_path, replica_item_path, log_file)
        else:
            # Only copy if the file is new or has changed
            if item not in replica_files_set or md5(source_item_path, log_file) != md5(replica_item_path, log_file):
                shutil.copy2(source_item_path, replica_item_path)
                log(f"Copied '{source_item_path}' to '{replica_item_path}'", log_file)


@exception_handler
def log(message: str, log_file: str) -> None:
    """
    Log messages to the console and to a log file.

    Args:
    - message: The message to be logged.
    - log_file: Path to the log file where the message should be written.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"[{timestamp}] {message}"
    print(formatted_message)
    with open(log_file, "a") as f:
        f.write(formatted_message + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("interval", type=int, help="Synchronization interval (in seconds)")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    while True:
        sync_folders(args.source, args.replica, args.log_file)
        time.sleep(args.interval)
