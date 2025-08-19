from __future__ import annotations

from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from .extensions import db
from .forms import MedicineForm, TransactionForm
from .models import Medicine, Transaction


inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/")
@login_required
def dashboard():
	medicines = Medicine.query.order_by(Medicine.name.asc()).all()
	low_stock = [m for m in medicines if m.is_low_stock]
	expiring = [m for m in medicines if m.is_expiring_soon]
	return render_template(
		"dashboard.html",
		medicines=medicines,
		low_stock=low_stock,
		expiring=expiring,
	)


@inventory_bp.route("/medicines/new", methods=["GET", "POST"])
@login_required
def create_medicine():
	form = MedicineForm()
	if form.validate_on_submit():
		medicine = Medicine(
			name=form.name.data,
			manufacturer=form.manufacturer.data,
			batch_number=form.batch_number.data,
			expiry_date=form.expiry_date.data,
			quantity=form.quantity.data,
			low_stock_threshold=form.low_stock_threshold.data,
			unit_price=form.unit_price.data,
		)
		db.session.add(medicine)
		db.session.commit()
		flash("Medicine created", "success")
		return redirect(url_for("inventory.dashboard"))
	return render_template("medicines/form.html", form=form, title="Add Medicine")


@inventory_bp.route("/medicines/<int:medicine_id>/edit", methods=["GET", "POST"])
@login_required
def edit_medicine(medicine_id: int):
	medicine = Medicine.query.get_or_404(medicine_id)
	form = MedicineForm(obj=medicine)
	if form.validate_on_submit():
		form.populate_obj(medicine)
		db.session.commit()
		flash("Medicine updated", "success")
		return redirect(url_for("inventory.dashboard"))
	return render_template("medicines/form.html", form=form, title="Edit Medicine")


@inventory_bp.route("/medicines/<int:medicine_id>/delete", methods=["POST"])
@login_required
def delete_medicine(medicine_id: int):
	medicine = Medicine.query.get_or_404(medicine_id)
	db.session.delete(medicine)
	db.session.commit()
	flash("Medicine deleted", "success")
	return redirect(url_for("inventory.dashboard"))


@inventory_bp.route("/medicines/<int:medicine_id>/tx", methods=["GET", "POST"])
@login_required
def record_transaction(medicine_id: int):
	medicine = Medicine.query.get_or_404(medicine_id)
	form = TransactionForm()
	if form.validate_on_submit():
		quantity_change = form.quantity.data if form.type.data == "PURCHASE" else -form.quantity.data
		new_quantity = medicine.quantity + quantity_change
		if new_quantity < 0:
			flash("Insufficient stock to dispense", "danger")
			return render_template("medicines/transaction.html", form=form, medicine=medicine)
		medicine.quantity = new_quantity
		tx = Transaction(medicine=medicine, type=form.type.data, quantity=form.quantity.data, notes=form.notes.data)
		db.session.add(tx)
		db.session.commit()
		flash("Transaction recorded", "success")
		return redirect(url_for("inventory.dashboard"))
	return render_template("medicines/transaction.html", form=form, medicine=medicine)