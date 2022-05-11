from django.http import HttpResponse
from django.http import HttpResponse
from store.models import Product
from tags.models import TaggedItem


def say_hello(request):
    queryset = TaggedItem.objects.get_tags_for(Product, 1)

    return HttpResponse("Hello, world!")
