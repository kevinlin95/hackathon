from flask import Blueprint, render_template

resource_bp = Blueprint('resource', __name__)


@resource_bp.route('/resources', methods=["GET"])
def resources():
    return render_template('resource.html')
