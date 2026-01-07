## Issue

### Description

I used the Meshcapade create-from-video API to generate avatars + associated animation for 2 videos.
The asset IDs are:
 - ID1: 7fae7513-9860-4fa0-80a4-3dd1e75fb8d4
 - ID2: 994da76b-7f3c-400a-8c0c-e70815ba384c

If I log in to me.meshcapade.com and download the avatars from my Vault as glb files, both downloaded files include the animation data (skeletal + morph weight). This is expected.

If I use the python export.py script:
 - The export for ID1 is the same as the download from the web. Includes skeletal + morph weight animation data.
 - The export for ID2 does NOT include any animation data. It only includes the avatar mesh.
 => THIS IS NOT EXPECTED.

 ### Commands used
 
 See instruction below for setting up the script.
```bash
python export.py 7fae7513-9860-4fa0-80a4-3dd1e75fb8d4
python export.py 994da76b-7f3c-400a-8c0c-e70815ba384c
```
### Vide used as input
See file video.mp4 which was used for testing.


## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

1. Set the Meshcapade API token as an environment variable:
```bash
export MESHCAPADE_API_TOKEN="your-api-token-here"
```

2. Run the export script:
```bash
python export.py <asset_id>
```

Replace `<asset_id>` with the ID of the avatar you want to export.

The script will:
- Export the avatar in GLB format
- Wait for the export to complete
- Download the exported file to `<asset_id>.glb` in the current directory

### Example
```bash
export MESHCAPADE_API_TOKEN="abc123xyz"
python export.py my-avatar-id
```
