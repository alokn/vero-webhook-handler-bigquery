#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error: $1" >&2
    exit 1
}

# Set your variables
PROJECT_ID="<YOUR_PROJECT_ID>"
FUNCTION_NAME="<YOUR_FUNCTION_NAME>"
REGION="<YOUR_REGION>"
DATASET="<YOUR_DATASET>"
TABLE="<YOUR_TABLE>"
SERVICE_ACCOUNT_NAME="<YOUR_SERVICE_ACCOUNT_NAME>"
SERVICE_ACCOUNT_EMAIL="<YOUR_SERVICE_ACCOUNT_EMAIL>"
RUNTIME="python310"

# Set values for memory and CPU
MEMORY="128Mi"
CPU="0.1"
MAX_INSTANCES="100"

# Deploy the function (Gen 2)
echo "Deploying Cloud Function..."
gcloud functions deploy $FUNCTION_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --runtime=$RUNTIME \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point=$FUNCTION_NAME \
    --source=api \
    --set-env-vars=PROJECT_ID=$PROJECT_ID,DATASET=$DATASET,TABLE=$TABLE \
    --gen2 \
    --memory=$MEMORY \
    --cpu=$CPU \
    --max-instances=$MAX_INSTANCES \
    --service-account=$SERVICE_ACCOUNT_EMAIL || handle_error "Failed to deploy Cloud Function"


echo "Cloud Function (Gen 2) deployed successfully."