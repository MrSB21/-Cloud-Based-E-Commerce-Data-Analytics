from flask import Flask, render_template, request, jsonify
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-query')
def run_query():
    query_type = request.args.get('query')

    if query_type == 'delivery':
        query = """SELECT * FROM `cc-coursework-sb.thelook.query1_view` LIMIT 10"""
    elif query_type == 'returns':
        query = """SELECT * FROM `cc-coursework-sb.thelook.query2_view` LIMIT 10"""
    else:
        return jsonify({'error': 'Invalid query type'}), 400

    try:
        job = client.query(query)
        results = job.result()
        data = [dict(row.items()) for row in results]
        return jsonify({'results': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
