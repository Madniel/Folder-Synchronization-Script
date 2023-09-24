import os
import shutil
from datetime import datetime
from typing import Dict

import xxhash

from utils.decorator import exception_handler
SYSTEM_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL", "COM1", "LPT1"}  # This is for Windows. Adjust accordingly.


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
    with open(filename, "rb") as file:
        [hasher.update(chunk) for chunk in iter(lambda: file.read(4096), b"")]

    return hasher.hexdigest()


def remove_entry(entry: os.DirEntry, file_path: str, log_file: str) -> None:
    """
    Remove a specific file or directory and log the removal action.le.

    Args:
    - entry (os.DirEntry): The os.DirEntry object representing the file or directory to be removed.
    - file_path (str): The path to the file or directory that needs to be removed.
    - log_file (str): Path to the log file where the removal action will be logged.

    Note:
    It is essential that the provided os.DirEntry object corresponds to the given file_path.
    """
    if entry.is_dir():
        shutil.rmtree(file_path)
    else:
        os.remove(file_path)
    log(f"Removed '{file_path}'", log_file)


def remove_extra_entries(source_files: Dict, replica_files: Dict, replica: str, log_file: str) -> None:
    """
    Remove files or directories in the replica that are not present in the source.

    Args:
    - source_files (Dict): Dictionary with item names as keys and os.DirEntry objects
                           as values representing the files and directories in the source.
    - replica_files (Dict): Dictionary with item names as keys and os.DirEntry objects
                            as values representing the files and directories in the replica.
    - replica (str): Path to the replica directory.
    - log_file (str): Path to the log file where actions will be logged.

    Note:
    The function makes use of the 'remove_entry' function to perform the removal operation.
    """
    additional_files = set(replica_files.keys()) - set(source_files.keys())
    for additional_file in additional_files:
        file_path = os.path.join(replica, additional_file)
        entry = replica_files[additional_file]
        remove_entry(entry, file_path, log_file)


def is_files_are_identical(source_path: str, replica_path: str) -> bool:
    """
    Check if two files are identical based on their size, modification time, and hash.

    Args:
    - source_path: Path to the source file.
    - replica_path: Path to the replica file.

    Returns:
    - bool: True if files are identical, otherwise False.
    """

    if os.path.getsize(source_path) != os.path.getsize(replica_path):
        return False
    if os.path.getmtime(source_path) != os.path.getmtime(replica_path):
        return False
    if fast_hash(source_path) != fast_hash(replica_path):
        return False

    return True


def copy_from_source_to_replica(source_files: Dict, replica: str, log_file: str) -> None:
    """
    Copy files/directories from source to replica. Only copy files that don't exist in the replica or have changed.

    Args:
    - source: Path to the source directory.
    - source_entries: Dictionary with item names as keys and os.DirEntry objects as values for the source directory.
    - replica: Path to the replica directory.
    - log_file: Path to the log file.
    """

    for file_name, source_entry in source_files.items():
        replica_path = os.path.join(replica, file_name)

        if source_entry.is_dir():
            os.makedirs(replica_path, exist_ok=True)
            sync_folders(source_entry.path, replica_path, log_file)
            continue

        action = "Updated"
        if file_name not in os.listdir(replica):
            action = "Copied"
        elif is_files_are_identical(source_entry.path, replica_path):
            continue

        shutil.copy2(source_entry.path, replica_path)
        log(f"{action} '{source_entry.path}' to '{replica_path}'", log_file)


def is_source_exists(source: str, log_file: str) -> bool:
    """
    Check if the source directory exists and log if it doesn't.

    Args:
    - source: Path to the source directory.
    - log_file: Path to the log file.

    Returns:
    - bool: True if the source directory exists, False otherwise.
    """
    if not os.path.exists(source):
        log(f"Source directory '{source}' does not exist!", log_file)
        return False
    return True


def check_replica_exists(replica: str) -> None:
    """
    Create the replica directory if it doesn't exist.

    Args:
    - replica: Path to the replica directory.
    """
    if not os.path.exists(replica):
        os.makedirs(replica)


def get_directory_entries(directory: str) -> Dict:
    """
    Retrieve the directory entries for the given directory.

    Args:
    - directory: Path to the directory.

    Returns:
    - Dict: Dictionary with directory entries.
    """
    return {entry.name: entry for entry in os.scandir(directory)}


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

    if not is_source_exists(source, log_file):
        return

    check_replica_exists(replica)

    source_entries = get_directory_entries(source)
    replica_entries = get_directory_entries(replica)

    remove_extra_entries(source_files=source_entries,
                         replica_files=replica_entries,
                         replica=replica,
                         log_file=log_file)

    copy_from_source_to_replica(source_files=source_entries,
                                replica=replica,
                                log_file=log_file)


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
    with open(log_file, "a") as file:
        file.write(formatted_message + "\n")
