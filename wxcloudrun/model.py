from datetime import datetime
from decimal import Decimal

from wxcloudrun import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


class Orders(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column('orderNo', db.String(64), nullable=False, unique=True)
    customer_name = db.Column('customerName', db.String(100), nullable=False)
    customer_phone = db.Column('customerPhone', db.String(32))
    product_name = db.Column('productName', db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_amount = db.Column('totalAmount', db.Numeric(12, 2), nullable=False, default=Decimal('0.00'))
    status = db.Column(db.String(32), nullable=False, default='pending')
    address = db.Column(db.String(500))
    remark = db.Column(db.String(500))
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now)
    updated_at = db.Column(
        'updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def to_dict(self):
        return {
            'id': self.id,
            'orderNo': self.order_no,
            'customerName': self.customer_name,
            'customerPhone': self.customer_phone,
            'productName': self.product_name,
            'quantity': self.quantity,
            'totalAmount': str(self.total_amount),
            'status': self.status,
            'address': self.address,
            'remark': self.remark,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
