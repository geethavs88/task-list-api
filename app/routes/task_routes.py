from flask import Blueprint, request, Response, abort, make_response
from ..db import db
from ..models.task import Task
from .routes_utilities import validate_model, create_model, get_models_with_filters
from datetime import datetime
import os
import requests

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)
    # request_body = request.get_json()
   
    # try:
    #     new_task = Task.from_dict(request_body)
    # except KeyError as error:
    #     return {"details": "Invalid data"}, 400

    # db.session.add(new_task)
    # db.session.commit()

    
    # task_response = new_task.to_dict()
    # return task_response, 201

@bp.get("")
def get_all_tasks():

    return get_models_with_filters(Task, request.args)
    # query = db.select(Task)
    # title_param = request.args.get("title")
    # if title_param:
    #     query = query.where(Task.title == title_param)
    # description_param = request.args.get("description")
    # if description_param :
    #     query = query.where(Task.description.ilike(f"%{description_param}%"))


    # tasks = db.session.scalars(query)
    # result_list = []
    # for task in tasks:
    #     result_list.append(task.to_dict())

    # return result_list

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]

    task.description = request_body["description"]
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]
    else:
        task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# @bp.get("")
# def sort_by_title():
#     sort_param = request.args.get("sort")
#     query = db.select(Task)
#     if sort_param == "asc" :
#         query = query.order_by(Task.title.asc())
#     elif sort_param == "desc":
#         query = query.order_by(Task.title.desc())

#     tasks = db.session.scalars(query)
#     result_list = [task.to_dict() for task in tasks]
#     return result_list



@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    task.title="My Beautiful Task"
    db.session.commit()
    slack_url = "https://slack.com/api/chat.postMessage"
    slack_request_body = {
        "channel": "#task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    slack_headers  = {
        "Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}",
        "Content-Type": "application/json"
    }
    requests.post(slack_url, json = slack_request_body, headers = slack_headers)

    return Response(status=204, mimetype="application/json")



@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")

