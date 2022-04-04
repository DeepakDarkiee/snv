import logging
from django.conf import settings

from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import APIException, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from snv.common import app_logger, rest_utils


from ..models import Album, Gallery, Image
from .serializers import (
    AlbumDetailSerializer,
    AlbumSerializer,
    GalleryDetailSerializer,
    GallerySerializer,
    ImagePreviewSerializer,
    ImageUploadSerializer,
)
from .simple_fb_auth import IsFacebookAuthenticated, SimpleFacebookAuthentication

logger = logging.getLogger(__name__)


def get_gallery(path):
    """
    Selects `gallery` from database based on its `path` attribute.
    """
    gallery = None
    try:
        gallery = Gallery.objects.get(name=path)
    except Gallery.DoesNotExist:
        raise NotFound()
    except Exception:
        raise APIException()

    return gallery


def get_image(gallery_path, image_path):
    """
    Selects `image` from database based on its `gallery_path` and `image_path`
    attributes.
    """
    image = None
    try:
        image = Image.objects.get(gallery__name=gallery_path, path=image_path)
    except Image.DoesNotExist:
        raise NotFound()
    except Exception as e:
        logger.error(e)
        raise APIException()

    return image


class GalleryListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GallerySerializer
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        user = request.user
        galleries = Gallery.objects.filter(user__id=user.id)
        serializer = GallerySerializer(galleries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # logger.debug(request.user)
        data = request.data
        
        serializer = self.serializer_class(data=data,)
        # serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errors = serializer.errors.get("name")
        if errors:
            if len(errors) == 1 and errors[0].code == "unique":
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GalleryDetailView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = GalleryDetailSerializer
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, path, format=None):

        gallery = get_gallery(path)
        serializer = GalleryDetailSerializer(gallery)
        return Response(serializer.data)
    
    def post(self, request, path, format=None):
        logger.debug(request.user)
        success_response = {"uploaded": [], "errors": []}

        # find galery
        gallery = get_gallery(path)

        # in case of no files in body, return bad request
        if not request.FILES:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for key, val in request.FILES.items():
                image = Image.create_from_file(gallery, val, request.user)
                serializer = ImageUploadSerializer(data=image)
                if serializer.is_valid():
                    img = serializer.save()
                    success_response["uploaded"].append(
                        {
                            "name": img.name,
                            "path": img.path,
                            "fullpath": img.fullpath,
                            "modified": img.modified,
                        }
                    )
                else:
                    success_response["errors"].append(
                        {"name": val.name, "error": serializer.errors}
                    )

            return Response(success_response, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            raise APIException()

    def delete(self, request, path, format=None):
        gallery = get_gallery(path)
        gallery.delete()
        return Response(None, status=status.HTTP_200_OK)
    

class ImageDetailView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    # serializer_class = GallerySerializer
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, gallery_path, image_path, format=None):
        # galleries = Gallery.objects.all()
        # serializer = GallerySerializer(galleries, many=True)
        # return Response(serializer.data)    
        logger.debug("GET Image {}/{}".format(gallery_path, image_path))
        image = get_image(gallery_path, image_path)
        return FileResponse(image.file.file)

    def delete(self, request, gallery_path, image_path, format=None):
        logger.debug("DELETE Image {}/{}".format(gallery_path, image_path))
        image = get_image(gallery_path, image_path)
        image.delete()
        return Response(None, status=status.HTTP_200_OK)
        

class ImagePreviewView(generics.GenericAPIView):
    """
    Image preview (thumbnail) entrypoint.

    - `GET` method returns image thumbnail with `x_size` and `y_size`. If one
    of size values is zero, resizing method preserves ratio. Image selection
    is based on `gallery_path` and `image_path` attributes.
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = ImagePreviewSerializer

    def get(self, request, x_size, y_size, gallery_path, image_path, format=None):
        logger.debug(
            (
                "GET Image preview x={x_size}, y={y_size}, path={gallery_path}/{image_path}".format(
                    x_size=x_size,
                    y_size=y_size,
                    gallery_path=gallery_path,
                    image_path=image_path,
                )
            )
        )

        serializer = ImagePreviewSerializer(data={"x_size": x_size, "y_size": y_size})
        if serializer.is_valid():
            image = get_image(gallery_path, image_path)
            # resize image
            try:
                resized_image = image.get_thumbnail(x_size, y_size)
            except Exception as e:
                logger.error(e)
                raise APIException()

            return FileResponse(resized_image)

        return Response(serializer.errors, status=status.HTTP_200_OK)

class AlbumListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AlbumSerializer
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        user = request.user
        albums = Album.objects.filter(gallery__user__id=user.id)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # logger.debug(request.user)
        data = request.data
        serializer = self.serializer_class(data=data)
        # serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errors = serializer.errors.get("name")
        if errors:
            if len(errors) == 1 and errors[0].code == "unique":
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AlbumDetailSerializer
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, id=None , format=None):
        try :
            user=request.user
            album=user.user_gallery.albums.get(id=id)
            serializer = AlbumSerializer(album)
            return Response(serializer.data)
        except Exception as e:
            return rest_utils.build_response(
                                status.HTTP_400_BAD_REQUEST,
                                rest_utils.HTTP_REST_MESSAGES["400"],
                                data=None,
                                errors=str('Album Does Not Exists'),
                            )

    
    def put(self, request, id=None, format=None):
        logger.debug(request.user)
        success_response = {"added": [], "errors": []}
        try:
            data = request.data
            image_list = data['images']

            # find galery
            user=request.user
            album=user.user_gallery.albums.get(id=id)
            
            for image in image_list:
                image = Image.objects.get(id=image) 
                album.images.add(image)
            album.save()  
            success_response["added"].append(
                                {
                                    "data":data,
                                }
                            )


            return Response(success_response, status=status.HTTP_200_OK)
        except Exception as e:
            return rest_utils.build_response(
                                status.HTTP_400_BAD_REQUEST,
                                rest_utils.HTTP_REST_MESSAGES["400"],
                                data=None,
                                errors=str('Album Does Not Exists'),
                            )

    def delete(self, request, id=None, format=None):
        try:
            user=request.user
            album=user.user_gallery.albums.get(id=id)
            album.delete()
            return Response(None, status=status.HTTP_200_OK)
        except Exception as e:
            return rest_utils.build_response(
                                status.HTTP_400_BAD_REQUEST,
                                rest_utils.HTTP_REST_MESSAGES["400"],
                                data=None,
                                errors=str('Album Does Not Exists'),
                            )

class AlbumSharingView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request ,id=None, format=None):
        success_response = {"Shareable_Link": [], "Msg": []}
        try :
            link = settings.URL
            link = f"{link}/api/album/{id}"
            success_response['Shareable_Link'].append(link)
            success_response['Msg'].append('Link Generated Successfully')

            return Response(success_response,status=status.HTTP_200_OK)

        except Exception as e:
            return rest_utils.build_response(
                                status.HTTP_400_BAD_REQUEST,
                                rest_utils.HTTP_REST_MESSAGES["400"],
                                data=None,
                                errors=str('Album Does Not Exists'),
                            )