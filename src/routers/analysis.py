# analysis.py
"""
Router for the data analysis
"""
from fastapi import APIRouter

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


router = APIRouter(
    tags=["analysis"],
)

# GET ENDPOINT
@router.get("/test", summary="Test Endpoint")
def test_endpoint():
    """
    Test Endpoint
    """
    return {"status": 200}
