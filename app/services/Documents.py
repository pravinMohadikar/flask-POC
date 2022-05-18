from flask import request, jsonify

def UploadDocument():
    try:
        if 'file' not in request.files:
            print("No file attached")
            return jsonify({
                'error':'No file attached',
                'message':'No file attached to upload'
            }), 400
        if 'Content-type' not in request.headers:
            return jsonify({'Content-type'})

        file = request.file['file']
        #
        # if file and allowed_file(file.filename):
        #     req
    except Exception as e:
        raise e

