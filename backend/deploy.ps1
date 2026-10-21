param(
  [Parameter(Mandatory=$true)][string]$ProjectId,
  [string]$Region = "us-central1",
  [string]$Service = "transformsql-vertex"
)

gcloud config set project $ProjectId
gcloud services enable run.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com
gcloud run deploy $Service --source . --region $Region --no-allow-unauthenticated --set-env-vars "GOOGLE_CLOUD_PROJECT=$ProjectId,GOOGLE_CLOUD_LOCATION=$Region,GOOGLE_GENAI_USE_VERTEXAI=True,VERTEX_MODEL=gemini-2.5-flash"
