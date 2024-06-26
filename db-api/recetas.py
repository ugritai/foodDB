import os
from typing import Optional, List, Union

from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
from bson import ObjectId

from models import RecipeModel, RecipeCollection, AbuelaModel, AbuelaCollection, ShortRecipeCollection, ShortRecipeModel, MealRECRecipeModel, MealRECRecipeCollection
from bd import abuela_collection, recipe1m_collection, foodcom_collection, mealrec_collection, recipeQA_collection

from fastapi import Depends
from auth import get_current_user, UserModel

import json

router = APIRouter()

@router.get(
        "/mealrec",
        response_description="Listar todas las recetas de MealRec",
        response_model=MealRECRecipeCollection,
        response_model_by_alias=False
)
async def listar_recetas_mealrec():
    """
    Listar todas las recetas de MealRec.

    La respuesta está limitada a 1000 resultados.
    """
    recetas = await mealrec_collection.find().to_list(1000)
    return MealRECRecipeCollection(recetas=recetas)


@router.get(
    "/mealrec/{receta_id}",
    response_description="Obtener una receta por ID",
    response_model=MealRECRecipeModel,
    response_model_by_alias=False
)
async def obtener_receta_por_id(receta_id: str):
    receta = await mealrec_collection.find_one({"_id": ObjectId(receta_id)})
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    if 'interactions' in receta and receta['num_interactions'] > 10:
        receta['interactions'] = receta['interactions'][:10]

    return receta



@router.get(
    "/all",
    response_description="Listar todas las recetas",
    response_model=ShortRecipeCollection,
    response_model_by_alias=False,
) 
async def listar_recetas():
    """
    Listar todas las recetas.
    """

    abuela_recetas = await abuela_collection.find().to_list(1)
    recipe1m_recetas = await recipe1m_collection.find().to_list(1)
    foodcom_recetas = await foodcom_collection.find().to_list(1)
    mealrec_recetas = await mealrec_collection.find().to_list(1)
    recipeQA_recetas = await recipeQA_collection.find().to_list(1)
    return (ShortRecipeCollection(recetas=foodcom_recetas + abuela_recetas + mealrec_recetas + recipeQA_recetas + recipe1m_recetas))

@router.get(
    "/{titulo}",
    response_description="Buscar recetas por su título",
    response_model=RecipeCollection,
    response_model_by_alias=False,
)
async def buscar_recetas_por_titulo(titulo: str):
    """
    Buscar una receta por su título.    
    """
    
    recetas = []
    async for recipe in abuela_collection.find():
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    async for recipe in recipe1m_collection.find():
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    async for recipe in foodcom_collection.find():
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    async for recipe in mealrec_collection.find():
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    async for recipe in recipeQA_collection.find():
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    print("Recetas encontradas: ", len(recetas))
    if len(recetas) > 0:
        return RecipeCollection(recetas=recetas)

    raise HTTPException(status_code=404, detail=f"No se encontraron recetas con el nombre {titulo}")

@router.get(
    "/idioma/{idioma_ISO}/titulo/{titulo}",
    response_description="Buscar recetas por ingrediente",
    response_model=RecipeCollection,
    response_model_by_alias=False,
)
async def buscar_recetas_por_titulo_e_idioma(idioma_ISO: str, titulo: str):

    recetas = []
    async for recipe in abuela_collection.find({"language_ISO": idioma_ISO.upper()}):
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    async for recipe in recipe1m_collection.find({"language_ISO": idioma_ISO.upper()}):
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    async for recipe in foodcom_collection.find({"language_ISO": idioma_ISO.upper()}):
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    async for recipe in mealrec_collection.find({"language_ISO": idioma_ISO.upper()}):
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    async for recipe in recipeQA_collection.find({"language_ISO": idioma_ISO.upper()}):
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    print("Recetas encontradas: ", len(recetas))
    if len(recetas) > 0:
        return RecipeCollection(recetas=recetas)

    raise HTTPException(status_code=404, detail=f"No se encontraron recetas con el nombre {titulo} en el idioma {idioma_ISO}")



    
@router.get(
    "/abuela/",
    response_description="Listar todas las recetas de la abuela",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def listar_abuela():
    """
    Listar las recetas de la abuela.
    
    La respuesta está limitada a 1000 resultados.
    """
    return AbuelaCollection(recetas=await abuela_collection.find().to_list(1000))


@router.get(
    "/abuela/{id}",
    response_description="Buscar una receta de la abuela por ID",
    response_model=AbuelaModel,
    response_model_by_alias=False,
)
async def buscar_Abuela_por_id(id: str):
    """
    Buscar una receta de la abuela por su ID.
    """
    receta = await abuela_collection.find_one({"_id": ObjectId(id)})
    if receta:
        return receta

    raise HTTPException(status_code=404, detail=f"No se encontró la receta de la abuela con el ID {id}")

@router.get(
    "/abuela/titulo/{titulo}",
    response_description="Buscar una receta de la abuela",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def buscar_Abuela_por_titulo(titulo: str):
    """
    Buscar una receta de la abuela por su título.    
    """
    
    recetas = []
    async for recipe in abuela_collection.find():
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    print("Recetas encontradas: ", len(recetas))
    if len(recetas) > 0:
        return AbuelaCollection(recetas=recetas)

    raise HTTPException(status_code=404, detail=f"No se encontraron recetas con el nombre {titulo}")


@router.get(
    "/abuela/ingrediente/{ingrediente}",
    response_description="Buscar recetas de la abuela por ingrediente",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def buscar_Abuela_por_ingrediente(ingrediente: str):
    """
    Buscar recetas de la abuela por ingrediente.
    """
    recetas_encontradas = []

    #async for receta in abuela_collection.find({"ingredients": {"$regex": ingrediente, "$options": "i"}}):
    #    recetas_encontradas.append(receta)
    
    async for receta in abuela_collection.find({"ingredients.ingredient": {"$regex": ingrediente, "$options": "i"}}).limit(100):
        recetas_encontradas.append(receta)

    if recetas_encontradas:
        return AbuelaCollection(recetas=recetas_encontradas)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron recetas que contengan el ingrediente {ingrediente}")
    
    
    
@router.get(
    "/abuela/pais/{pais_ISO}",
    response_description="Buscar recetas de la abuela por país",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
    )
async def buscar_Abuela_por_pais(pais_ISO: str):
    """
    Buscar recetas de la abuela por país.
    """
    recetas_encontradas = []
    
    pais_ISO = pais_ISO.upper() # Convertir a mayúsculas para asegurar la búsqueda

    #async for receta in abuela_collection.find({"origin_ISO": pais}):
    #    recetas_encontradas.append(receta)

    async for receta in abuela_collection.find({"origin_ISO": pais_ISO}):
        recetas_encontradas.append(receta)

    if recetas_encontradas:
        return AbuelaCollection(recetas=recetas_encontradas)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron recetas originadas en el país {pais_ISO}")
    

@router.get(
    "/abuela/pais/{pais_ISO}/titulo/{titulo}",
    response_description="Buscar recetas de la abuela por país y título",
    response_model=AbuelaCollection,
    response_model_by_alias=False,

)
async def buscar_Abuela_por_pais_y_titulo(pais_ISO: str, titulo: str):
    """
    Buscar recetas de la abuela por país y título.
    """
    recetas_encontradas = []

    # Convertir el código ISO a mayúsculas
    pais_ISO = pais_ISO.upper()

    async for receta in abuela_collection.find({"origin_ISO": pais_ISO, "title": {"$regex": titulo, "$options": "i"}}).limit(100):
        recetas_encontradas.append(receta)

    if recetas_encontradas:
        return AbuelaCollection(recetas=recetas_encontradas)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron recetas originadas en el país {pais_ISO} con el título {titulo}")
    
    
@router.get(
    "/abuela/pais/{pais_ISO}/ingrediente/{ingrediente}",
    response_description="Buscar recetas de la abuela por país e ingrediente",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def buscar_Abuela_por_pais_e_ingrediente(pais_ISO: str, ingrediente: str):
    """
    Buscar recetas de la abuela por país e ingrediente.
    """
    recetas_encontradas = []

    # Convertir el código ISO a mayúsculas
    pais_ISO = pais_ISO.upper()

    async for receta in abuela_collection.find({"origin_ISO": pais_ISO, "ingredients.ingredient": {"$regex": ingrediente, "$options": "i"}}).limit(100):
        recetas_encontradas.append(receta)

    if recetas_encontradas:
        return AbuelaCollection(recetas=recetas_encontradas)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron recetas originadas en el país {pais_ISO} que contengan el ingrediente {ingrediente}")