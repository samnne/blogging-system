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

