import tensorflow as tf
import sys
import pandas as pd
import time

# # change this as you see fit
# # image_path = sys.argv[1]
# image_path = 'testImages/image.jpg'
#
#
#
# # Loads label file, strips off carriage return
# label_lines = [line.rstrip() for line in tf.io.gfile.GFile("Breed_Cat/retrained_labels.txt")]

# Unpersists graph from file
# start = time.time()

graph = tf.get_default_graph()
with tf.gfile.FastGFile("Breed_Cat/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
# print("load model time: " ,time.time()-start)

def predict():
    start = time.time()
    with graph.as_default():
        # change this as you see fit
        # image_path = sys.argv[1]
        image_path = 'testImages/image.jpg'

        # Loads label file, strips off carriage return
        label_lines = [line.rstrip() for line in tf.io.gfile.GFile("Breed_Cat/retrained_labels.txt")]


        # Read in the image_data
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            # print("1 ", time.time()-start)
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

            # print("2 ", time.time()-start)
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            top_k = top_k[0:3]
            result = []
            for node_id in top_k:
                cat_string = label_lines[node_id].capitalize().replace(' ', '_')
                score = round(predictions[0][node_id] * 100, 2)
                result.append([cat_string, score])
                # print('%s (score = %.5f)' % (human_string, score))
            prediction_ = pd.DataFrame(result, columns=['Breed', 'Probability'])
            prediction_.Probability = [str(x) + '%' for x in prediction_.Probability]
            print(prediction_)
            # print("3 ", time.time() -start)
            return prediction_



