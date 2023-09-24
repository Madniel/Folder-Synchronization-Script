import argparse
import time

from sync_folders.sync_folders import sync_folders

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the folder synchronization.")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("interval", type=int, help="Synchronization interval (in seconds)")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    while True:
        sync_folders(args.source, args.replica, args.log_file)
        time.sleep(args.interval)
