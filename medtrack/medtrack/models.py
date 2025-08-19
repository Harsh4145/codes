from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, nullable=False, index=True)
	name = db.Column(db.String(120), nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	role = db.Column(db.String(32), nullable=False, default="admin")
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	def set_password(self, password: str) -> None:
		self.password_hash = generate_password_hash(password)

	def check_password(self, password: str) -> bool:
		return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
	return User.query.get(int(user_id))


class Medicine(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False, index=True)
	manufacturer = db.Column(db.String(200), nullable=True)
	batch_number = db.Column(db.String(100), nullable=True)
	expiry_date = db.Column(db.Date, nullable=False)

	quantity = db.Column(db.Integer, nullable=False, default=0)
	low_stock_threshold = db.Column(db.Integer, nullable=False, default=10)

	unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)

	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	updated_at = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
	)

	transactions = db.relationship(
		"Transaction", back_populates="medicine", cascade="all, delete-orphan"
	)

	@property
	def is_low_stock(self) -> bool:
		return self.quantity <= self.low_stock_threshold

	@property
	def is_expiring_soon(self) -> bool:
		if not self.expiry_date:
			return False
		days_until_expiry = (self.expiry_date - date.today()).days
		return days_until_expiry <= 30


class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	medicine_id = db.Column(db.Integer, db.ForeignKey("medicine.id"), nullable=False)
	type = db.Column(db.String(16), nullable=False)  # PURCHASE or DISPENSE
	quantity = db.Column(db.Integer, nullable=False)
	notes = db.Column(db.String(255), nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	medicine = db.relationship("Medicine", back_populates="transactions")