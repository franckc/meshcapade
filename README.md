# meshcapade
Bug repro

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
