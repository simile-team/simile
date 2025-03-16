# simile/resource_population.py
"""
Implements Population-related methods: create, get_agents, add_agent, remove_agent, delete, etc.
"""

from .api_requestor import request
from .task import Task
from .error import RequestError

class Population:
    @staticmethod
    def create(name="New Population"):
        """
        Synchronously create a population via POST /create_population/.
        Returns a dict { "status": "success", "population_id": "..." } or raises an error.
        """
        payload = {"name": name}
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
    def create_sub_population(population_id="", n=1):
        """
        Asynchronously create a sub-population by sampling from an existing population
        or from all agents if no population_id is given.
        Endpoint: POST /create_sub_population/
        Returns a Task object. On success, final data should have "new_population_id".
        """
        payload = {
            "population_id": population_id,
            "n": n
        }
        resp = request("POST", "/create_sub_population/", json=payload)
        data = resp.json()
        task_id = data.get("task_id")
        if not task_id:
            raise RequestError("No 'task_id' returned from create_sub_population endpoint.")

        # The result endpoint is /create_sub_population_result/<task_id>/
        result_endpoint = "/create_sub_population_result/{task_id}/"
        return Task(task_id, result_endpoint)
