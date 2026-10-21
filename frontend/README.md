# TransformSQL frontend

Static browser UI. It supports login, workbook upload, sheet discovery, SQL preview, direct/derived filtering, row approval, BigQuery execution, private target comparison, result/deviation display, copy, and downloads.

Serve this folder with any static server. Set `window.TRANSFORMSQL_API_BASE` when the backend is hosted separately.

## Local startup

Start the backend first on port `8081`, then serve this directory:

```powershell
python -m http.server 8080
```

Open `http://localhost:8080` and use `admin` / `transform123` for the demo login.

The frontend calls:

- `POST /api/generate` to scan the workbook and create row-level SQL.
- `POST /api/run-bigquery` to execute the selected generated query.
- `POST /api/compare-bigquery` to compare the generated output with the target table column.

If the backend is unavailable, the browser uses its local XLSX parser for generation. BigQuery execution and comparison still require the backend and configured Google credentials.
