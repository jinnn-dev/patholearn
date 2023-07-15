from app.scheduler.schedulers import PeriodicTask


def remove_periodic_task(clearml_task_id: str, session):
    periodic_task = session.query(PeriodicTask).filter_by(name=clearml_task_id).first()
    if periodic_task is not None:
        session.delete(periodic_task)
        session.commit()
