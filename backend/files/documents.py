from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models.file import File


@registry.register_document
class FileHeadingDocument(Document):
    class Index:
        name = 'headings'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
    class Django:
        model = File
        fields = ['heading']