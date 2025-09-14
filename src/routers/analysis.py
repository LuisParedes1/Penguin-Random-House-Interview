# analysis.py
"""
Router for the data analysis
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from enum import Enum

import logging
# from src.app import DATA

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


router = APIRouter(
    tags=["analysis"],
)

@router.get("/data_analysis", summary="Return data analysis based on specified metric and filters")
def data_analysis(average: Optional[bool] = None,
                  median: Optional[bool] = None,
                  max_values: Optional[bool] = None,
                  include_uy: Optional[bool] = None,
                  include_ar: Optional[bool] = None,
                  include_cl: Optional[bool] = None,
                  year: Optional[int] = None,
                  global_results: bool = False):
    """
    Data analysis based on specified metric and filters. Unless otherwise specified by the `global_results` flag, 
    the function returns data analysis grouped by country code.
    """

    if not average and not median and not max_values:
        raise HTTPException(status_code=400, detail="Specify at least one metric.")
    
    country_map: dict[str, bool] = {
        "uy": include_uy,
        "ar": include_ar,
        "cl": include_cl,
    }
    country_codes: list[str] = [code for code, included in country_map.items() if included]

    if not country_codes:
        raise HTTPException(status_code=400, detail="At least one country must be included.")
    

    result: dict[str, float] = {"status": 200}

    # if average:
    #     result['average'] = get_metric
    
    return JSONResponse(content=result, status_code=200)
