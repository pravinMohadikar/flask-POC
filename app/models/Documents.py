from S3UploadDocument import UploadDocumentS3

def uploadDocument(self, file, request_data):
    try:
        S3Bucket = "Hr-services-documents"
        S3key = ""
        UploadDocumentS3(file, S3Bucket, S3key, request_data)
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        data_insert = {
            "document_type_id": None if "document_type_id" not in request_data else request_data["document_type_id"],
            "filename": file.filename,
            "filetitle": None if "filetittle" not in request_data else request_data["filetitle"],
            "filedescription": None if "filedescription" not in request_data else request_data["filedescription"],
            "fileextension": request_data["fileextension"],
            "s3_bucket": S3Bucket,
            "s3_key": S3key + "/" + file.filename
        }
        return {"status": "Success", "description":"Sucessfully loaded the document in AWS S3"}
    except Exception as e:
        raise e