import argparse
import time

from sync_folders.sync_folders import sync_folders

if __name__ == "__main__":
    """
    run_script: A script for folder synchronization.

    This script continually synchronizes the contents of a source folder to a replica folder.
    Users can specify the source and replica directories, synchronization interval, and the path to a log file.

    Usage:
        run_script.py <source_folder_path> <replica_folder_path> <synchronization_interval_in_seconds> <log_file_path>

    Example:
        run_script.py /path/to/source/folder /path/to/replica/folder 10 /path/to/logfile.log

    This example will sync the source folder to the replica folder every 10 seconds and log the synchronization 
    activities to the specified log file.
    """
    parser = argparse.ArgumentParser(description="Run the folder synchronization.")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("interval",
                        type=int,
                        help="Synchronization interval (in seconds)")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    while True:
        sync_folders(args.source, args.replica, args.log_file)
        time.sleep(args.interval)
