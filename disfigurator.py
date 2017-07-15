from flask import Flask, jsonify, request
import random

app = Flask(__name__)

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def choice():
	return random.choice([True, False])

def isUpper(let):
	return let == let.upper()

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

def mutate(phrase):
	out = ""
	for let in phrase:
		if let not in alphabet:
			out = out + let
		else:
			if choice():
				out = out + str(let).upper()
			else:
				out = out + str(let).lower()
	return out

def crossover(pivot, messageA, messageB):
	halfAA, halfAB = messageA[:pivot], messageB[pivot:]
	halfBA, halfBB = messageB[:pivot], messageB[pivot:]
	crossA = halfAA + halfBB
	crossB = halfBA + halfAB
	fitA = fitness(crossA)
	fitB = fitness(crossB)
	if fitA > fitB:
		return crossA
	return crossB

def genetic_dumbify(message):
	GENERATION_COUNT = 100
	GENERATION_POPULATION = 20
	best_message = mutate(message)
	best_fit = fitness(best_message)
	for generation in range(GENERATION_COUNT):
		best_in_generation = best_message
		best_fit_generation = fitness(best_in_generation)
		for entity in range(GENERATION_POPULATION):
			pivot = random.randint(0, len(message))
			resp = crossover(pivot, best_in_generation, mutate(best_in_generation))
			if fitness(resp) > best_fit_generation:
				best_in_generation = resp
				best_fit_generation = fitness(resp)
		if best_fit_generation > best_fit:
			best_fit = best_fit_generation
			best_message = best_in_generation
			if best_fit == 1.0:
				return best_message
	return best_message



@app.route('/disfigure')
def disfigurate():
	message = request.args.get("phrase")
	output = genetic_dumbify(message)	
	return jsonify({"phrase" : output})

def main():
	app.run(host="0.0.0.0", port=8000, threaded=True)

main()
