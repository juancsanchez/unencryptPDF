import logging
import azure.functions as func
import io
from pypdf import PdfReader, PdfWriter
from pypdf.errors import FileNotDecryptedError, EmptyFileError

# It's good practice to initialize the Function App object.
# The bp object will be used to register our function.
app = func.FunctionApp()

@app.route(route="decrypt", auth_level=func.AuthLevel.FUNCTION)
def decrypt_pdf(req: func.HttpRequest) -> func.HttpResponse:
    """
    An HTTP-triggered Azure Function to decrypt a password-protected PDF.

    This function expects a multipart/form-data POST request containing:
    1. 'pdf_file': The encrypted PDF file.
    2. 'password': The password for the PDF file.

    Args:
        req (func.HttpRequest): The incoming HTTP request object.

    Returns:
        func.HttpResponse: An HTTP response containing either the decrypted
                           PDF file stream or a JSON error message.
    """
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # --- 1. Retrieve and Validate Request Data ---
        # The request must be multipart/form-data
        post_files = req.files
        form_data = req.form

        pdf_file = post_files.get('pdf_file')
        password = form_data.get('password')

        # Do not log the password or file content for security reasons.
        if not pdf_file or not password:
            logging.warning("Request is missing 'pdf_file' or 'password' field.")
            return func.HttpResponse(
                '{"error": "Request must include a `pdf_file` and `password` field in multipart/form-data."}',
                status_code=400,
                mimetype="application/json"
            )

        # --- 2. Process the PDF in Memory ---
        # Read the uploaded file's content into a bytes buffer.
        pdf_bytes = pdf_file.read()
        input_stream = io.BytesIO(pdf_bytes)

        # --- 3. Decryption Logic ---
        try:
            reader = PdfReader(input_stream)

            # Verify if the PDF is actually encrypted.
            if not reader.is_encrypted:
                logging.warning("Attempted to decrypt a non-encrypted PDF.")
                return func.HttpResponse(
                    '{"error": "The provided PDF file is not encrypted."}',
                    status_code=422, # Unprocessable Entity
                    mimetype="application/json"
                )

            # Attempt to decrypt the PDF with the provided password.
            if reader.decrypt(password) == 0:
                # pypdf's decrypt() returns 0 if the password is wrong.
                logging.warning("Incorrect password provided.")
                return func.HttpResponse(
                    '{"error": "Incorrect password provided for the PDF file."}',
                    status_code=401, # Unauthorized
                    mimetype="application/json"
                )

            # --- 4. Prepare Success Response ---
            # Create a new PDF writer and add the decrypted pages.
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            # Save the decrypted PDF to an in-memory stream.
            output_stream = io.BytesIO()
            writer.write(output_stream)
            output_stream.seek(0) # Rewind the stream to the beginning.

            logging.info("PDF decrypted successfully.")
            return func.HttpResponse(
                body=output_stream.read(),
                status_code=200,
                mimetype='application/pdf',
                headers={
                    'Content-Disposition': 'attachment; filename="decrypted.pdf"'
                }
            )

        except FileNotDecryptedError:
            # This is another way pypdf signals a wrong password.
            logging.warning("FileNotDecryptedError: Incorrect password.")
            return func.HttpResponse(
                '{"error": "Incorrect password provided for the PDF file."}',
                status_code=401, # Unauthorized
                mimetype="application/json"
            )
        except EmptyFileError:
            # This handles cases where the file is 0 bytes or not a valid PDF.
            logging.error("EmptyFileError: The uploaded file is empty or not a valid PDF.")
            return func.HttpResponse(
                '{"error": "The uploaded file is empty or not a valid PDF."}',
                status_code=400,
                mimetype="application/json"
            )
        except Exception as e:
            # Catch other potential pypdf or processing errors.
            logging.error(f"An unexpected error occurred during PDF processing: {e}", exc_info=True)
            return func.HttpResponse(
                '{"error": "An unexpected error occurred while processing the PDF."}',
                status_code=500,
                mimetype="application/json"
            )

    except Exception as e:
        # Catch-all for any other unexpected errors.
        logging.error(f"An unexpected error occurred in the function: {e}", exc_info=True)
        return func.HttpResponse(
             '{"error": "An internal server error occurred."}',
             status_code=500,
             mimetype="application/json"
        )
