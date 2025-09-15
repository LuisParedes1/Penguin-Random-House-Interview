# analysis.py
"""
Router for the data analysis
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from enum import Enum
from pandas import DataFrame
import logging
from src.data import DATASET

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


router = APIRouter(
    tags=["analysis"],
)


def apply_filters(data: DataFrame, 
                  country_codes: list[str],
                  year: Optional[int] 
) -> DataFrame:
    if year:
        data = data[data["fecha"].dt.year == year]
    
    return data[data["country"].map(lambda x: x.upper() in country_codes)]


@router.get("/data_analysis", summary="Return data analysis based on specified metric and filters")
def data_analysis(average: Optional[bool] = None,
                  median: Optional[bool] = None,
                  max_value: Optional[bool] = None,
                  include_uy: Optional[bool] = None,
                  include_ar: Optional[bool] = None,
                  include_cl: Optional[bool] = None,
                  year: Optional[int] = None,
                  global_results: bool = False):
    """
    Data analysis based on specified metric and filters. Unless otherwise specified by the `global_results` flag, 
    the function returns data analysis grouped by country code.
    """

    logger.info("Starting data analysis")


    metrics_map: dict[str, bool] = {
        "mean": average,
        "median": median,
        "max": max_value
    }
    metrics: list[str] = [metric for metric, included in metrics_map.items() if included]

    if not metrics:
        logger.error("No metric specified")
        raise HTTPException(status_code=400, detail="Specify at least one metric.")


    country_map: dict[str, bool] = {
        "UY": include_uy,
        "AR": include_ar,
        "CL": include_cl,
    }
    country_codes: list[str] = [code for code, included in country_map.items() if included]

    if not country_codes:
        logger.error("No country code specified")
        raise HTTPException(status_code=400, detail="At least one country must be included.")


    filtered_data: DataFrame = apply_filters(DATASET, country_codes, year)

    if filtered_data.empty:
        logger.error("Empty filters")
        # TODO: Make sure status code is appropiate
        raise HTTPException(status_code=500, detail="Filters returned no data")


    results: dict[str, float] = {}

    if global_results:
        results["global_results"] = filtered_data['value'].agg(metrics).to_dict()
    else:
        results = filtered_data.groupby('country')['value'].agg(metrics).to_dict('index')  

    logger.info("Analysis successfully finished. Returning metrics")

    return JSONResponse(content=results, status_code=200)
