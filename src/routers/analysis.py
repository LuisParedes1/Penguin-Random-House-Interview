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
def data_analysis(mean: bool = False,
                  median: bool = False,
                  max_value: bool = False,
                  include_uy: bool = False,
                  include_ar: bool = False,
                  include_cl: bool = False,
                  year: Optional[int] = None,
                  global_results: bool = False):
    """
    Data analysis based on specified metric and filters. Unless otherwise specified by the `global_results` flag, 
    the function returns data analysis grouped by country code.
    """

    logger.info("Starting data analysis")


    metrics_map: dict[str, bool] = {
        "mean": mean,
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
        logger.error(f"Filters {{year: {year}, country_codes: {country_codes}}} returned no data")
        raise HTTPException(status_code=404, detail="Filters returned no data")


    results: dict[str, float] = {}

    if global_results:
        results["global_results"] = filtered_data['value'].agg(metrics).to_dict()
        results["on_countries"] = country_codes
    else:
        results = filtered_data.groupby('country')['value'].agg(metrics).to_dict('index')  

    logger.info("Analysis successfully finished. Returning metrics")

    return JSONResponse(content=results, status_code=200)
