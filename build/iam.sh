PROJECT_ID=private-project-schimmerd
PROJECT_NUMBER=64173991942

# Granting permissions:
MEMBER=serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=${MEMBER} \
    --role=roles/run.admin
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=${MEMBER} \
    --role=roles/storage.admin
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=${MEMBER} \
    --role=roles/datastore.owner
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=${MEMBER} \
    --role=roles/pubsub.admin
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=${MEMBER} \
    --role=roles/iam.serviceAccountUser