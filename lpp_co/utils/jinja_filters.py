from datetime import datetime


def format_datetime_to_date(date_str):
    try:
        date_obj = datetime.strptime(str(date_str), "%Y-%m-%d %H:%M:%S.%f")
        return date_obj.strftime("%d/%m/%Y")
    except Exception:
        return date_str


def substring_if_longer(value, length):
    if value is None:
        return ""  # Handle the case where input is None
    if not isinstance(value, str):
        return ""  # Handle cases where value is not a string
    if len(value) > length:
        return value[:length] + '...'  # Adjust the length as needed
    return value


def replace_none(value, to_value="-"):
    try:
        if value is None or value == "":
            return to_value
        else:
            # Ensure the value is a string before attempting to replace newlines
            return str(value).replace("\n", "<br>")
    except Exception:
        # In case of any unexpected error, return the default value
        return to_value
