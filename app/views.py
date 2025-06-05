from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import (
    Ingredient as IngredientModel,
    Meal as MealModel,
    Meal,
    MealIngredient,
    Ingredient,
    MealServing,
)
from app.core.security import get_current_user  # Ensure this dependency exists
from app.urls import notify_inventory_update
import asyncio

get_db = SessionLocal()

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ---------- GET ROUTES ----------

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/ingredients/", response_class=HTMLResponse)
def ingredients_view(request: Request, db: Session = Depends(get_db)):
    ingredients = db.query(IngredientModel).all()
    return templates.TemplateResponse("ingredients.html", {
        "request": request,
        "ingredients": ingredients
    })


@router.get("/serve-meal/", response_class=HTMLResponse)
def serve_meal_view(request: Request, db: Session = Depends(get_db)):
    meals = db.query(MealModel).all()
    return templates.TemplateResponse("serve_meal.html", {
        "request": request,
        "meals": meals
    })


@router.get("/charts/", response_class=HTMLResponse)
def charts_view(request: Request, db: Session = Depends(get_db)):
    ingredients = db.query(IngredientModel).all()
    labels = [i.name for i in ingredients]
    data = [i.quantity for i in ingredients]
    return templates.TemplateResponse("charts.html", {
        "request": request,
        "labels": labels,
        "data": data
    })

# ---------- POST ROUTE FOR SERVING MEALS ----------

@router.post("/serve-meal/", response_class=HTMLResponse)
def serve_meal_post(
    request: Request,
    meal_id: int = Form(...),
    portions: int = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        return templates.TemplateResponse("serve_meal.html", {
            "request": request,
            "error": "Meal not found.",
            "meals": db.query(Meal).all()
        })

    meal_ingredients = db.query(MealIngredient).filter(MealIngredient.meal_id == meal_id).all()

    # Check if ingredients are sufficient
    for item in meal_ingredients:
        ingredient = db.query(Ingredient).filter(Ingredient.id == item.ingredient_id).first()
        required = item.quantity * portions
        if ingredient.quantity < required:
            return templates.TemplateResponse("serve_meal.html", {
                "request": request,
                "error": f"Not enough {ingredient.name} in stock.",
                "meals": db.query(Meal).all()
            })

    # Deduct ingredients and notify via WebSocket
    for item in meal_ingredients:
        ingredient = db.query(Ingredient).filter(Ingredient.id == item.ingredient_id).first()
        ingredient.quantity -= item.quantity * portions
        db.add(ingredient)
        asyncio.create_task(notify_inventory_update(f'Inventory updated: {ingredient.name}'))

    # Log the meal serving
    new_serving = MealServing(
        meal_id=meal.id,
        portions=portions,
        served_by=current_user.id
    )
    db.add(new_serving)
    db.commit()

    return RedirectResponse(url="/serve-meal/", status_code=status.HTTP_302_FOUND)
