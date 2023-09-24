import os
import shutil
from datetime import datetime

import xxhash

from utils.decorator import exception_handler


@exception_handler
def fast_hash(filename: str) -> str:
    """
    Calculate a fast hash of a file using xxHash.

    Args:
    - filename: Path to the file for which the hash needs to be calculated.

    Returns:
    - str: Hash of the file content.
    """
    hasher = xxhash.xxh64()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


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

    if not os.path.exists(source):
        log(f"Source directory '{source}' does not exist!", log_file)
        return

    os.makedirs(replica, exist_ok=True)

    source_entries = {entry.name: entry for entry in os.scandir(source)}
    replica_entries = {entry.name: entry for entry in os.scandir(replica)}

    # Remove files/directories in replica not present in source
    for item_name in set(replica_entries.keys()) - set(source_entries.keys()):
        item_path = os.path.join(replica, item_name)
        if replica_entries[item_name].is_dir():
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
        log(f"Removed '{item_path}'", log_file)

    # Copy files from source to replica
    for item_name, source_entry in source_entries.items():
        replica_path = os.path.join(replica, item_name)

        if source_entry.is_dir():
            os.makedirs(replica_path, exist_ok=True)
            sync_folders(source_entry.path, replica_path, log_file)
        else:
            should_copy = False
            if item_name not in replica_entries:
                should_copy = True
            else:
                # Check file size or modified timestamp before computing hash for efficiency
                if os.path.getsize(source_entry.path) != os.path.getsize(replica_path) or os.path.getmtime(
                        source_entry.path) != os.path.getmtime(replica_path):
                    should_copy = True
                elif fast_hash(source_entry.path) != fast_hash(replica_path):
                    should_copy = True

            if should_copy:
                shutil.copy2(source_entry.path, replica_path)
                if item_name not in replica_entries:
                    log(f"Copied '{source_entry.path}' to '{replica_path}'", log_file)
                else:
                    log(f"Updated '{replica_path}' from '{source_entry.path}'", log_file)


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
