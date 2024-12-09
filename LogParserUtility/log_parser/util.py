#!/usr/bin/env python3

import re
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Log Parsing Utility")
    parser.add_argument("-f", "--first", type=int, help="Print first NUM lines")
    parser.add_argument("-l", "--last", type=int, help="Print last NUM lines")
    parser.add_argument("-t", "--timestamps", action="store_true", help="Print lines with timestamps")
    parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines with IPv4 addresses")
    parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines with IPv6 addresses")
    parser.add_argument("file", nargs="?", type=str, help="File to process", default=None)
    return parser.parse_args()


def read_lines(file):
    try:
        with open(file, "r") if file else sys.stdin as f:
            return f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def filter_first(lines, num):
    return lines[:num]


def filter_last(lines, num):
    return lines[-num:]


def filter_timestamps(lines):
    timestamp_pattern = re.compile(r"\b\d{2}:\d{2}:\d{2}\b")
    return [line for line in lines if timestamp_pattern.search(line)]


def filter_ipv4(lines):
    ipv4_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    return [highlight_matches(line, ipv4_pattern) for line in lines if ipv4_pattern.search(line)]


def filter_ipv6(lines):
    ipv6_pattern = re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b")
    return [highlight_matches(line, ipv6_pattern) for line in lines if ipv6_pattern.search(line)]


def highlight_matches(line, pattern):
    return pattern.sub(lambda match: f"\033[93m{match.group(0)}\033[0m", line)


def main():
    args = parse_args()
    lines = read_lines(args.file)

    if args.first:
        lines = filter_first(lines, args.first)
    if args.last:
        lines = filter_last(lines, args.last)
    if args.timestamps:
        lines = filter_timestamps(lines)
    if args.ipv4:
        lines = filter_ipv4(lines)
    if args.ipv6:
        lines = filter_ipv6(lines)

    for line in lines:
        print(line, end="")


if __name__ == "__main__":
    main()
