from verify.utils.veriff import Variff


def create_session(request_data):
    try:
        session_response = Variff.create_session_api(request_data)
        session_verification = session_response["verification"]
        result, message, data = True, "Success", session_verification

    except Exception as e:
        result, message, data = False, str(e), None
    return result, message, data


def front_document_upload(request_data):
    try:
        session_response = Variff.upload_document_front_api(request_data)
        print(session_response)
        doc_front = session_response["image"]
        result, message, data = True, "Success", doc_front

    except Exception as e:
        result, message, data = False, str(e), None
    return result, message, data


def back_document_upload(request_data):
    try:
        session_response = Variff.upload_document_back_api(request_data)
        print(session_response)
        doc_back = session_response["image"]
        result, message, data = True, "Success", doc_back

    except Exception as e:
        result, message, data = False, str(e), None
    return result, message, data


def person_face_upload(request_data):
    try:
        session_response = Variff.person_face_api(request_data)
        print(session_response)
        face = session_response["image"]
        result, message, data = True, "Success", face

    except Exception as e:
        result, message, data = False, str(e), None
    return result, message, data


def get_decision(user):
    try:
        session_response = Variff.get_decision_api(user)
        print(session_response)
        decision = session_response["verification"]
        result, message, data = True, "Success", decision

    except Exception as e:
        result, message, data = False, str(e), None
    return result, message, data
