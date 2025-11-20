import requests
from requests.auth import HTTPBasicAuth
import os
import time
import json
import argparse
from dotenv import load_dotenv

load_dotenv(override=True)

HANDLE_PREFIX = os.environ["HANDLE_PREFIX"]

def create_pid(PID: str, url: str, username: str, password: str) -> None:
    print(f"Creating PID for {PID}")

    headers = {"Content-Type": "application/json"}

    handle_url = f"https://pid.gwdg.de/handles/{HANDLE_PREFIX}/{PID}"
    data = json.dumps([{"type": "URL", "parsed_data": url}])
    r = requests.put(
        url=handle_url,
        data=data,
        headers=headers,
        auth=HTTPBasicAuth(username, password),
    )
    r.raise_for_status()
    print(f"PUT request url: {r.url}")
    print(f"PUT request status code: {r.status_code}")


def get_pid(PID: str, username: str, password: str) -> dict | None:
    headers = {"Content-Type": "application/json"}
    handle_url = f"https://pid.gwdg.de/handles/{HANDLE_PREFIX}/{PID}"

    r = requests.get(
        url=handle_url,
        headers=headers,
        auth=HTTPBasicAuth(username=username, password=password),
    )

    if r.status_code == 404:
        return None
    if r.status_code == 200:
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:
            print(f"JSONDecodeError when trying to parse content from request: {r}")
            return None
    print(f"Unexpected status code: {r.status_code} for GET request to url: {r.url}")
    return None

def pid_list(username: str, password: str) -> None:
    headers = {"Content-Type": "application/json"}
    handle_url = f"https://pid.gwdg.de/handles/{HANDLE_PREFIX}"

    r = requests.get(
        url=handle_url,
        headers=headers,
        auth=HTTPBasicAuth(username=username, password=password),
    )

    if r.status_code == 404:
        print("Prefix not found.")
    elif r.status_code == 200:
        pids = [pid for pid in r.content.decode("utf-8").split("\r\n") if pid.strip() != ""]
        for pid in pids:
            content = get_pid(pid, username, password)
            if content:
                print(pid, content[0]["type"], content[0]["parsed_data"])
            else:
                print(pid, None, None)
    else:
        print(f"Unexpected status code: {r.status_code} for GET request to url: {r.url}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Manage PIDs for language resources"
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    parser_create = subparsers.add_parser("create", help="Create and modify PIDs.")
    parser_list = subparsers.add_parser("list", help="List all PIDs.")

    parser_create.add_argument(
        "PID",
        type=str,
        help="The actual PID to create.",
    )

    parser_create.add_argument(
        "--url",
        type=str,
        help="The URL that the PID is associated with.",
    )

    parser_create.add_argument(
        "--update",
        help="Update an existing PID if it exists.",
        action="store_true",
    )

    args = parser.parse_args()

    for env_variable in ("username", "password"):
        if not env_variable in os.environ:
            print(f"environment variable '{env_variable}' is missing in .env file!")
            exit(1)

    match args.command:
        case "list":
            pid_list(os.environ["username"], os.environ["password"])
        case "create":
            # first: check if PID exists
            pid = get_pid(args.PID, os.environ["username"], os.environ["password"])

            # if it exists, update only if update param is explicitly set, otherwise exit
            if pid != None:
                if args.update:
                    print(f"{args.PID} already exists, updating as requested.")
                    pass
                else:
                    print(f"{args.PID} already exists, leaving it untouched. Exiting.")
                    exit(1)

            create_pid(args.PID, args.url, os.environ["username"], os.environ["password"])
        case _:
            parser.print_help()
