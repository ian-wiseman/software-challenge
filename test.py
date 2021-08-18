from fastapi import FastAPI
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_get_genes_by_name(pattern: str, db: Session = Depends(get_db)):
    response = client.get("genesets/search/Great")
    assert response.status_code == 200
    assert response.json() == {"name": "Great Genes"}
