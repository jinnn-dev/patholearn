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
        },
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )
    return response.json()["data"]["projects"]


def get_projects():
    response = httpx.post(
        f"{Config.CLEARML_API}/projects.get_all_ex",
        json={
            "active_users": ["2bb19837bfc846c98ef34e0388ef3028"],
        },
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )
    return response.json()["data"]["projects"]
