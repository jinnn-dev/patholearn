from sqlalchemy import inspect
import sqlalchemy as sal
from sqlalchemy import text
import requests
import json
import argparse
import os

from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.task_statistic import TaskStatistic
from app.models.user_solution import UserSolution

import app.models as models


def import_user_into_supertokens(email: str, password_hash: str) -> str:
    url = "http://supertokens:3567/recipe/user/passwordhash/import"
    body = {"email": email, "passwordHash": password_hash, "hashingAlgorithm": "bcrypt"}
    headers = {"content-type": "application/json"}

    result = requests.post(url, data=json.dumps(body), headers=headers)
    return result.json()["user"]["id"]


def set_metadata(user_id: str, firstname: str, lastname: str):
    url = "http://supertokens:3567/recipe/user/metadata"
    body = {
        "userId": user_id,
        "metadataUpdate": {"first_name": firstname, "last_name": lastname},
    }

    headers = {"content-type": "application/json"}

    result = requests.put(url, data=json.dumps(body), headers=headers)
    return result.status_code


def import_user_into_new_db(user_mapping: dict):
    with Session(new_db_engine) as conn:
        user_create = UserCreate(
            email=user_mapping["email"],
            id=user_mapping["new_id"],
            firstname=(
                user_mapping["firstname"].strip()
                + (
                    (" " + user_mapping["middlename"].strip())
                    if user_mapping["middlename"]
                    else ""
                )
            ),
            lastname=user_mapping["lastname"],
            is_superuser=user_mapping["is_superuser"],
            last_login=user_mapping["last_login"],
        )
        crud_user.create(db=conn, obj_in=user_create)


def get_users_from_old_db():
    with old_db_engine.connect() as conn:
        users_result = conn.execute(text("SELECT * FROM user"))

    return users_result.fetchall()


def select_everythin_from_table(table_name: str):
    with old_db_engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table_name}"))
    return result.fetchall()


def import_row(model_type, import_data, user_mapping, user_id_column):
    with Session(new_db_engine) as db:
        new_row = model_type(**import_data)
        if user_id_column:
            setattr(
                new_row,
                user_id_column,
                user_mapping[getattr(new_row, user_id_column)]["new_id"],
            )
        db.add(new_row)
        db.commit()


# def import_course_into_new_db(course, user_mapping: dict):
#     owner_id = course["owner_id"]

#     with Session(new_db_engine) as db:
#         new_course = Course(**course)
#         new_course.owner_id = user_mapping[owner_id]["new_id"]
#         db.add(new_course)
#         db.commit()


# def import_course_members_into_new_db(course_member, user_mapping: dict):
#     member_id = course_member["user_id"]

#     with Session(new_db_engine) as db:
#         new_course_member = CourseMembers(**course_member)
#         new_course_member.user_id = user_mapping[member_id]["new_id"]
#         db.add(new_course_member)
#         db.commit()


# def import_task_group_into_new_db(task_group, user_mapping: dict):
#     with Session(new_db_engine) as db:
#         task_group = TaskGroup(**task_group)
#         db.add(task_group)
#         db.commit()


# def import_base_task_into_new_db(base_task, user_mapping: dict):
#     with Session(new_db_engine) as db:
#         base_task = BaseTask(**base_task)
#         db.add(base_task)
#         db.commit()


# def import_task_into_new_db(task: Task, user_mapping: dict):

#     new_task = Task(**task)
#     if (task.task_data is None)
#     delattr(task, new_task)
# with Session(new_db_engine) as db:
#     task = models.task.Task()

#     db.add(task)
#     db.commit()


def import_task_into_new_db(task, user_mapping: dict):
    new_task = Task(**task._mapping)
    if new_task.solution is None:
        delattr(new_task, "solution")
    else:
        new_task.solution = json.loads(new_task.solution)
    if new_task.task_data is None:
        delattr(new_task, "task_data")
    else:
        new_task.task_data = json.loads(new_task.task_data)
    if new_task.annotation_groups is None:
        delattr(new_task, "annotation_groups")
    else:
        new_task.annotation_groups = json.loads(new_task.annotation_groups)
    if new_task.info_annotations is None:
        delattr(new_task, "info_annotations")
    else:
        new_task.info_annotations = json.loads(new_task.info_annotations)
    with Session(new_db_engine) as db:
        db.add(new_task)
        db.commit()


def import_user_solution_into_new_db(user_solution, user_mapping: dict):
    new_user_solution = UserSolution(**user_solution._mapping)
    if user_solution.solution_data is None:
        delattr(new_user_solution, "solution_data")
    else:
        new_user_solution.solution_data = json.loads(new_user_solution.solution_data)
    if user_solution["task_result"] is None:
        delattr(new_user_solution, "task_result")
    else:
        new_user_solution.task_result = json.loads(new_user_solution.task_result)

    new_user_solution.user_id = user_mapping[new_user_solution.user_id]["new_id"]
    with Session(new_db_engine) as db:
        db.add(new_user_solution)
        db.commit()


def import_task_statistics(task_statistic, user_mapping: dict):
    new_task_statistic = TaskStatistic(**task_statistic._mapping)
    if new_task_statistic.solution_data is None:
        delattr(new_task_statistic, "solution_data")
    else:
        new_task_statistic.solution_data = json.loads(new_task_statistic.solution_data)

    if new_task_statistic.task_result is None:
        delattr(new_task_statistic, "task_result")
    else:
        new_task_statistic.task_result = json.loads(new_task_statistic.task_result)
    new_task_statistic.user_id = user_mapping[new_task_statistic.user_id]["new_id"]
    with Session(new_db_engine) as db:
        db.add(new_task_statistic)
        db.commit()


def make_import(table_name, model_type, user_id_column, import_name):
    print(f"Importing {import_name}...")
    for element in select_everythin_from_table(table_name):
        import_row(
            model_type=model_type,
            import_data=element._mapping,
            user_id_column=user_id_column,
            user_mapping=user_mapping,
        )
    print("Done")


# def import_new_task_into_new_db(new_task, user_mapping: dict):
#     with Session(new_db_engine) as db:
#         new_task = NewTask(**new_task)
#         new_task.user_id = user_mapping[new_task.user_id]["new_id"]
#         db.add(new_task)
#         db.commit()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Database Migration",
        description="Migrates an old database to the new authentication service",
    )
    parser.add_argument("-odb", "--old_db", default="db")
    parser.add_argument("-ndb", "--new_db", default="patholearn_db")
    parser.add_argument("-sdb", "--supertokens_db", default="supertokens")
    parser.add_argument("-sip", "--supertokens_db_ip", default="db")
    parser.add_argument("-su", "--supertokens_db_user", default="supertoken_db_user")
    parser.add_argument(
        "-sp", "--supertokens_db_password", default="supertoken_password"
    )

    args = parser.parse_args()

    learn_db_ip = os.environ.get("MYSQL_HOST", "lern_db")
    learn_db_user = os.environ.get("MYSQL_USER", "user")
    learn_db_password = os.environ.get("MYSQL_PASSWORD", "password")

    old_db_engine = sal.create_engine(
        f"mysql+mysqlconnector://{learn_db_user}:{learn_db_password}@{learn_db_ip}/{args.old_db}"
    )
    new_db_engine = sal.create_engine(
        f"mysql+mysqlconnector://{learn_db_user}:{learn_db_password}@{learn_db_ip}/{args.new_db}"
    )
    supertokens_db_engine = sal.create_engine(
        f"mysql+mysqlconnector://{args.supertokens_db_user}:{args.supertokens_db_password}@{args.supertokens_db_ip}/{args.supertokens_db}"
    )

    with Session(new_db_engine) as conn:
        conn.execute(text("DELETE FROM user WHERE email = 'admin@admin.de'"))
        conn.commit()

    user_mapping = {}

    for user in get_users_from_old_db():
        user_id = user["id"]
        firstname = user["firstname"]
        middlename = user["middlename"]
        lastname = user["lastname"]
        email = user["email"]
        hashed_password = user["hashed_password"]
        is_activae = user["is_active"]
        is_superuser = user["is_superuser"]
        last_login = user["last_login"]

        supertoken_user_id = import_user_into_supertokens(email, hashed_password)
        print(supertoken_user_id)
        set_metadata(
            supertoken_user_id,
            f"{firstname.strip() or ''}{' ' + middlename.strip() if middlename else ''}",
            lastname or "",
        )

    user_mapping[user_id] = {"new_id": supertoken_user_id, **(user._mapping)}

    import_user_into_new_db(user_mapping[user_id])

    make_import("course", models.course.Course, "owner_id", "Courses")
    make_import(
        "coursemembers",
        models.course_members.CourseMembers,
        "user_id",
        "Course members",
    )
    make_import("taskgroup", models.task_group.TaskGroup, None, "Task groups")
    make_import("basetask", models.base_task.BaseTask, None, "Base tasks")

    for task in select_everythin_from_table("task"):
        import_task_into_new_db(task, user_mapping)

    make_import("newtask", models.new_task.NewTask, "user_id", "New Tasks")
    make_import("taskhint", models.task_hint.TaskHint, None, "Task Hint")

    for user_solution in select_everythin_from_table("usersolution"):
        import_user_solution_into_new_db(user_solution, user_mapping)

    for task_statistic in select_everythin_from_table("taskstatistic"):
        import_task_statistics(task_statistic, user_mapping)

    make_import(
        "questionnaire", models.questionnaire.Questionnaire, None, "Questionnaire"
    )

    make_import(
        "questionnairequestion",
        models.questionnaire_question.QuestionnaireQuestion,
        None,
        "Questionnaire Question",
    )
    make_import(
        "questionnairequestionoption",
        models.questionnaire_question_option.QuestionnaireQuestionOption,
        None,
        "Questionnaire Question Option",
    )
    make_import(
        "questionnaireanswer",
        models.questionnaire_answer.QuestionnaireAnswer,
        "user_id",
        "Questionnaire Answer",
    )

    make_import(
        "taskquestionnaires",
        models.task_questionnaires.TaskQuestionnaires,
        None,
        "Task Questionnaires",
    )

    make_import("hintimage", models.hint_image.HintImage, None, "Hint Image")
