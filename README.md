# Rest in Peace (RIP)

RIP is a python-based framework for writing a http-api. It is generic enough to create non RESTful apis too. Its currently written to support Django but can be easily extended for any other web-frameworks (like Flask, for instance).

## Getting started
Create a new (RIP) API object, like so
```python
from rip.api import Api
my_api = Api(name='api', version='0.1')
```

To the newly created api, you can add resources (endpoints). Resources are where users will make http requests. Let's see how to define a resource (we will define an example "Tweet" resource)
```python
from rip.crud.crud_resource import CrudResource, CrudActions
class Tweet(CrudResource):
    schema_cls = TweetSchema
    allowed_actions= [CrudActions.READ_LIST,
                        CrudActions.READ_DETAIL,
                        CrudActions.UPDATE_DETAIL,
                        CrudActions.CREATE_DETAIL,
                        CrudActions.DELETE_DETAIL]
    entity_actions_cls = TweetEntityActions
    serializer_cls = TweetEntitySerializer
    authorization_cls = TweetAuthorization
    allowed_filters = {'id': (EQUALS)}
    default_limit = 20
    default_offset = 0
```
Above, we defined a CRUD type resource called 'Tweet'. By defining it as a CRUD (or RESTful) resource, we need to give it some more configuration. As a typical REST resource, it needs a ```schema``` (a list of fields on that resource), and a set of actions that can be performed on that resource (```allowed_actions```). Its easy to see how you can restrict the actions that can be performed on the resource.

Lets see how the schema itself is defined.

```python
from rip.api_schema import ApiSchema
from rip.filter_types import EQUALS
from rip.schema.base_field import FieldTypes
from rip.schema import fields

class TweetSchema(ApiSchema):
    id = fields.StringField(max_length=10, required=True,
                     field_type=FieldTypes.READONLY)
    author = fields.StringField(max_length=100, required=True,
                       field_type=FieldTypes.READONLY)
    body = fields.StringField(max_length=100, required=True,
                               field_type=FieldTypes.READONLY)
    is_active = fields.BooleanField(required=True)
    resource_uri = fields.ResourceUriField()

    class Meta:
        schema_name = 'tweet'
```
---

Now, lets examine the ```Tweet``` resource again. What are ```entity_actions``` and ```schema_mapper```?

This is the slightly complex part. RIP assumes that each resource is constructed from an ```entity```. To be specific, every field of the resource can be constructed from one or more fields on the corresponding ```entity```. Entities, typically, are business objects that mean something speciic to your app. In this case, it is likely that your app has an internal entity called ```tweet``` which will be used. In simple Django projects, entities can also be ```django.model.Model``` objects.

The ```entity_actions``` configuration defines a how these entities are generated. Here's an example definition.

```python
from myapp.models import Tweet
from rip.generic_steps.default_entity_actions import DefaultEntityActions

class TweetEntityActions(DefaultEntityActions):
    def get_entity_list(self, request, **kwargs):
        return Tweet.objects.filter(**kwargs)

    def update_entity(self, request, entity, **update_params):
        return Tweet.objects.update(id=entity.id, **update_params)

    def get_entity_list_total_count(self, request, **kwargs):
        return Tweet.objects.count(**kwargs)
```

Next, the ```entity_serializer``` is a class with functions (like 
```serialize_fieldname```) that describe how the ```fieldname``` in the resource is created from entities. 
If left blank, we simply pull the same fieldname from the entity.

```python
from rip.generic_steps.default_entity_serializer import DefaultEntitySerializer

class TweetEntitySerializer(DefaultEntitySerializer):
    def serialize_author(self, request, entity):
        return entity.full_name

```


Next, lets look at the ```authorization``` property of the ```Tweet``` resource. It defines any specific rules that you might want to implement to allow/deny access to certain actions or resource endpoints.

```python
from rip import error_types
from rip.generic_steps.default_authorization import DefaultAuthorization
from rip.response import Response

class TweetAuthorization(DefaultAuthorization):
    def authorize_read_detail(self, request):
        if request.user.username != request.entity.author.username:
            return Response(is_success=False, reason=error_types.ObjectNotFound)
        return request
```


And, that's it :)


## Under the Hood
Underneath, RIP is simply designed as a collection of actions. A resource is just a container of a few actions (typically bound together as per some business needs). Each action is implemented as a pipeline of functions. Each of these functions take a ```request```/```response```, potentially modify it, and pass on the result to the next function in the pipeline. To those who are familiar with Django Middleware, this follows a similar pattern.

## One last thing
Another cool feature of RIP is that it also exposes a python API (along with the HTTP api). This allows you to use the api internally without requiring to make HTTP calls. For instance,
- when one API call internally requires making another API call
- an internal function or backend job is best represented by an API call
- testing your API (without selenium)

You can call actions on your api objects easily, like so

```python
tweet_resource = Tweet()
response = tweet_resource.read_list(request)
```

