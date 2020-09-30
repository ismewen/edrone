## Introduction
drf开发的工具类
## Installation

clone the repo from GitHub and then:

    python setup.py install

## QuickStart

### NestedModelField

serialise to model instance According to `lookup_field` in model and `looup_field_name` in data

Usage:
```python

from dutils.serializers import Serializer
from dutils.fields import NestedModelField


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class EmailSerializer(Serializer):
    username = models.CharField('email',max_length=150,unique=True)
    user = NestedModelField(model=User, lookup_field="id", lookup_field_name="user_id")
    class Meta:
        model = "user", "username"
data = {"user_id": 1, "email": "someone@email.com"}
ss = EmailSerializer(data)
ss.is_valid()
email = ss.save()
print(email, email.user)
# <Email someone@email.com>, <User 1>

```
### viewset && routers
!! important must discovery all viewset

Usage:
```python
from dutils.views import ViewSet 
from dutils.routers import router

class EmailViewSet(ViewSet):
    name = "email"
    path = "emails"
    model = Email
    serializer_class = EmailSerializer
    serializer_mapping = {
        # 不同的操作使用不同的序列化器
        "create": EmailCreateSerializer,
        "update": EmailUpdateSerializer,
    }
    
class UserViewSet(ViewSet):
    name = "user"
    path = "users"
    model = User
    nested_viewsets = [
        EmailViewSet
    ]
    serializer_class = UserSeriliazer    
    filter_fields = "name","id"

    
router.custom_register(UserViewSet)
```

add urls in your project urls

```python
from dutils.routers import router
# must discovery all viewset
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^v1/', include(router.urls)),   

```

Now, your project has the following four urls

- /v1/users/{user_pk}/ # allow http action `GET`, `Delete`, `Patch` 
- /v1/users/ # allow http action `Get`, `Post'
- /v1/users/{user_pk}/emails/{email_pk}/ # allow http action `GET`, `Delete`, `Patch` 
- /v1/users/{user_pk}/emails/ # allow http action `Get`, `Post'

### StateMachine

combined [transitions](https://github.com/pytransitions/transitions) with django model. 

### filter support
添加如下配置
```python
REST_FRAMEWORK = {

    'DEFAULT_FILTER_BACKENDS': ("dutils.utils.q.DutilFilterBackend",)
}
```

GET /v1/users/?q=name=ethan,id__gt=3

生成的查询语句如下

```python
query = Users.objects.all().filter(name="ethan").filter(id__gt=3)
```

### decorators  

#### class_method_retry
when specific error occurs, retry specific times after sleep second

#### viewset_url_params_require
define mandatory params, if not receive, raise `RequestQueryParamsMissing` Error

example:

```python
class EmailViewSet(ViewSet):
    name = "email"
    path = "emails"
    model = Email
    serializer_class = EmailSerializer
    
    @viewset_url_params_require(["say", "hello"])
    @action(list=True)
    def say_hello(self, *args, **kwargs):
        return "hello world"
        
url的查询参数中必须要包含say, hello 这两个参数

```
