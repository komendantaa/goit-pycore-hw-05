import sys
import re
from collections import Counter, defaultdict
from typing import List, Dict
from pathlib import Path


def parse_log_line(line: str) -> Dict[str, str]:
    match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)", line)
    if match:
        date, level, msg = match.groups()
        return {"date": date, "level": level, "msg": msg}
    return {}


def load_logs(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, "r", encoding="UTF-8") as file:
        return [parse_log_line(line) for line in file.readlines()]


def filter_logs_by_level(
    logs: List[Dict[str, str]], level: str
) -> List[Dict[str, str]]:
    return [log for log in logs if log["level"] == level.upper()]  # better performance
    # return list(filter(lambda d: d["level"] == level.upper(), logs)) # for huge files (generator)


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    counts = defaultdict(int)
    for log in logs:
        counts[log.get("level")] += 1
    return counts
    # levels = (log.get("level") for log in logs)
    # return Counter(levels)


def display_log_counts(counts: dict) -> None:
    header = "Рівень логування | Кількість"
    print(header)
    print("-" * len(header))

    if not counts:
        return print("Немає данних")

    for level, count in counts.items():
        print(f"{level or '':<16} | {count}")


def main():
    # Validation
    path_to_file = sys.argv[1] if len(sys.argv) > 1 else None
    if not path_to_file:
        print("Path to file required")
        exit(1)

    if not path_to_file.endswith(".log"):
        print(f"File '{path_to_file}' is not log file, '*.log' required.")
        exit(1)

    path_to_file = Path(path_to_file)
    if not path_to_file.is_file():
        print(f"File not found at path '{path_to_file}'")
        exit(1)

    # Parsing
    logs = load_logs(path_to_file)
    if not logs:
        print("No logs found in the file.")
        exit(1)

    # Counting
    counts = count_logs_by_level(logs)

    # Printing log counts
    display_log_counts(counts)

    # Printing logs by level
    level = sys.argv[2].upper() if len(sys.argv) > 2 else None
    if level:
        filtered = filter_logs_by_level(logs, level)
        print(f"\nДеталі логів для рівня '{level}':")
        if filtered:
            for log in filtered:
                print(log.get("date"), " - ", log.get("msg"))
        else:
            print("Немає данних")


if __name__ == "__main__":
    main()
