import requests
from requests.auth import HTTPBasicAuth
import os
import lxml
import time
import json
import argparse
from dotenv import load_dotenv


PID_HANDLE = "21.11146"


def create_pid(sbr_num: int, username: str, password: str) -> None:
    print(f"Creating PID for sbr-{sbr_num}")

    sbr_id = f"sbr-{sbr_num}"
    landingpage_url = (
        f"https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-{sbr_id}/"
    )

    headers = {"Content-Type": "application/json"}

    url = f"https://pid.gwdg.de/handles/{PID_HANDLE}/{sbr_num}"
    data = json.dumps([{"type": "URL", "parsed_data": landingpage_url}])
    r = requests.put(
        url=url,
        data=data,
        headers=headers,
        auth=HTTPBasicAuth(username, password),
    )
    r.raise_for_status()
    print(f"PUT request url: {r.url}")
    print(f"PUT request status code: {r.status_code}")


def pid_exists(sbr_num: int, username: str, password: str) -> bool:
    headers = {"Content-Type": "application/json"}
    url = f"https://pid.gwdg.de/handles/{PID_HANDLE}/{sbr_num}"

    r = requests.get(
        url=url,
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
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Create a PID for a Språkbanken resource"
    )
    parser.add_argument(
        "sbr_num",
        type=int,
        help="Resource number (number after sbr- in the resource catalogue url)",
    )
    parser.add_argument(
        "-c",
        "--check_previous",
        action="store_true",
        help="If flagged, check if PID exist for all previous sbr-numbers (from 1 to sbr_num)",
    )
    parser.add_argument(
        "-a",
        "--add_previous",
        action="store_true",
        help="If flagged, will create PIDs when they are missing for all previous sbr-numbers (from 1 to sbr_num)",
    )
    args = parser.parse_args()

    for env_variable in ("username", "password"):
        if not os.environ[env_variable]:
            print(f"environment variable '{env_variable}' is missing in .env file!")
            exit(1)

    if args.check_previous:
        print(f"Checking if PID exist for all sbr numbers upto {args.sbr_num}")
        pid_missing_list = [
            i
            for i in range(1, args.sbr_num)
            if not pid_exists(i, os.environ["username"], os.environ["password"])
        ]
        if pid_missing_list:
            print(
                f"PID missing for the following sbr numbers: {'\n'.join(str(i) for i in pid_missing_list)}"
            )
            if args.add_previous:
                for i in pid_missing_list:
                    create_pid(
                        sbr_num=i,
                        username=os.environ["username"],
                        password=os.environ["password"],
                    )

        else:
            print("No PIDs missing")

    create_pid(args.sbr_num, os.environ["username"], os.environ["password"])
    print(f"PID link for COMEDI metadata:\nhdl:{PID_HANDLE}/{args.sbr_num}")
