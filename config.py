from data import background, body, face, hat

'''
All Configurations needed for the Generator
Import all your Traits from a DB or another file
Add Traits in 'Trait Data' with whatever TraiteNames (Key) you choose

Trait Array Format:
    <Array> [
        <Dictionary> {
            "file": <string> - points to the Name of the actual image file [no need for extentsion in name, file must be .png] *can be empty
            "label": <string> - Call it what you want
            "weight": <int> - Weigt Distribution of randomly choosing this trait [Sum of all Traits has to be 100]
        }
    ]

Trait Directory: Parent Directory where the Trait Images are saved
Output Directory: Directory where all the Output exports
Output NFT Name: Name of the Output Files [a Number will be added at the End of the Filename]
Output JSON Name: Name of the Output JSON File with all the Statistics and NFT Traits
Output seperate JSON: Create a seperate JSON for each NFT with its traits
Generate Amount: Amount of NFTs to be generated
Image Size: Size of the NFT Images
Weighted Distribution: True => Use Weighted Distribution from your Traits, False => Equal Distribution for all Traits
Can Generate Empty: Traits with the possibility of not appearing in every NFT
Trait Data: Add your Traits the NFT will be generated from ['<NAME>': <Trait[]>]

NFT type: Type of the NFT for JSON Metadata

'''

config = {
    "Trait Directory": './art',
    "Output Directory": './output',
    "Output NFT Name": "nft_",
    "Output JSON Name": 'nft-data',
    "Output seperate JSON": True,
    "NFT type": 'object',
    "Generate Amount": 20,
    "Image Size": [280, 280],
    "Weighted Distribution": True,
    "Can Generate Empty": ["Hat"],
    "Trait Data": {
        "Background": background,
        "Body": body,
        "Face": face,
        "Hat": hat
    }
}