I used the Meshcapade create-from-video API to generate avatars + associated animation for 2 videos.
The asset IDs are:
 - ID1: 7fae7513-9860-4fa0-80a4-3dd1e75fb8d4
 - ID2: 994da76b-7f3c-400a-8c0c-e70815ba384c

If I log in to me.meshcapade.com and download the avatars from my Vault as glb files, both downloaded files include the animation data (skeletal + morph weight). This is expected.

If I use the python export.py script:
 - The export for ID1 is the same as the download from the web. Includes skelet + morph weight animation data.
 - The export for ID2 does NOT include any animation data. It only includes the avatar mesh.
 => THIS IS NOT EXPECTED.

