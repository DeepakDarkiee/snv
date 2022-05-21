
from gallery.models import Gallery


def is_album_exist(request_data):
    result, message = False, "Failed"
    album_name = request_data.get("album_name", None)
    gallery = request_data.get("gallery", None)
    # gallery =Gallery.objects.get(id=gallery_id)
    exist=gallery.albums.filter(name=album_name).exists()
    if not exist:
        result, message = True, "Successfully Added"
    else:
        result, message = False, "Already Exists"
    return result, message