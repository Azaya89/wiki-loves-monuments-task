import requests


def _common_data(file: str) -> str:
    """Gets a file name and returns the common metadata information of the file API."""

    # Fetch the file API in json format.
    response = requests.get(
        "https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=commonmetadata&format=json&titles="
        + file
    )

    # Format the response to be json readable in python.
    data = response.json()

    # Get the page ID of the file.
    pageid = [id for id in data["query"]["pages"]]
    pageid = pageid[0]

    # Get the metadata API information.
    metadata = data["query"]["pages"][pageid]["imageinfo"][0]["commonmetadata"]
    return metadata


def get_location(file: str) -> str:
    """Returns the primary location where the image was taken."""

    # Fetch the metadata API information.
    _common_data(file)

    # Get the location information from the metadata dictionary.
    for l in _common_data(file):
        if l["name"] == "SublocationDest":
            location = l["value"]
            return f"Image Location: {location}"

    # Return a message if location information is unavailable.
    return "Image location unavailable."


def get_country(file: str) -> str:
    """Returns the country where the image was taken."""

    # Fetch the metadata information.
    _common_data(file)

    # Fetch the country information from the metadata dictionary.
    for c in _common_data(file):
        if c["name"] == "CountryDest":
            country = c["value"]
            return f"Country location: {country}"

    # Return a message if country information is unavailable.
    return "Country unavailable"


def date_taken(file: str) -> str:
    """Returns the Date/Time when the image was originally taken."""

    # Fetch the metadata information.
    _common_data(file)

    # Fetch the Datetime from the metadata dictionary.
    for d in _common_data(file):
        if d["name"] == "DateTimeOriginal":
            date = d["value"]
            return f"Date of Image: {date}"

    # Return a message if datetime information is unavailable.
    return "Date unavailable"


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
    pageid = [id for id in data["query"]["pages"]]
    pageid = pageid[0]

    # Get the image dimensions from the imageinfo dictionary
    try:
        dimensions = data["query"]["pages"][pageid]["imageinfo"][0]
        return f"Image Dimensions: {dimensions}"
    # Return a message if size information is unavailable.
    except KeyError:
        return "Image dimensions unavailable."


def get_camera(file: str) -> str:
    """Returns the Camera Model used in making the image."""

    # Fetch the metadata information.
    _common_data(file)

    # Get the camera model.
    for c in _common_data(file):
        if c["name"] == "Model":
            camera = c["value"]
            return f"Camera Model: {camera}"

    # Return a message if camera information is unavailable.
    return "Camera model unavailable."


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
    pageid = [id for id in data["query"]["pages"]]
    pageid = pageid[0]

    # Get coordinates of the image from the coordinate dictionary.
    try:
        coordinates = data["query"]["pages"][pageid]["coordinates"][0]

        geo_location = (
            f"Latitude: {coordinates['lat']}, Longitude: {coordinates['lon']}"
        )
        return geo_location
    except KeyError:
        return "Geo-location unavailable."

#Example:
print(
    date_taken(
        "File:Webysther_20211009111944_-_Igreja_Matriz_de_Nossa_Senhora_da_Candelária.jpg"
    )
)
