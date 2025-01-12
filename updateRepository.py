import json
import requests
import datetime


def get_latest_releases():
    url = "https://api.github.com/repos/CDFER/JLCPCB-Kicad-Library/releases"
    response = requests.get(url)
    return response.json()


def update_packages_json(packages_json_file: str, new_releases) -> None:
    with open(packages_json_file, "r") as f:
        packages = json.load(f)

    packages["packages"][0]["versions"] = []

    for release in new_releases:
        version = release.get("tag_name", "")
        asset = next(
            (
                asset
                for asset in release.get("assets", [])
                if asset.get("name", "").startswith("JLCPCB-KiCad-Library-") and asset.get("name", "").endswith(".zip")
            ),
            None,
        )
        if asset:
            download_url = asset.get("browser_download_url", "")
            packages["packages"][0]["versions"].append(
                {"version": version, "status": "stable", "kicad_version": "8.0", "download_url": download_url}
            )

    with open(packages_json_file, "w") as f:
        json.dump(packages, f, indent=4)


def update_repository_json(repository_json_file: str) -> None:
    with open(repository_json_file, "r") as f:
        repository = json.load(f)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    repository["packages"]["update_time_utc"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
    repository["packages"]["update_timestamp"] = int(current_time.timestamp())
    with open(repository_json_file, "w") as f:
        json.dump(repository, f, indent=4)


def main() -> None:
    releases = get_latest_releases()
    update_packages_json("packages.json", releases)
    update_repository_json("repository.json")


if __name__ == "__main__":
    main()
