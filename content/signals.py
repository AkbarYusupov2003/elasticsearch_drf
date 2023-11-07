import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry

from content import models


@receiver(post_save)
def update_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']    
    
    if app_label == 'content':
        if model_name == 'content':
            if kwargs.get('update_fields') != frozenset(("rating", "rating_count")):
                if kwargs["instance"].draft == True:
                    registry.delete_related(instance)
                    registry.delete(instance)
                else:
                    registry.update(instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs["instance"]

    if app_label == "content":
        if model_name == "content":
            registry.update(instance)
            
            
# from django.core.management import call_command

# TODO use: call_command("search_index", "--populate")


# import time

# def test():
#     start_time = time.time()
#     content = models.Content.objects.get(title_ru="Бог игроков")
#     content.rating = content.rating + 1
#     content.save(update_fields=["rating_count", "rating"])
#     # for content in models.Content.objects.all()[:100]:
#     #     content.rating = content.rating
#     #     content.rating_count = content.rating_count 
#     #     content.save()
#     call_command("search_index", "--populate")
#     # os.system("python manage.py search_index --populate")
#     print("--- %s seconds ---" % (time.time() - start_time))
