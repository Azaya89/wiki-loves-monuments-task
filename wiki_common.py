import requests

# Helper functions
def _page_id(data: str) -> str:
    """Returns the page ID from the json formatted data page."""

    pageid = [id for id in data["query"]["pages"]]
    pageid = pageid[0]
    return pageid


def _common_data(file: str) -> str:
    """Gets a file name and returns all the common metadata information of the file API."""

    # Fetch the file API in json format.
    response = requests.get(
        "https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=commonmetadata&format=json&titles="
        + file
    )

    # Format the response to be json readable in python.
    data = response.json()

    # Get the page ID of the file.
    pageid = _page_id(data)

    # Get the metadata API information.
    metadata = data["query"]["pages"][pageid]["imageinfo"][0]["commonmetadata"]
    return metadata


def _get_info(file: str, key: str, value: str) -> str:
    """Returns the value category specified from the image key provided."""
    # Return a value if available.
    for i in _common_data(file):
        if i["name"] == key:
            value = i["value"]
            return value

    # Return a message if value is unavailable.
    return f"*{value} Unavailable.*"


# Main functions
def get_location(file: str) -> str:
    """Returns the primary location where the image was taken."""

    location = _get_info(file, "SublocationDest", "Location")
    return f"Image Location: {location}"


def get_country(file: str) -> str:
    """Returns the country where the image was taken."""

    country = _get_info(file, "CountryDest", "Country")
    return f"Country Location: {country}"


def date_taken(file: str) -> str:
    """Returns the Date/Time when the image was originally taken."""

    date = _get_info(file, "DateTimeOriginal", "Date of Image")
    return f"Date of Image: {date}"


def get_dimension(file: str) -> str:
    """Returns the original dimensions(size, width, height) of the image"""

    # Fetches the file image info API in json format.
    response = requests.get(
        "https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=dimensions&format=json&titles="
        + file
    )

    # Renders the API in json readable format for python.
    data = response.json()

    # Get the page ID of the file.
    pageid = _page_id(data)

    # Get the image dimensions from the imageinfo dictionary
    try:
        dimensions = data["query"]["pages"][pageid]["imageinfo"][0]
        return f"Image Dimensions: {dimensions}"

    # Return a message if size information is unavailable.
    except KeyError:
        return "Image dimensions unavailable."


def get_camera(file: str) -> str:
    """Returns the Camera Model used in making the image."""

    camera = _get_info(file, "Model", "Camera Model")
    return f"Camera Model: {camera}"


def get_coordinates(file: str) -> str:
    """Returns the geo-location (Latitude and Longitude) of the Image."""

    # Fetch the file API in json format.
    response = requests.get(
        "https://commons.wikimedia.org/w/api.php?action=query&prop=coordinates&format=json&titles="
        + file
    )

    # Format the response to be json readable in python.
    data = response.json()

    # Get the page ID of the file.
    pageid = _page_id(data)

    # Get coordinates of the image from the coordinate dictionary.
    try:
        coordinates = data["query"]["pages"][pageid]["coordinates"][0]

        geo_location = (
            f"Latitude: {coordinates['lat']}, Longitude: {coordinates['lon']}"
        )
        return geo_location

    # Return a message if geo-location information is unavailable.
    except KeyError:
        return "Geo-location unavailable."


# Example:
print(
    date_taken(
        "File:Webysther_20211009173053_-_Edifício_à_Rua_Floriano_Peixoto,_1386.jpg"
    )
)
