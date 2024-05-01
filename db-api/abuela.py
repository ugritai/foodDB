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

from models import AbuelaModel, AbuelaCollection
from bd import abuela_collection

router = APIRouter() # Enrutador para las recetas de la abuela


    
@router.get(
    "/",
    response_description="Listar todas las recetas de la abuela",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def list_abuela():
    """
    Listar las recetas de la abuela.
    
    La respuesta está limitada a 100 resultados.
    """
    return AbuelaCollection(abuela=await abuela_collection.find().to_list(100))

@router.get(
    "/titulo/{titulo}",
    response_description="Buscar una receta de la abuela",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def search_abuela_by_title(titulo: str):
    """
    Buscar una receta de la abuela por su título.    
    """
    
    recetas = []
    recetas = []
    async for recipe in abuela_collection.find():
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    print("Recetas encontradas: ", len(recetas))
    if len(recetas) > 0:
        return AbuelaCollection(abuela=recetas)

    raise HTTPException(status_code=404, detail=f"No se encontraron recetas con el nombre {titulo}")


@router.get(
    "/ingrediente/{ingrediente}",
    response_description="Buscar recetas de la abuela por ingrediente",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def search_abuela_by_ingredient(ingrediente: str):
    """
    Buscar recetas de la abuela por ingrediente.
    """
    recetas_encontradas = []

    #async for receta in abuela_collection.find({"ingredients": {"$regex": ingrediente, "$options": "i"}}):
    #    recetas_encontradas.append(receta)
    
    async for receta in abuela_collection.find({"ingredients": {"$regex": ingrediente, "$options": "i"}}).limit(100):
        recetas_encontradas.append(receta)

    if recetas_encontradas:
        return AbuelaCollection(abuela=recetas_encontradas)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron recetas que contengan el ingrediente {ingrediente}")
    
    
    
@router.get(
    "/pais/{pais_ISO}",
    response_description="Buscar recetas de la abuela por país",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
    )
async def search_abuela_by_country(pais_ISO: str):
    """
    Buscar recetas de la abuela por país.
    """
    recetas_encontradas = []
    
    pais_ISO = pais_ISO.upper() # Convertir a mayúsculas para asegurar la búsqueda

    #async for receta in abuela_collection.find({"origin_ISO": pais}):
    #    recetas_encontradas.append(receta)

    async for receta in abuela_collection.find({"origin_ISO": pais_ISO}).limit(100):
        recetas_encontradas.append(receta)

    if recetas_encontradas:
        return AbuelaCollection(abuela=recetas_encontradas)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron recetas originadas en el país {pais_ISO}")
    

@router.get(
    "/pais/{pais_ISO}/titulo/{titulo}",
    response_description="Buscar recetas de la abuela por país y título",
    response_model=AbuelaCollection,
    response_model_by_alias=False,

)
async def search_abuela_by_country_and_title(pais_ISO: str, titulo: str):
    """
    Buscar recetas de la abuela por país y título.
    """
    recetas_encontradas = []

    # Convertir el código ISO a mayúsculas
    pais_ISO = pais_ISO.upper()

    async for receta in abuela_collection.find({"origin_ISO": pais_ISO, "title": {"$regex": titulo, "$options": "i"}}).limit(100):
        recetas_encontradas.append(receta)

    if recetas_encontradas:
        return AbuelaCollection(abuela=recetas_encontradas)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron recetas originadas en el país {pais_ISO} con el título {titulo}")
    
    
@router.get(
    "/pais/{pais_ISO}/ingrediente/{ingrediente}",
    response_description="Buscar recetas de la abuela por país e ingrediente",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def search_abuela_by_country_and_ingredient(pais_ISO: str, ingrediente: str):
    """
    Buscar recetas de la abuela por país e ingrediente.
    """
    recetas_encontradas = []

    # Convertir el código ISO a mayúsculas
    pais_ISO = pais_ISO.upper()

    async for receta in abuela_collection.find({"origin_ISO": pais_ISO, "ingredients": {"$regex": ingrediente, "$options": "i"}}).limit(100):
        recetas_encontradas.append(receta)

    if recetas_encontradas:
        return AbuelaCollection(abuela=recetas_encontradas)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron recetas originadas en el país {pais_ISO} que contengan el ingrediente {ingrediente}")