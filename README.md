# MongoDB FastAPI example

Small FastAPI document service backed by MongoDB. Read [SECURITY.md](SECURITY.md)
before configuring a database or applying the manifests in `infrastructure/k8s`.
The duplicate RAR source archive was removed because it retained embedded
credentials. Git remains the source of versioned code.

Install `requirements.txt`, export your own database settings, then start from
the repository root: `python -m uvicorn services.data_loader.app:app`.
Run offline configuration tests: `python -m unittest discover -s tests -v`.
Complete API behavior and deployment verification are still planned.
