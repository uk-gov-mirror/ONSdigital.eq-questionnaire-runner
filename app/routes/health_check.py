import json

from flask import current_app, Blueprint
from newrelic import agent

health_check_blueprint = Blueprint(name="health_check", import_name=__name__)


@health_check_blueprint.route("/status", methods=["GET"])
def health_check():
    if current_app.config.get("EQ_NEW_RELIC_ENABLED"):
        agent.ignore_transaction()

    data = {"status": "OK", "version": current_app.config["EQ_APPLICATION_VERSION"]}
    return json.dumps(data)

