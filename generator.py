import os
from pathlib import Path
from PIL import Image
from random import randint
import json

from config import config

###########################################
# VARIABLE DECLARATION AND INITIALIZATION #
###########################################

#Load in all the Configuration for easier use
dir = config["Trait Directory"]
outputDir = config["Output Directory"]
outputName = config["Output NFT Name"]
jsonName = config["Output JSON Name"]
seperateJson = config['Output seperate JSON']
amountToGen = config["Generate Amount"]
imageSize = config["Image Size"]
useWeightedDistribution = config["Weighted Distribution"]
canBeEmpty = config["Can Generate Empty"]
traitData = config['Trait Data']

nftType = config['NFT type']

#Declare and Initialize Variables
traits = traitData.keys()
statsTraits = {}
nfts = {}
count = {}
maxGen = 0
position = [0,0]
generated = [0]*amountToGen


#Count all Possibilities for each Trait AND calculate Maximum non-duplicate Possibilities
for trait in traits:
	count[trait] = len([item for item in os.listdir(dir + '/' + trait)])
	if trait in canBeEmpty:
		count[trait] += 1
	maxGen = count[trait] if maxGen == 0 else maxGen * count[trait]

print("Maximum is "+str(maxGen))

#Make sure no more NFTs are generated then possible [Prevent Duplicates]
if amountToGen > maxGen:
	amountToGen = maxGen

####################
# HELPER FUNCTIONS #
####################

'''
Update Statistics of Traits in Dictionary with Label instead of Int [getTraitLabel]
@param <string>trait - Name of the Trait
@param <int>id - Trait Index
'''
def addStat(trait, id):
	traitName = getTraitLabel(trait, id)
	if (trait in statsTraits):
		if traitName in statsTraits[trait]:
			statsTraits[trait][traitName] += 1
		else:
			statsTraits[trait][traitName] = 1
	else:
		statsTraits[trait] = {}
		statsTraits[trait][traitName] = 1

'''
Return the Trait Index from all the weighted Pairs
@param <Pair(<int>, <int>)>pairs - <Array>[(Weight, Trait Index), ...]
@return <int>
'''
def weighted_random(pairs):
    total = sum(pair[0] for pair in pairs)
    r = randint(1, total)
    for (weight, value) in pairs:
        r -= weight
        if r <= 0: return value

'''
Get All Trait Weight Distribution Pairs(Weight, Trait Index) for one Trait
@param <string>trait - Trait Name
@return <Array>[Pair(Wieght, Trait Index), ...]
'''
def getWeight(trait):
	data = traitData[trait]
	pairs = [0] * len(data)
	for i, trait in enumerate(data):
		pairs[i] = (trait["weight"], i)
	return pairs

'''
Get the Trait Label
@param <string>trait - Trait Name
@param <int>id - Trait Index
@return <string>
'''
def getTraitLabel(trait, id):
	return traitData[trait][id]["label"]

'''
Get Trait Filename
@param <string>trait - Trait Name
@param <int>id - Trait Index
@return <string>
'''
def getTraitFile(trait, id):
	return traitData[trait][id]["file"]


'''
Generate a NFT with random Traits
@return <Dictionary>{"traits": <Dictionary>{Trait: Trait Index, ...} "gen": <string>NFT 'Hash'}
'''
def generateNftTraits():
	nft = {}
	gen = ''
	for trait in traits:
		traitId = None

		#Choose wheter to use Trait Weighted Distribution or not
		if useWeightedDistribution:
			traitId = weighted_random(getWeight(trait))
		else:
			traitId = randint(1, count[trait]) - 1 if trait in canBeEmpty else randint(0, count[trait] - 1)

		nft[trait] = traitId
		#Generate a NFT 'Hash' for Duplication Check '<trait><trait><trait>...'
		gen = (f'{gen}{traitId}')
	return {"traits": nft, "gen": gen}

'''
Generate a NFT with Trait Labels instead of Trait Indices [getTraitLabel]
@param nft - <Dictionary>{Trait: Trait Index, ...}
@return <Dictionary>{Trait: Trait Label, ...}
'''
def getJsonNft(nft):
	jsonNft = {}
	for trait in traits:		
			traitId = nft[trait]
			jsonNft[trait] = getTraitLabel(trait, traitId)
	return jsonNft


'''
Generate a NFT with all Metadata for JSON export
@id - <int>ID of the NFT
@param nft - <Dictionary>{Trait: Trait Index, ...}
@return <Dictionary>{<Metadata>}
'''
def constructJsonMetadata(id, nft):	
	properties = {
		'name': f'{outputName}{id}',
		'description': '',
		'image': f'<ipfs-link>/{outputName}{id}.png',
		'attributes': getJsonNft(nft),
	}

	jsonNft = {
		'title': 'Asset Metadata',
		'type': nftType,
		'properties': properties,
	}

	return jsonNft


#Make sure the Output Directory exists, if not, create one 
Path(outputDir).mkdir(parents=True, exist_ok=True)

#################
# NFT GENERATOR #
#################

'''
Generate NFTs until the specified Amount is reached [Generate Amount]
Prevent Duplicates
Output Images
'''
counter = 1
while len([item for item in os.listdir(outputDir)]) < amountToGen:
	id = counter

	#Generate NFT with random Traits
	generatedNft = generateNftTraits()
	nft = generatedNft["traits"]
	gen = generatedNft["gen"]

	#Check for Duplicates
	if gen in generated:
		#Skip Duplicate
		print("Duplicate found")
	else:
		#Generate blank NFT Image
		render = Image.new('RGBA', imageSize)

		#Go through each Trait and generate the final NFT Image
		for trait in traits:		
			traitId = nft[trait]

			#Update Statistics Dictionary
			addStat(trait, traitId)

			#Get Trait Image File and Merge it with the existing NFT Image
			file = getTraitFile(trait, traitId)
			if file != "":
				image = Image.open(f'{dir}/{trait}/{getTraitFile(trait, traitId)}.png').convert("RGBA")
				render.paste(image, position, mask=image)
		
		#Save current NFT 'Hash' for next Duplicate Check
		generated[id - 1] = gen		

		#Add NFT with Trait Labels to NFTs Dictionary
		nfts[id] = getJsonNft(nft)

		#Output NFT Image
		render.save(f'{outputDir}/{outputName}{id}.png')

		#Output seperate JSON Files
		if seperateJson:
			jsonNft = constructJsonMetadata(id, nft)
			with open(f'./{outputDir}/{outputName}{id}.json', 'w') as outfile:
				json.dump(jsonNft, outfile)

		#Increase ID Counter
		counter += 1
			


#####################
# STATISTICS OUTPUT #
#####################

#Prepare Statistics for easier use later
data = {
	"statistics": statsTraits,
	"nfts": nfts
}

#Output a JSON File with all Statistics and NFTs Information
with open(f'./{outputDir}/{jsonName}.json', 'w') as outfile:
	json.dump(data, outfile)

#Output a JSON File with all Statistics
if seperateJson:
	with open(f'./{outputDir}/statistics.json', 'w') as outfile:
		json.dump(statsTraits, outfile)
