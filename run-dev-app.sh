#!/bin/bash

docker build -t streamlit-supabase ./Dockerfile.streamlit .
docker run -p 8501:8501 streamlit-supabase