from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
import os
from controllers import DataController, ProjectController
from models import ResponseSignals
import aiofiles
import logging

logger = logging.getLogger("uvicorn.error")
 
data_router = APIRouter( 
    prefix = "/api/v1/data",
    tags =["api_v1", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    # validate the uploaded file


    data_controller =DataController()
    isvalid, result_signal = data_controller.validate_uploaded_file(file= file)

    if not isvalid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                'signal': result_signal
            }
        )
    

    project_dir_path = ProjectController().get_project_path(project_id= project_id)
    file_path = data_controller.generate_unique_filename(orig_file_name= file.filename,
                                                         project_id= project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
        return JSONResponse(
                content = {
                    'signal': ResponseSignals.FILE_UPLOAD_SUCCESS.value
                }
            )
        
        
    except Exception as e:
        logger.error(f'error while uploading file: {e}')

        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                'signal': ResponseSignals.FILE_UPLOAD_FAILED.value
            }
        )



        


   

    

