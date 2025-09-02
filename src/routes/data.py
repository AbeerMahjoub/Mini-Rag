from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
import os
from controllers import DataController, ProjectController, ProcessController
from models import ResponseSignals
import aiofiles
import logging
from .schemes.data import ProcessRequest

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
    file_path, file_id = data_controller.generate_unique_filepath(orig_file_name= file.filename,
                                                         project_id= project_id)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
        return JSONResponse(
                content = {
                    'signal': ResponseSignals.FILE_UPLOAD_SUCCESS.value,
                    'file_id': file_id
                }
            )
        
        
    except Exception as e:
        logger.error(f'error while uploading file: {e}')

        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                'signal': ResponseSignals.FILE_UPLOAD_FAILED.value,
                
            }
        )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    process_controller = ProcessController(project_id= project_id)

    file_content = process_controller.get_file_content(file_id= file_id)
    file_chunks = process_controller.process_file_content(file_content= file_content,
                                                          file_id= file_id,
                                                          chunk_size= chunk_size,
                                                          overlap_size= overlap_size)
    
    if file_chunks is None or len(file_chunks) ==0:
        return JSONResponse(
                content = {
                    'signal': ResponseSignals.PROCESSING_FAILED.value,}
                    
            )

    
    return file_chunks
        


   

    

