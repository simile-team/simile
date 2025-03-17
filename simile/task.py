# simile/task.py
import time
from .api_requestor import request

class Task:
    """
    Represents an asynchronous Celery-like task. 
    Contains logic for polling the result endpoint until completion or failure.
    Used internally to hide the async nature from the end user.
    """
    def __init__(self, task_id, result_endpoint):
        self.task_id = task_id
        self.result_endpoint = result_endpoint  # e.g. '/generate_agent_response_result/{task_id}/'
        self._last_status = None
        self._last_result = None
        self._finished = False

    @property
    def last_status(self):
        """Returns the last known status from the server."""
        return self._last_status

    @property
    def result(self):
        """If the task has finished successfully, returns the result payload."""
        if self._finished and self._last_status == "SUCCESS":
            return self._last_result
        return None

    @property
    def error(self):
        """If the task has failed, returns the error message."""
        if self._finished and self._last_status == "FAILURE":
            return self._last_result
        return None

    def poll(self):
        """
        Perform a single poll to the result endpoint,
        storing the status in self._last_status and marking self._finished if done.
        """
        url = self.result_endpoint.format(task_id=self.task_id)
        resp = request("GET", url)
        data = resp.json()

        status_ = data.get("status")
        self._last_status = status_

        if status_ == "PENDING":
            # still running
            pass
        elif status_ == "SUCCESS":
            self._finished = True
            self._last_result = data.get("result") or data.get("data")
        elif status_ == "FAILURE":
            self._finished = True
            self._last_result = data.get("error")
        else:
            # Some other custom statuses are treated as "still running"
            pass

    def wait(self, interval=2, timeout=300):
        """
        Poll in a loop until the task finishes or times out.
        Returns the final result on success, or raises an exception on failure or timeout.
        """
        start = time.time()
        while True:
            self.poll()
            if self._finished:
                break
            if time.time() - start > timeout:
                raise TimeoutError(
                    f"Task {self.task_id} did not complete within {timeout} seconds."
                )
            time.sleep(interval)

        if self._last_status == "SUCCESS":
            return self._last_result
        else:
            raise RuntimeError(f"Task {self.task_id} failed with error: {self._last_result}")
