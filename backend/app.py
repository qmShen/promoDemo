from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

from StoryEvaluator import StoryEvaluator
import pandas as pd

FILE_ABS_PATH = os.path.dirname(__file__)

app = Flask(__name__)
CORS(app)
data_path = '{}/data/NBA_K.csv'.format(FILE_ABS_PATH)
df = pd.read_csv(data_path)
evaluator = StoryEvaluator(df, [])

@app.route('/api/test/counter/', methods=['POST'])
def update_counter():
    params = request.json
    counter = int(params['counter'])

    counter += 1

    resp = {'counter': counter}
    return jsonify(resp), 200, {"Content-Type": "application/json"}


@app.route('/api/test/fetchData/', methods=['POST'])
def fetch_data():
    data_path = '{}/data/NBA_K.csv'.format(FILE_ABS_PATH)
    df = pd.read_csv(data_path)
    df = df[df['measure'] == 'PTS']
    records = df.to_dict('record')
    return json.dumps(records)

@app.route('/api/test/evaluateFacts/', methods=['POST'])
def evaluate_story_facts():
    params = request.json
    print('params', params)
    evaluator.set_story_list(params)
    scores = evaluator.calc_score()
    print('scores', scores)
    return json.dumps(scores)


@app.route('/api/test/evaluateStories/', methods=['POST'])
def evaluate_stories():
    import time
    start_time = time.time()
    params = request.json
    factObjs = params
    print('evaluate_story_facts params', len(factObjs))
    for factObj in factObjs:
        ids = factObj['factIds']
        evaluator.set_story_list(ids)
        eva_results = evaluator.calc_score()
        del factObj['factIds']
        factObj['eva'] = eva_results
    print('result', time.time() - start_time)
    return json.dumps(factObjs)

if __name__ == '__main__':
    app.run()
