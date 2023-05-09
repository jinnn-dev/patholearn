import json
from typing import List

from clearml.backend_api.session.client import APIClient, StrictSession
from clearml.backend_api.session.client.client import TableResponse, Entity
from clearml.backend_api.services.v2_23.projects import ProjectsGetAllResponseSingle
import httpx

from app.config.config import Config

session = StrictSession(initialize_logging=True)


def get_datasets():
    # client = APIClient(session=session)

    # result: TableResponse = client.projects.get_all(
    #     name="/\\.datasets/", search_hidden=True
    # )
    # response: List[Entity] = result.response
    # print(len(response))
    # projects = []
    # for entity in response:
    #     print(entity)
    #     projects.append({"id": entity.id, "name": entity.name})
    response = httpx.post(
        f"{Config.CLEARML_API}/projects.get_all_ex",
        json={
            "search_hidden": True,
            "name": "/\\.datasets/",
            "system_tags": ["dataset"],
            "include_dataset_stats": True,
        },
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )
    return response.json()["data"]["projects"]


def create_project(project_name: str, description: str = None):
    with httpx.Client() as client:
        response = client.post(
            f"{Config.CLEARML_API}/projects.create",
            json={"name": project_name, "description": description},
            auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
        )

    return response.json()["data"]


def get_projects():
    response = httpx.post(
        f"{Config.CLEARML_API}/projects.get_all_ex",
        json={
            "active_users": ["2bb19837bfc846c98ef34e0388ef3028"],
            "include_stats": True,
        },
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )
    return response.json()["data"]["projects"]


def get_project(project_id: str):
    print(project_id)
    response = httpx.post(
        f"{Config.CLEARML_API}/projects.get_by_id",
        json={"project": project_id},
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )
    return response.json()["data"]["project"]


def get_tasks_to_project(project_id: str):
    response = httpx.post(
        f"{Config.CLEARML_API}/tasks.get_all_ex",
        json={
            "project": [project_id],
            "only_fields": [
                "id",
                "name",
                "type",
                "status",
                "status_reason",
                "status_message",
                "status_changed",
                "created",
                "started",
                "last_update",
                "last_change",
                "last_changed_by",
            ],
        },
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )
    return response.json()["data"]["tasks"]


def get_task(task_id: str):
    response = httpx.post(
        f"{Config.CLEARML_API}/tasks.get_by_id_ex",
        json={"id": [task_id]},
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )

    return response.json()["data"]["tasks"][0]


def get_task_log(task_id: str):
    response = httpx.post(
        f"{Config.CLEARML_API}/events.get_task_log",
        json={"task": task_id, "navigate_earlier": True},
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )

    return response.json()["data"]["events"]


def get_task_metrics(task_id: str):
    response = httpx.post(
        f"{Config.CLEARML_API}/events.scalar_metrics_iter_histogram",
        json={"key": "iter", "task": task_id},
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )
    return response.json()["data"]
