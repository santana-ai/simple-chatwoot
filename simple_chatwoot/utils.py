from typing import Dict

from requests.models import Response

def check_response(response: Response, expected_code:int, error_message:str)->Dict:
    if response.status_code == expected_code:
            json_response_dict = response.json()
            return json_response_dict
    else:
        try:
            print("response status code is: ", response.status_code)
            print("response body is: ", response.json())
            raise Exception(error_message)
        except Exception:
            raise Exception(error_message)
