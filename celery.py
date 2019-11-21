def run_task():
   celery -A tasks worker -B --loglevel=INFO
