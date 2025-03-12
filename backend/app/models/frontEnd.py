from tortoise import fields,models

class ApiList(models.Model):
    name = fields.CharField(max_length=20, unique=True, description='接口名称')  # unique 是否唯一
    path = fields.CharField(max_length=20, unique=True, description='接口路径')
    type = fields.JSONField(max_length=30, description='接口类型')
    urlExample = fields.CharField(max_length=30, description='接口示例',blank=True, null=True)
    introduce = fields.CharField(max_length=60, description='接口介绍',blank=True, null=True)
    requestParameters = fields.JSONField(max_length=300, description='请求参数',blank=True, null=True)
    returnParameters = fields.JSONField(max_length=300, description='返回参数',blank=True, null=True)


class ApiStats(models.Model):
    apilist: fields.ReverseRelation[ApiList] = fields.ForeignKeyField(
        model_name='models.ApiList',   # 外键关系的模型
        related_name='stats'           # 反向访问字段的名称
    )
    daily_count = fields.IntField(default=0)
    total_count = fields.IntField(default=0)


class FriendLinks(models.Model):
    name = fields.CharField(max_length=20, unique=True,description='网站名称')
    url = fields.CharField(max_length=30,unique=True,description='网站链接')
    email = fields.CharField(max_length=20, unique=True, description="邮箱地址")
    icon = fields.CharField(max_length=255,description='网站图标')
    description = fields.CharField(max_length=255,description='网站描述')
    is_approved = fields.BooleanField(default=False, description='是否已审核')

    class Meta:
        table = "friend_links"

