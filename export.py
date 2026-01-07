#!/usr/bin/env python3
"""
Script to export an asset from Meshcapade

The steps involved are:
1. Get an API token from env variable
2. Export the avatar in the requested format
3. Wait for the export to be ready
4. Download the exported file

Reference:
Meshcapade API documentation: https://meshcapade.com/api

Example usage:
python export.py 7fae7513-9860-4fa0-80a4-3dd1e75fb8d4
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional

import requests


# Meshcapade API base URL
API_BASE_URL = "https://api.meshcapade.com/api/v1"

# Asset state constants
ASSET_STATE_READY = "READY"
ASSET_STATE_ERROR = "ERROR"


def try_get_download_url(token: str, asset_id: str, export_payload: dict) -> Optional[str]:
    """
    Call export avatar endpoint to check on state and get download URL if ready.
    
    Args:
        token: API authentication token
        asset_id: ID of the avatar
        export_payload: The export payload to use
        
    Returns:
        Download URL if export is ready, None otherwise
    """
    url = f"{API_BASE_URL}/avatars/{asset_id}/export"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=export_payload)
    response.raise_for_status()
    response_json = response.json()

    # Extract state and download URL from JSON:API response format
    # Response format: { "data": { "attributes": { "state": "READY", "url": { "path": "https://...", ... }, ... }, ... } }
    data = response_json.get("data", {})
    attributes = data.get("attributes", {})
    
    if not attributes:
        raise ValueError(f"Export response came back empty: {response_json}")
    
    state = attributes.get("state")
    url_obj = attributes.get("url", {})
    download_url = url_obj.get("path") if url_obj else None
    
    if state == ASSET_STATE_READY:
        return download_url
    elif state == ASSET_STATE_ERROR:
        raise RuntimeError(f"Export finished with ERROR state: {response_json}")
    else:
        # Still processing
        return None


def export_avatar(token: str, asset_id: str) -> str:
    """
    Export avatar and wait for it to be ready.
    
    Args:
        token: API authentication token
        asset_id: ID of the avatar to export

    Returns:
        Download URL for the exported file
    """
    poll_interval = 5 # poll every 5 seconds
    max_wait = 600 # wait for up to 10 minutes

    export_payload = {
        "format": "GLB",
        "anim": "scan",
    }
    
    start_time = time.time()
    download_url = None
    
    while not download_url:
        download_url = try_get_download_url(token, asset_id, export_payload)
        
        if download_url:
            break
        
        # Check timeout
        elapsed = time.time() - start_time
        if elapsed > max_wait:
            raise TimeoutError(f"Export timed out after {max_wait} seconds")
        
        print(f"Export processing... (elapsed: {int(elapsed)}s)")
        time.sleep(poll_interval)
    
    return download_url


def download_file(download_url: str, output_path: str) -> None:
    """
    Download a file and save it to the specified path.
    
    Args:
        download_url: URL to download from
        output_path: Path where the file should be saved
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "wb") as f:
        try:
            response = requests.get(download_url, stream=True, timeout=60)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise RuntimeError(f"Failed to download file: {err}") from err
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
    
    print(f"  File downloaded to: {output_path}")


def main():
    """
    Main function to orchestrate the asset export and download process.
    """
    parser = argparse.ArgumentParser(
        description="Download an avatar from Meshcapade API using avatar ID"
    )
    parser.add_argument(
        "asset_id",
        type=str,
        help="ID of the avatar to download",
    )
    
    args = parser.parse_args()
    
    # Determine output path
    output_path = f"{args.asset_id}.glb"
    
    try:
        # Step 1: Get API token from .env file
        print("Step 1: Getting API token...")
        token = os.getenv("MESHCAPADE_API_TOKEN")
        if not token:
            raise ValueError("MESHCAPADE_API_TOKEN is not set in the environment variables")

        # Step 2: Export the avatar
        print("Step 2: Exporting avatar...")
        download_url = export_avatar(token, args.asset_id)
        print("Export completed!")
        
        # Step 3: Download the exported file
        print("Step 3: Downloading avatar...")
        download_file(download_url, output_path)
        
        print(f"\nSuccess! Avatar downloaded and saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()