from typing import Dict, List
from clearml import Dataset
import httpx

from app.config.config import Config
from app.core.train.train_model import start_training


def ping():
    try:
        with httpx.Client() as client:
            response = client.post(
                f"{Config.CLEARML_API}/debug.ping",
                auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
                timeout=100,
            )
            if response.json()["data"]["msg"] == "ClearML server":
                return "Ok"
            return "Error"
    except (httpx.ConnectError, httpx.ConnectTimeout) as e:
        print(e)
        return "Error"


def get_specific_dataset(dataset_id):
    with httpx.Client() as client:
        response = client.post(
            f"{Config.CLEARML_API}/tasks.get_all_ex",
            json={
                "id": [],
                "project": [dataset_id],
                "order_by": ["-last_update"],
                "type": ["data_processing"],
                "user": [],
                "system_tags": ["__$and", "__$not", "archived", "dataset"],
                "include_subprojects": False,
                "search_hidden": True,
                "only_fields": [
                    "name",
                    "status",
                    "system_tags",
                    "project",
                    "company",
                    "last_change",
                    "started",
                    "last_iteration",
                    "tags",
                    "user.name",
                    "runtime.progress",
                    "hyperparams.properties.version.value",
                    "project.name",
                    "last_update",
                    "runtime._pipeline_hash",
                    "runtime.version",
                    "execution.queue",
                    "type",
                    "hyperparams.properties.version",
                ],
            },
            auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
        )
    return response.json()["data"]["tasks"][0]


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


def get_datatset_debug_images(dataset_id: str):
    with httpx.Client() as client:
        response = client.post(
            f"{Config.CLEARML_API}/events.debug_images",
            json={
                "metrics": [
                    {
                        "task": dataset_id,
                    }
                ],
                "iters": 10,
            },
            auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
        )
    events = response.json()["data"]["metrics"][0]["iterations"][0]["events"]
    urls = []
    for event in events:
        urls.append(event["url"].replace("s3", "http"))
    return urls


def create_project(project_name: str, description: str = None):
    with httpx.Client() as client:
        response = client.post(
            f"{Config.CLEARML_API}/projects.create",
            json={"name": project_name, "description": description},
            auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
        )

    return response.json()["data"]


def delete_project(project_id: str):
    with httpx.Client() as client:
        response = client.post(
            f"{Config.CLEARML_API}/projects.delete",
            json={"delete_contents": True, "project": project_id},
            auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
        )
    return response.json()["data"]


def get_projects():
    response = httpx.post(
        f"{Config.CLEARML_API}/projects.get_all_ex",
        json={
            "active_users": ["2bb19837bfc846c98ef34e0388ef3028"],
            "include_stats": True,
            "search_hidden": True,
        },
        auth=(Config.CLEARML_API_ACCESS_KEY, Config.CLEARML_API_SECRET_KEY),
    )
    return response.json()["data"]["projects"]


def get_project(project_id: str):
    response = httpx.post(
        f"{Config.CLEARML_API}/projects.get_by_id",
        json={"project": project_id, "include_dataset_stats": True},
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


def create_task_and_enque(data: dict):
    dataset_task = get_specific_dataset(data["dataset_id"])
    data["dataset_id"] = dataset_task["id"]
    project = get_project(data["project_id"])
    data["project_name"] = project["name"]
    return start_training(data)


def get_task(task_id: str):
    response = httpx.post(
        f"{Config.CLEARML_API}/tasks.get_by_id_ex",
        json={
            "id": [task_id],
            "only_fields": [
                "id",
                "name",
                "status",
                "project",
                "last_worker",
                "runtime",
            ],
        },
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


def create_dataset(
    dataset_name: str,
    dataset_description: str,
    dataset_project: str,
    dataset_tags: List[str],
):
    dataset = Dataset.create(
        dataset_name=dataset_name,
        dataset_project=dataset_project,
        description=dataset_description,
        dataset_tags=dataset_tags,
        output_uri="s3://10.168.2.83:9000/clearml",
    )
    return dataset


def add_files_to_dataset(dataset: Dataset, folder_path: str):
    dataset.add_files(folder_path)
    dataset.upload()


def set_metadata_of_dataset(dataset: Dataset, metadata: Dict):
    return dataset.set_metadata(metadata, ui_visible=False)


def finalize_dataset(dataset: Dataset):
    dataset.finalize(raise_on_error=True)


def get_dataset_task(dataset: Dataset):
    return get_task(dataset.id)
