import os
from typing import Optional, List, Union
from datetime import datetime

from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
from bson import ObjectId

from models import DietModel, DietCollection, DietCompleteModel, DietCompleteCollection
from bd import dietas_collection, users_collection, get_collection, mealrec_collection

from fastapi import Depends
from auth import get_current_user, UserModel

import json

router = APIRouter()

async def completarDieta(dieta):
    appetizer = await mealrec_collection.find_one({"_id": dieta["appetizerID"]})
    main_dish = await mealrec_collection.find_one({"_id": dieta["main_dishID"]})
    dessert = await mealrec_collection.find_one({"_id": dieta["dessertID"]})

    dieta["appetizer"] = appetizer
    dieta["main_dish"] = main_dish
    dieta["dessert"] = dessert

    return dieta

@router.get("/", response_model=DietCompleteCollection)
async def get_dietas(current_user: UserModel = Depends(get_current_user)):

    dietas = await dietas_collection.find({"created_by": current_user.email}).to_list(1000)

    for dieta in dietas:
        dieta = await completarDieta(dieta)

    return DietCompleteCollection(diets=dietas)


@router.get("/{dieta_id}", response_model=DietCompleteModel)
async def get_dieta(dieta_id: str):
    dieta = await dietas_collection.find_one({"_id": ObjectId(dieta_id)})
    if dieta:

        dieta = await completarDieta(dieta)

        return DietCompleteModel(**dieta)
    
    raise HTTPException(status_code=404, detail="Dieta no encontrada")


@router.post("/", response_model=DietModel)
async def create_dieta(dieta: DietModel, current_user: UserModel = Depends(get_current_user)):
    dieta_dict = dieta.model_dump()
    if dieta_dict["appetizerID"]:
        dieta_dict["appetizerID"] = ObjectId(dieta_dict["appetizerID"])

    if dieta_dict["main_dishID"]:
        dieta_dict["main_dishID"] = ObjectId(dieta_dict["main_dishID"])

    if dieta_dict["dessertID"]:
        dieta_dict["dessertID"] = ObjectId(dieta_dict["dessertID"])

    dieta_dict["created_by"] = current_user.email
    dieta_dict["created_at"] = datetime.now()
    dieta_dict["dietary_preferences"] = []
    dieta_id = await dietas_collection.insert_one(dieta_dict)
    
    # Agregar el ID de la dieta al array de dietas del usuario
    await users_collection.update_one(
        {"email": current_user.email},
        {"$push": {"diets": dieta_id.inserted_id}}
    )
    
    dieta = await dietas_collection.find_one({"_id": dieta_id.inserted_id})
    return DietModel(**dieta)

@router.delete("/{dieta_id}", response_model=DietModel)
async def delete_dieta(dieta_id: str, current_user: UserModel = Depends(get_current_user)):
    dieta = await dietas_collection.find_one({"_id": ObjectId(dieta_id)})
    
    if not dieta:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")
    
    # Verificar si el usuario actual es el creador de la dieta
    if dieta["created_by"] != current_user.email:
        raise HTTPException(status_code=403, detail="No tiene permiso para eliminar esta dieta")
    
    # Eliminar la dieta de la colección de dietas
    delete_result = await dietas_collection.delete_one({"_id": ObjectId(dieta_id)})
    
    if delete_result.deleted_count == 1:
        # Encontrar al usuario que creó la dieta
        user = await users_collection.find_one({"email": current_user.email})
        if user:
            current_user_id = user["_id"]
            # Eliminar el ID de la dieta del array de dietas del usuario
            await users_collection.update_one(
                {"_id": current_user_id},
                {"$pull": {"diets": ObjectId(dieta_id)}}
            )
        return DietModel(**dieta)
    else:
        raise HTTPException(status_code=500, detail="No se pudo eliminar la dieta")
