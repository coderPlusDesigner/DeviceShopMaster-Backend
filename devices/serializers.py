from rest_framework import serializers
from .models import Products
from django.core.files.images import ImageFile
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class ProductsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Products
        fields = "__all__"


class CreateProductsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Products
        fields = "__all__"
    
    def create(self, validated_data):
        image = validated_data.get('image')
        thumbnail = validated_data.get('thumbnail')

        if not thumbnail and image:
            if isinstance(image, InMemoryUploadedFile):
                img = Image.open(BytesIO(image.read()))
            else:
                img = Image.open(image.path)

            if img.width > 400:
                output_size = (400, img.height * 400 // img.width)
                img.thumbnail(output_size)
                thumb_io = BytesIO()
                img.save(thumb_io, format='PNG')
                thumb_file = InMemoryUploadedFile(thumb_io, None, f"{image.name.split('.')[0]}_thumb.jpg", 'image/jpeg', thumb_io.tell(), None)
                validated_data['thumbnail'] = thumb_file

        return super().create(validated_data)
    

class UpdateProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

    def update(self, instance, validated_data):
        image = validated_data.get('image', instance.image)
        thumbnail = validated_data.get('thumbnail', instance.thumbnail)

        if image and image != instance.image:
            instance.image.delete()
            instance.thumbnail.delete()

            if isinstance(image, InMemoryUploadedFile):
                # Handling in-memory uploaded files
                img = Image.open(BytesIO(image.read()))
            else:
                img = Image.open(image.path)

            output_size = (400, img.height * 400 // img.width)
            img.thumbnail(output_size)
            thumb_io = BytesIO()
            img.save(thumb_io, format='PNG')
            thumb_file = InMemoryUploadedFile(thumb_io, None, f"{image.name.split('.')[0]}_thumb.jpg", 'image/jpeg', thumb_io.tell(), None)
            thumbnail = thumb_file
            instance = super().update(instance, validated_data)
            instance.image = image
            instance.thumbnail = thumbnail
        else:
            instance = super().update(instance, validated_data)

        instance.save()
        
        return instance
