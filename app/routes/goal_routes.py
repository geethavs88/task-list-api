from flask import Blueprint, request, Response
from ..db import db
from ..models.goal import Goal
from ..models.task import Task
from .routes_utilities import validate_model, create_model, get_models_with_filters
from datetime import datetime

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def send_list_of_task_to_goal_id(goal_id):
    goal = validate_model(Goal,goal_id)
    query = db.select(Task).where(Task.goal_id == goal.id)
    existing_tasks = db.session.scalars(query).all()
    for each_task in existing_tasks:
        each_task.goal_id = None
    request_body = request.get_json()
    task_ids= request_body.get("task_ids", [])
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id =goal.id
    db.session.commit()
    response_body = {
        "id" : goal.id,
        "task_ids" : [task.id for task in goal.tasks]
    }
    return response_body, 200

@bp.get("/<id>/tasks")
def get_all_tasks_with_one_goal(id):
    goal = validate_model(Goal, id)
    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]
    return goal_dict