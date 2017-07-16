from flask import Flask, jsonify, request
import random
import numpy.random
import operator

app = Flask(__name__)

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def choice():
	return random.choice([True, False])

def isUpper(let):
	return let == let.upper()

# We don't want a chain of upper/lower letters in a row longer than three. Every violation lowers the fitness level
def fitness(message):
	FITNESS_NEIGHBOR_CAP = 3
	count = 1.0
	total = 0.0
	upper = False
	for let in message:
		if let in alphabet:
			if isUpper(let):
				if upper == False:
					upper = True
					count = 0
				else:
					count = count + 1
			else:
				if upper == True:
					upper = False
					count = 0
				else:
					count = count + 1
			if count >= FITNESS_NEIGHBOR_CAP:
				total = total + 1
	if total < 1.0:
		return 1.0
	return 1.0 - (total / len(message))

def swap(letter):
	if isUpper(letter):
		return letter.lower()
	else:
		return letter.upper()

# Randomly mutate either one, or roughly ten percent of, letter(s) in the message
def mutate(phrase):
	message = list(phrase)
	ten_percent = int(((len(message) * 1.0) * 0.1)) if len(message) > 10 else 1
	for i in range(0, ten_percent):
		ind = random.randint(0, len(message) - 1)
		if message[ind] in alphabet:
			message[ind] = swap(message[ind])
	return "".join(message)


def crossover(pivot, messageA, messageB):
	halfAA, halfAB = messageA[:pivot], messageB[pivot:]
	halfBA, halfBB = messageB[:pivot], messageB[pivot:]
	crossA = halfAA + halfBB
	crossB = halfBA + halfAB
	candidates = [messageA, messageB, crossA, crossB]
	# Let us get the best possible outcome of this crossover 
	return sorted(candidates, key=fitness).pop()
	

def genetic_dumbify(message):
	GENERATION_COUNT = 25
	GENERATION_POPULATION = 10
	MAX_SPECIES_POPULATION = 15
	livingPopulation = list()
	# We firstly have to have some initial parents. Let's have the initial message, and a slightly mutated one.
	initParentA = message
	initParentB = mutate(message)
	livingPopulation.append(initParentA)
	livingPopulation.append(initParentB)
	for generation in range(GENERATION_COUNT):
		bestInPack = sorted(livingPopulation, key=fitness)
		parentA = bestInPack[len(bestInPack) - 1]
		parentB = bestInPack[len(bestInPack) - 2]
		for entity in range(GENERATION_POPULATION):
			pivot = random.randint(0, len(message))
			# Breed parents and get a child with a slight mutation
			livingPopulation.append(mutate(crossover(pivot, parentA, parentB)))
		# The stronger live, the weaker don't. Let's cull the herd.
		if len(livingPopulation) > MAX_SPECIES_POPULATION:
			culledHerd = list()
			sortedHerd = sorted(livingPopulation, key=fitness)
			for i in range(MAX_SPECIES_POPULATION):
				tmp = sortedHerd.pop()
				culledHerd.append(tmp)
			culledHerd = list(reversed(culledHerd))
			# Let's randomly kill off one of the "leaders of the pack"
			if choice():
				_ = culledHerd.pop()
			livingPopulation = culledHerd
	return sorted(livingPopulation, key=fitness).pop()



@app.route('/disfigure')
def disfigurate():
	message = request.args.get("phrase")
	output = genetic_dumbify(message)	
	return jsonify({"phrase" : output})

def main():
	app.run(host="0.0.0.0", port=8000, threaded=True)

main()
