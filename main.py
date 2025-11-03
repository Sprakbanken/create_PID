import requests
from requests.auth import HTTPBasicAuth
import os
import lxml
import time
import json
import argparse
from dotenv import load_dotenv


PID_HANDLE = "21.11146"


def create_pid_url(sbr_num: int, username: str, password: str) -> str:
    sbr_id = f"sbr-{sbr_num}"
    landingpage_url = (
        f"https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-{sbr_id}/"
    )

    headers = {"Content-Type": "application/json"}

    baseurl = f"https://pid.gwdg.de/handles/{PID_HANDLE}/"
    data = json.dumps([{"type": "URL", "parsed_data": landingpage_url}])
    r = requests.put(
        baseurl + sbr_id,
        data=data,
        headers=headers,
        auth=HTTPBasicAuth(username, password),
    )
    r.raise_for_status()
    print(f"PUT request url: {r.url}")
    print(f"PUT request status code: {r.status_code}")
    return r.url


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Create a PID URL for a Språkbanken resource"
    )
    parser.add_argument(
        "sbr_num",
        type=int,
        help="Resource number (number after sbr- in the resource catalogue url)",
    )
    args = parser.parse_args()

    for env_variable in ("username", "password"):
        if not os.environ[env_variable]:
            print(f"environment variable '{env_variable}' is missing in .env file!")
            exit(1)

    url = create_pid_url(args.sbr_num, os.environ["username"], os.environ["password"])

    print(f"PID link for COMEDI metadata:\nhdl:{PID_HANDLE}/sbr-{args.sbr_num}")
