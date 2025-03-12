from tortoise import fields,models

class CosVideo(models.Model):
    url = fields.CharField(max_length=2048,unique=True)
    class Meta:
        table = 'data_cos_video'

class CosImage(models.Model):
    url = fields.CharField(max_length=2048,unique=True)
    class Meta:
        table = 'data_cos_image'