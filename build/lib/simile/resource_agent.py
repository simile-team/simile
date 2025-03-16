# simile/resource_agent.py
"""
Implements Agent-related methods analogous to how you might use openai.Completion or similar classes.
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
        population_id="",
        read_permission="private",
        write_permission="private",
        agent_data=None
    ):
        """
        Asynchronously create an agent via POST /create_single_agent/
        Returns a Task object that you can poll or wait on.

        Usage:
            from simile import Agent
            task = Agent.create("John", "Doe")
            # block until done:
            result = task.wait()  # => {"agent_id": "..."}
            new_agent_id = result["agent_id"]
        """
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

        resp = request("POST", "/create_single_agent/", json=payload)
        data = resp.json()
        task_id = data.get("task_id")
        if not task_id:
            raise RequestError("No 'task_id' returned from create_single_agent endpoint.")

        # The result endpoint is /create_single_agent_result/<task_id>/
        result_endpoint = "/create_single_agent_result/{task_id}/"
        return Task(task_id, result_endpoint)

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
        Asynchronously generate an agent's response via /generate_agent_response/.
        question_type can be 'categorical', 'numerical', or 'chat'.
        question_payload is a dict. E.g. { "question": "...", "options": [...] }, etc.
        
        Returns a Task object for polling or waiting.
        Usage:
            from simile import Agent
            task = Agent.generate_response("a_123", "chat", {...})
            result = task.wait()
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
        return Task(task_id, result_endpoint)
