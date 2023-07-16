import json

from app.scheduler.schedulers import PeriodicTask
from app.scheduler.session import SessionManager
from app.scheduler.models import IntervalSchedule, PeriodicTask

beat_dburi = "sqlite:///app/scheduler/schedule.db"

session_manager = SessionManager()
session = session_manager.session_factory(beat_dburi)
session.close()


def remove_periodic_task(clearml_task_id: str, session=None):
    if not session:
        _, session_maker = session_manager.create_session(beat_dburi)
        session = session_maker()
    periodic_task = session.query(PeriodicTask).filter_by(name=clearml_task_id).first()
    if periodic_task is not None:
        session.delete(periodic_task)
        session.commit()


def create_periodic_task(
    peridodic_task_name: str,
    task_name: str,
    data: dict,
    interval: int = 5,
    session=None,
):
    if not session:
        _, session_maker = session_manager.create_session(beat_dburi)
        session = session_maker()
    schedule = (
        session.query(IntervalSchedule)
        .filter_by(every=interval, period=IntervalSchedule.SECONDS)
        .first()
    )
    if not schedule:
        schedule = IntervalSchedule(every=5, period=IntervalSchedule.SECONDS)
        session.add(schedule)
        session.commit()

    task = PeriodicTask(
        interval=schedule,
        name=peridodic_task_name,
        task=task_name,
        kwargs=json.dumps(data),
        queue="ai",
    )
    session.add(task)
    session.commit()

    return schedule
