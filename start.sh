#!/bin/sh

python -m uvicorn main:app --host 0.0.0.0 --port $PORT --workers=4
