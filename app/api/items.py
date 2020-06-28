from http import HTTPStatus

from flask import jsonify, request, current_app, url_for

from app.api import api
from app.models.item import Item
from app.models.schemas.item import ItemSchema
from configuration import ENV_VNH_ITEMS_PER_PAGE


@api.route('/items/<str_or_int:id_or_name>')
def get_item(id_or_name):
    if isinstance(id_or_name, int):
        filter_ = {'id': id_or_name}
    else:
        filter_ = {'name': id_or_name}

    item = Item.query.filter_by(**filter_).first()

    if item is None:
        # Returning no content as 404s are considered errors and cause logging on the UI side
        return '', HTTPStatus.NO_CONTENT

    return ItemSchema().dump(item)


@api.route('/items/')
def get_items():
    page = request.args.get('page', 1, type=int)

    pagination = Item.query.order_by(Item.name.asc()).paginate(
        page, per_page=current_app.config[ENV_VNH_ITEMS_PER_PAGE],
        error_out=False)

    items = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_items', page=page-1)

    next_ = None
    if pagination.has_next:
        next_ = url_for('api.get_items', page=page+1)

    return jsonify({
        'items': [ItemSchema().dump(item) for item in items],
        'prev': prev,
        'next': next_,
        'count': pagination.total
    })
