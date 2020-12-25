### The Cookbook 
Service for getting information about user profile and recipes, which are currently saved

## Deploy
gcloud builds submit --tag eu.gcr.io/v135-5247-playground-schimmer/the-cookbook
gcloud beta run deploy the-cookbook --image eu.gcr.io/v135-5247-playground-schimmer/the-cookbook --platform managed --region europe-west1 --concurrency 10 --allow-unauthenticated --memory 2Gi
         
### Swagger docu coming soon

# Todo
- Rollback mechanism