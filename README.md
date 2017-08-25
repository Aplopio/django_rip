# Rest in Peace (RIP)

Django_RIP is a framework for writing http CRUD api's in Django. Majority of the functinality of Django_RIP is not dependent on Django. Django_RIP is a thin wrapper on top of RIP to provide url routing, http request and response management and data fetching from models. RIP itself is written purely in Python and is framework agnostic. Writing a wrapper like Django_RIP over RIP for Flask or any other framework would be very simple [contributions welcome!]

## Getting started

A building block for writing a CRUD api is a Resource. Resources are where users will make http requests. Let's see how to define a resource (we will define an example "Tweet" resource)

```python
from django_rip import fields
from django_rip.django_crud_resource import DjangoModelResource
from django_rip.rip.crud.crud_actions import READ_WRITE_ACTIONS
from yourapp.models import TweetModel

class TweetResource(DjangoModelResource):
    id = fields.StringField(max_length=10, required=True, field_type=FieldTypes.READONLY)
    author = fields.StringField(max_length=100, required=True, field_type=FieldTypes.READONLY)
    body = fields.StringField(max_length=100, required=True, field_type=FieldTypes.READONLY)
    is_active = fields.BooleanField(required=True)
    resource_uri = fields.ResourceUriField()

    class Meta:
        resource_name = 'tweets'
        model_cls = TweetModel
        allowed_actions = READ_WRITE_ACTIONS

```
Above, we defined a CRUD resource called 'Tweet' by extending it from a DjangoModelResource. That's it! That gets you a fully working, read-write API for the TweetModel and supports all CRUD operations in a RESTful way. It is easy add user authentication, data access authorization etc. Infact, is also very simple to fetch data from our own data source instead of the TweetModel.

## Connecting to urls

Router helps with generating urls for a Resource. A DjangoResource extends from django class based view and the router simply generates the right urls and hooks the resource to them. Let's see how to define a router.

```python
from django_rip.http_adapter.django_router import DefaultRouter

router = DefaultRouter(url_prefix='api/v1')
router.register(TweetResource)

--- urls.py

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls))
]
```
This makes TweetResource available at /api/v1/tweets/{id}
---

## Custom data / Custom authorization
It is easy to get custom data or add custom permission checks to see if the user has access the the data they are requesting.

```python
from django_rip import fields
from django_rip.django_crud_resource import DjangoModelResource
from django_rip.rip.crud.crud_actions import READ_WRITE_ACTIONS
from django_rip.rip.generic_steps import error_types
from yourapp.models import TweetModel

class TweetDataManager(ModelDataManager):
    def get_entity(self, request, **kwargs):
        entity = super(TweetDataManager, self).get_entity(request, **kwargs)
        if entity is None:
            return error_types.ObjectNotFound
        
        if not user_has_permission(request.user, entity):
            return error_types.ActionForbidden
        
        return entity


class TweetResource(DjangoModelResource):
    id = fields.StringField(max_length=10, required=True, field_type=FieldTypes.READONLY)
    author = fields.StringField(max_length=100, required=True, field_type=FieldTypes.READONLY)
    body = fields.StringField(max_length=100, required=True, field_type=FieldTypes.READONLY)
    is_active = fields.BooleanField(required=True)
    resource_uri = fields.ResourceUriField()

    class Meta:
        resource_name = 'tweets'
        model_cls = TweetModel
        allowed_actions = READ_WRITE_ACTIONS
        data_manager_cls = TweetDataManager

```

You can also fetch the tweet entity from custom data sources instead of calling the parent class function above.


## Under the Hood
Underneath, RIP is simply designed as a collection of actions. A resource is just a container of a few actions (typically bound together as per some business needs). Each action is implemented as a pipeline of functions. Each of these functions take a ```request```/```response```, potentially modify it, and pass on the result to the next function in the pipeline. To those who are familiar with Django Middleware, this follows a similar pattern.

