from flask import Flask, jsonify, request
import random
import string

app = Flask(__name__)

def dumbify(message):
	# alternate upper/lower transformations, left-to-right, randomly choosing 1, 2, or 3 characters at a time
	i = 0
	upper = random.choice([True, False])
	while i < len(message):
		c = random.choice([1,2,3])
		c = min(len(message)-i, c)
		if upper:
			message = message[0:i] + string.upper(message[i:i+c]) + message[i+c:]
		else:
			message = message[0:i] + string.lower(message[i:i+c]) + message[i+c:]
		upper = not upper
		i += c
	return message

@app.route('/disfigure')
def disfigurate():
	message = request.args.get("phrase")
	output = dumbify(message)	
	return jsonify({"phrase" : output})

def main():
	app.run(host="0.0.0.0", port=8000, threaded=True)

main()
