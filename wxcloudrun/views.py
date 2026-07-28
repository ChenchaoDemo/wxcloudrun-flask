from datetime import datetime
from decimal import Decimal, InvalidOperation
from flask import jsonify, render_template, request
from sqlalchemy.exc import SQLAlchemyError

from wxcloudrun import app, db
from wxcloudrun.dao import (
    delete_counterbyid,
    delete_order,
    insert_counter,
    list_orders,
    query_counterbyid,
    query_order_by_id,
    query_order_by_no,
    save_order,
    update_counterbyid,
    update_order,
)
from wxcloudrun.model import Counters, Orders
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'wxcloudrun-flask',
        'api': ['/api/count', '/api/orders'],
    })


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


def parse_order_params(params, partial=False):
    required_fields = ('orderNo', 'customerName', 'productName', 'totalAmount')
    if not partial:
        missing = [field for field in required_fields if params.get(field) in (None, '')]
        if missing:
            raise ValueError('missing required fields: {}'.format(', '.join(missing)))

    values = {}
    field_map = {
        'orderNo': 'order_no',
        'customerName': 'customer_name',
        'customerPhone': 'customer_phone',
        'productName': 'product_name',
        'status': 'status',
        'address': 'address',
        'remark': 'remark',
    }
    for source, target in field_map.items():
        if source in params:
            values[target] = params[source]

    if 'quantity' in params:
        values['quantity'] = int(params['quantity'])
        if values['quantity'] <= 0:
            raise ValueError('quantity must be greater than 0')
    elif not partial:
        values['quantity'] = 1

    if 'totalAmount' in params:
        values['total_amount'] = Decimal(str(params['totalAmount']))
        if values['total_amount'] < 0:
            raise ValueError('totalAmount cannot be negative')

    return values


@app.route('/api/orders', methods=['POST'])
def create_order():
    params = request.get_json(silent=True) or {}
    try:
        values = parse_order_params(params)
        if query_order_by_no(values['order_no']) is not None:
            return make_err_response('orderNo already exists')
        order = save_order(Orders(**values))
        return make_succ_response(order.to_dict())
    except (ValueError, TypeError, InvalidOperation) as e:
        return make_err_response(str(e))
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_err_response(str(e))


@app.route('/api/orders', methods=['GET'])
def get_orders():
    return make_succ_response([order.to_dict() for order in list_orders()])


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = query_order_by_id(order_id)
    if order is None:
        return make_err_response('order not found')
    return make_succ_response(order.to_dict())


@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def edit_order(order_id):
    order = query_order_by_id(order_id)
    if order is None:
        return make_err_response('order not found')

    params = request.get_json(silent=True) or {}
    try:
        values = parse_order_params(params, partial=True)
        if 'order_no' in values:
            existing = query_order_by_no(values['order_no'])
            if existing is not None and existing.id != order_id:
                return make_err_response('orderNo already exists')
        for field, value in values.items():
            setattr(order, field, value)
        order.updated_at = datetime.now()
        update_order()
        return make_succ_response(order.to_dict())
    except (ValueError, TypeError, InvalidOperation) as e:
        return make_err_response(str(e))
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_err_response(str(e))


@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def remove_order(order_id):
    order = query_order_by_id(order_id)
    if order is None:
        return make_err_response('order not found')
    try:
        delete_order(order)
        return make_succ_empty_response()
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_err_response(str(e))
