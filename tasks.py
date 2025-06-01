from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import MealServing, Meal, MealIngredient, MonthlyReport, Alert, AlertType
from app.db.session import SessionLocal
from celery_worker import celery_app
import math


@celery_app.task
def generate_monthly_report():
    db: Session = SessionLocal()

    now = datetime.utcnow()
    month = now.month
    year = now.year

    servings = db.query(MealServing).filter(
        MealServing.served_at.month == month,
        MealServing.served_at.year == year
    ).all()

    total_portions = sum([s.portions for s in servings])

    meals = db.query(Meal).all()
    total_possible = 0

    for meal in meals:
        meal_ingredients = db.query(MealIngredient).filter(MealIngredient.meal_id == meal.id).all()
        meal_min = float("inf")
        for item in meal_ingredients:
            if item.quantity == 0:
                continue
            stock = item.ingredient.quantity
            possible = math.floor(stock / item.quantity)
            if possible < meal_min:
                meal_min = possible
        total_possible += meal_min if meal_min != float("inf") else 0

    diff_percent = 0.0
    if total_possible > 0:
        diff_percent = 100 * abs(total_possible - total_portions) / total_possible

    report = MonthlyReport(
        month=month,
        year=year,
        total_portions_served=total_portions,
        total_portions_possible=total_possible,
        difference_percentage=diff_percent
    )
    db.add(report)
    db.commit()

    if diff_percent >= 15:
        alert = Alert(
            message=f"Discrepancy rate {diff_percent:.2f}% exceeds threshold!",
            alert_type=AlertType.usage_suspicious,
            related_report_id=report.id
        )
        db.add(alert)
        db.commit()

    db.close()