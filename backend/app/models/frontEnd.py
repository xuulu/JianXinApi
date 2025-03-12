from tortoise import fields,models

class ApiList(models.Model):
    name = fields.CharField(max_length=20, unique=True, description='接口名称')  # unique 是否唯一
    path = fields.CharField(max_length=20, unique=True, description='接口路径')
    type = fields.JSONField(max_length=30, description='接口类型')
    urlExample = fields.CharField(max_length=30, description='接口示例',blank=True, null=True)
    introduce = fields.CharField(max_length=60, description='接口介绍',blank=True, null=True)
    requestParameters = fields.JSONField(max_length=300, description='请求参数',blank=True, null=True)
    returnParameters = fields.JSONField(max_length=300, description='返回参数',blank=True, null=True)



