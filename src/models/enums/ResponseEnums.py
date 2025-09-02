from enum import Enum

class ResponseSignals(Enum):
    FILE_TYPE_NOT_SUPPORTED ="file type not supported"
    FILE_SIZE_EXCEEDED = "file size exceeded"
    FILE_UPLOAD_SUCCESS = 'file upload success'
    FILE_UPLOAD_FAILED = 'file upload failed'
    PROCESSING_SUCCESS = 'processing success'
    PROCESSING_FAILED = "processing failed"

    