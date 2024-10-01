from flask import Flask,jsonify,request,Response
from flask_cors import CORS
from celery import Celery
from celery.result import AsyncResult
import time

app = Flask(__name__)
celery_app = Celery('celery-worker')

# Update the configuration explicitly
celery_app.conf.update(
    broker_url='redis://redis:6379/0',     # Explicitly set the broker URL
    result_backend='redis://redis:6379/0', # Explicitly set the backend URL
    broker_connection_retry_on_startup=True  # Ensure retry on startup
)


CORS(app)

@app.route("/")
def test():
   return "Flask Running"

@app.route('/stream_status/<task_id>')
def stream_status(task_id):
    def event_stream():
        while True:
            task = AsyncResult(task_id , app = celery_app)
            if task.state == 'SUCCESS':
                yield f"data: {task.result}\n\n"
                break
            elif task.state == 'FAILURE':
                yield f"data: Task failed: {task.info}\n\n"
                break
            else:
                yield f"data: {task.state}\n\n"
            time.sleep(1)  # Adjust the polling interval if needed
    response = Response(event_stream(), content_type='text/event-stream')
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/prime_factors', methods=['POST'])
def prime_factors():
    data = request.json
    number = int(data.get('number'))
    print(number)
    if number is None or not isinstance(number, int) or number <= 0:
        return jsonify({'error': 'Please provide a valid positive integer.'}), 400
    
    result = celery_app.send_task('tasks.count_prime_factors', args=[number])
    # print(result.state)
    return jsonify({'task_id': result.id}), 200

if __name__ == "__main__":
   app.run(debug=True)