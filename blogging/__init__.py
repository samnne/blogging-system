import hashlib
from typing import Type
import json


def update_file(payload, dest_file, Encoder):
    """ """
    try:
        file = open(dest_file, "w")
        j_string = json.dumps(payload, indent=4, cls=Encoder)
        file.write(j_string)
        file.close()
    except Exception as e:
        print(f"Error Writing to File, {e}")


def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        cur_id = -1
        # if the class instance has id attribute, set the cur_id
        if hasattr(arr[mid], "id"):
            cur_id = arr[mid].id

        # if the class instance has code attribute, set the cur_id
        if hasattr(arr[mid], "code"):
            cur_id = arr[mid].code

        if cur_id == target:
            return arr[mid]
        elif cur_id < target:
            left = mid + 1
        else:
            right = mid - 1
    return None


def get_password_hash(password):
    # Learn a bit about password hashes by reading this code
    encoded_password = password.encode("utf-8")  # Convert the password to bytes
    hash_object = hashlib.sha256(
        encoded_password
    )  # Choose a hashing algorithm (e.g., SHA-256)
    hex_dig = (
        hash_object.hexdigest()
    )  # Get the hexadecimal digest of the hashed password
    return hex_dig


def raise_exception(exception: Type[Exception], msg: str = ""):
    # Middleware to raise exceptions
    print(msg)
    raise exception
