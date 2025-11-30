#!/bin/bash

echo "Starting FastAPI backend..."
uvicorn src.service_api:app --host 0.0.0.0 --port 8000 &


sleep 15



echo " Starting Streamlit frontend..."
streamlit run src/app_streamlit.py --server.port 7860 --server.address 0.0.0.0