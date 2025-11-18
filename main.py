import requests
from requests.auth import HTTPBasicAuth
import os
import lxml
import time
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

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


def get_pid(PID: str, username: str, password: str) -> bool:
    headers = {"Content-Type": "application/json"}
    handle_url = f"https://pid.gwdg.de/handles/{HANDLE_PREFIX}/{PID}"

    r = requests.get(
        url=handle_url,
        headers=headers,
        auth=HTTPBasicAuth(username=username, password=password),
    )

    if r.status_code == 404:
        return False
    if r.status_code == 200:
        try:
            return r.json()
        except:
            return {}
    print(f"Unexpected status code: {r.status_code} for GET request to url: {r.url}")
    return False

def pid_list(username: str, password: str) -> bool:
    headers = {"Content-Type": "application/json"}
    handle_url = f"https://pid.gwdg.de/handles/{HANDLE_PREFIX}"

    r = requests.get(
        url=handle_url,
        headers=headers,
        auth=HTTPBasicAuth(username=username, password=password),
    )

    if r.status_code == 404:
        return False
    if r.status_code == 200:
        pids = [pid for pid in r.content.decode("utf-8").split("\r\n") if pid.strip() != ""]
        for pid in pids:
            content = get_pid(pid, username, password)
            if content:
                yield [pid, content[0]["type"], content[0]["parsed_data"]]
            else:
                yield [pid, None, None]

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
        "--override",
        help="Override an existing PID if it exists.",
        action="store_true",
    )

    args = parser.parse_args()

    for env_variable in ("username", "password"):
        if not os.environ[env_variable]:
            print(f"environment variable '{env_variable}' is missing in .env file!")
            exit(1)

    if args.command:
        if args.command == "list":
            pids = pid_list(os.environ["username"], os.environ["password"])
            for pid in pids:
                print(pid)
            exit(1)
        elif args.command == "create":
            # first: check if PID exists
            pid = get_pid(args.PID, os.environ["username"], os.environ["password"])

            # if it exists, override only if override param is set, otherwise exit
            if pid != False:
                if args.override == True:
                    print(f"{args.PID} already exists, overriding as ordered.")
                    pass
                else:
                    print(f"{args.PID} already exists, not overriding. Exiting.")
                    exit(1)

            create_pid(args.PID, args.url, os.environ["username"], os.environ["password"])
    else:
        parser.print_help()