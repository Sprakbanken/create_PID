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


def pid_exists(PID: str, username: str, password: str) -> bool:
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
        return True
    print(f"Unexpected status code: {r.status_code} for GET request to url: {r.url}")
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a PID for a given resource"
    )
    parser.add_argument(
        "PID",
        type=str,
        help="The actual PID to create.",
    )

    parser.add_argument(
        "--url",
        type=str,
        help="The URL that the PID is associated with.",
    )

    parser.add_argument(
        "--override",
        help="Override an existing PID if it exists.",
        action="store_true",
    )

    args = parser.parse_args()

    for env_variable in ("username", "password"):
        if not os.environ[env_variable]:
            print(f"environment variable '{env_variable}' is missing in .env file!")
            exit(1)

    # first: check if PID exists
    exists = pid_exists(args.PID, os.environ["username"], os.environ["password"])

    # if it exists, override only if override param is set, otherwise exit
    if exists == True:
        if args.override == True:
            print(f"{args.PID} already exists, overriding as ordered.")
            pass
        else:
            print(f"{args.PID} already exists, not overriding. Exiting.")
            exit(1)

    create_pid(args.PID, args.url, os.environ["username"], os.environ["password"])
