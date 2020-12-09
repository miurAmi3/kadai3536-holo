import json

import numpy as np
import tensorflow as tf
from PIL import Image

def loobe(c_name):
	with open(".\\pixiv\\signature.json", "r") as f:
		signature = json.load(f)

	inputs = signature.get('inputs')
	outputs = signature.get('outputs')

	session = tf.compat.v1.Session(graph=tf.Graph())
	tf.compat.v1.saved_model.loader.load(sess=session,tags=signature.get("tags"),export_dir='.\\pixiv\\.')

	input_width, input_height = inputs["Image"]["shape"][1:3]

	image = Image.open(str(c_name))
	image = image.resize((input_width, input_height))
	image = np.asarray(image) / 255.0
	feed_dict = {inputs["Image"]["name"]: [image]}
	fetches = [(key, output["name"]) for key, output in outputs.items()]

	output = session.run(fetches=[name for _, name in fetches], feed_dict=feed_dict)
	kekka = output[0][0].decode()
	return kekka