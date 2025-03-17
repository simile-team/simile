# simile/resource_population.py
"""
Implements Population-related methods.
Some are synchronous; get_sub_population is async but we now hide the wait.
"""

from .api_requestor import request
from .task import Task
from .error import RequestError

class Population:
    @staticmethod
    def create(name, read_permission="private", write_permission="private", readme=""):
        """
        Synchronously create a population via POST /create_population/.
        
        Required fields:
          - name
          - read_permission
          - write_permission
        Optional:
          - readme

        Returns:
            {
              "status": "success",
              "population_id": "..."
            }
        or raises an error.
        """
        if not name:
            raise ValueError("name is required.")
        if not read_permission:
            raise ValueError("read_permission is required.")
        if not write_permission:
            raise ValueError("write_permission is required.")

        payload = {
            "name": name,
            "read_permission": read_permission,
            "write_permission": write_permission,
            "readme": readme
        }
        resp = request("POST", "/create_population/", json=payload)
        return resp.json()

    @staticmethod
    def get_agents(population_id):
        """
        Synchronously get the agents in a population via GET /get_population_agents/.
        Returns { "agent_ids": [ ... ] }
        """
        params = {"population_id": population_id}
        resp = request("GET", "/get_population_agents/", params=params)
        return resp.json()

    @staticmethod
    def add_agent(population_id, agent_id):
        """
        Synchronously add an agent to a population via POST /population_add_agent/.
        Returns { "status": "...", "message": "..." } or raises an error.
        """
        payload = {
            "population_id": population_id,
            "agent_id": agent_id
        }
        resp = request("POST", "/population_add_agent/", json=payload)
        return resp.json()

    @staticmethod
    def remove_agent(population_id, agent_id):
        """
        Synchronously remove an agent from a population via DELETE /population_remove_agent/.
        Returns { "status": "...", "message": "..." } or raises an error.
        """
        payload = {
            "population_id": population_id,
            "agent_id": agent_id
        }
        resp = request("DELETE", "/population_remove_agent/", json=payload)
        return resp.json()

    @staticmethod
    def delete(population_id):
        """
        Synchronously delete a population via DELETE /delete_population/.
        Returns { "status": "...", "message": "..." }
        """
        payload = {"population_id": population_id}
        resp = request("DELETE", "/delete_population/", json=payload)
        return resp.json()

    @staticmethod
    def get_sub_population(population_id="", n=1):
        """
        Initiates a sub-population retrieval/generation (blocking call) by sampling
        from an existing population (if population_id is provided) or from all
        agents if no population_id is given.

        Endpoint: POST /get_sub_population/
        Waits until the async task completes, then returns final result, typically
        containing "new_population_id".
        """
        payload = {
            "population_id": population_id,
            "n": n
        }
        resp = request("POST", "/get_sub_population/", json=payload)
        data = resp.json()
        task_id = data.get("task_id")
        if not task_id:
            raise RequestError("No 'task_id' returned from get_sub_population endpoint.")

        # The result endpoint is /get_sub_population_result/<task_id>/
        result_endpoint = "/get_sub_population_result/{task_id}/"

        # Wait for completion and return the final result
        final_data = Task(task_id, result_endpoint).wait()
        return final_data
