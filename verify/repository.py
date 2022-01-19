from verify.utils.veriff import Variff


def create_session(request_data):
    try:
        session_response = Variff.create_session_api(request_data)
        session_verification = session_response["verification"]
        result, message, data = True, "Success", session_verification

    except Exception as e:
        result, message, data = False, str(e), None
    return result, message, data
