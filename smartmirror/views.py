from flask import Blueprint, request, jsonify
from plugins import njt

blueprint = Blueprint('smartmirror', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET'])
def smartmirror():
	return jsonify({"hello": "World"})


@blueprint.route('/trains', methods=['GET'])
def trains():
	data = njt.trains()
	test = data.schedule()
	return jsonify(test)