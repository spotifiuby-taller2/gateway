from asyncio import constants
from http.client import HTTPException
from fastapi import FastAPI, HTTPException
from services.ApiKeyService import ApiKeyService
from data.constants import ISDEVELOPMENT
from src.data.migrations import runMigrations


class App:
    def contructor():
        app = FastAPI()
        apiKeyService = ApiKeyService()
    
    async def syncDB():
        if(not ISDEVELOPMENT):
            await runMigrations()

    def defineEvents(self):
        self.apiKeyService.defineEvents(self)