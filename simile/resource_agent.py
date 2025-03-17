# simile/resource_agent.py
"""
Implements Agent-related methods.
We now hide async calls by automatically waiting on tasks.
"""

from .api_requestor import request
from .task import Task
from .error import RequestError

class Agent:
    @staticmethod
    def create(
        first_name,
        last_name,
        forked_agent_id="",
        speech_pattern="",
        self_description="",
        population_id=None,
        read_permission="private",
        write_permission="private",
        agent_data=None
    ):
        """
        Creates a new agent (blocking call).
        
        * first_name (required)
        * last_name  (required)
        * population_id (required)
        * read_permission (default: 'private')
        * write_permission (default: 'private')
        
        This function will not return until the creation is fully done server-side.
        
        Returns:
            agent_id (str): The new agent's unique ID.
        
        Raises:
            ValueError if required fields are missing.
            RequestError if the server returns an error.
        """
        # Validate required fields
        if not first_name:
            raise ValueError("first_name is required.")
        if not last_name:
            raise ValueError("last_name is required.")
        if not population_id:
            raise ValueError("population_id is required.")
        if not read_permission:
            raise ValueError("read_permission is required.")
        if not write_permission:
            raise ValueError("write_permission is required.")

        if agent_data is None:
            agent_data = []

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "forked_agent_id": forked_agent_id,
            "speech_pattern": speech_pattern,
            "self_description": self_description,
            "population_id": population_id,
            "read_permission": read_permission,
            "write_permission": write_permission,
            "agent_data": agent_data
        }

        # Kick off the creation, which returns a task
        resp = request("POST", "/create_single_agent/", json=payload)
        data = resp.json()
        task_id = data.get("task_id")
        if not task_id:
            raise RequestError("No 'task_id' returned from create_single_agent endpoint.")

        # The result endpoint is /create_single_agent_result/<task_id>/
        result_endpoint = "/create_single_agent_result/{task_id}/"

        # Wait for the task to finish
        final_data = Task(task_id, result_endpoint).wait()
        agent_id = final_data.get("agent_id")

        if not agent_id:
            raise RequestError("No 'agent_id' returned in final result.")

        return agent_id

    @staticmethod
    def retrieve_details(agent_id):
        """
        Synchronously retrieve agent details via GET /get_agent_details/.
        Returns a dict with details or raises RequestError on failure.
        """
        params = {"agent_id": agent_id}
        resp = request("GET", "/get_agent_details/", params=params)
        return resp.json()

    @staticmethod
    def delete(agent_id):
        """
        Synchronously delete an agent via POST /delete_agent/.
        Returns a dict with {status, message} or raises RequestError.
        """
        payload = {"agent_id": agent_id}
        resp = request("POST", "/delete_agent/", json=payload)
        return resp.json()

    @staticmethod
    def generate_response(agent_id, question_type, question_payload):
        """
        Generates an agent's response (blocking call).
        
        question_type can be 'categorical', 'numerical', or 'chat'.
        question_payload is a dict, e.g. { "question": "...", "options": [...] }
        
        Returns:
            The final result from the server once the async task completes.
        """
        payload = {
            "agent_id": agent_id,
            "question_type": question_type,
            "question": question_payload
        }
        resp = request("POST", "/generate_agent_response/", json=payload)
        data = resp.json()
        task_id = data.get("task_id")
        if not task_id:
            raise RequestError("No 'task_id' returned from generate_agent_response endpoint.")

        # The result endpoint is /generate_agent_response_result/<task_id>/
        result_endpoint = "/generate_agent_response_result/{task_id}/"

        # Wait and return final data
        final_data = Task(task_id, result_endpoint).wait()
        return final_data
