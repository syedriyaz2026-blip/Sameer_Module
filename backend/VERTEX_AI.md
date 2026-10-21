# Vertex AI deployment

This module is designed as a portable, deterministic SQL engine. It can run in Vertex AI Workbench, a Vertex AI custom job, Cloud Run, or another Python service without a frontend dependency. It exposes the generated mapping result through `POST /api/generate` and also provides the Python functions `scan_workbook`, `generate_queries`, and `build_result`.

## Local run

```powershell
python -m pip install -r requirements.txt
python transformsql_engine.py --serve --port 8080
```

## Deploy

```powershell
.\deploy.ps1 -ProjectId YOUR_PROJECT_ID -Region us-central1
```

The deployment uses Cloud Run's service identity and does not put a service-account key in the repository. Grant the runtime service account permission to call Vertex AI, normally `roles/aiplatform.user`.

## Vertex AI rule compilation

If you later add Gemini-assisted rule interpretation in a Vertex AI service, keep the deterministic engine as the source of truth and validate model output before applying it. Do not let free-form model text directly execute as SQL.

Google's current Gen AI SDK uses `GOOGLE_GENAI_USE_VERTEXAI=True`, `GOOGLE_CLOUD_PROJECT`, and `GOOGLE_CLOUD_LOCATION` for Vertex AI, and Cloud Run supports deploying Python source with `gcloud run deploy --source`. See the official Vertex AI and Cloud Run documentation for IAM and billing requirements.
