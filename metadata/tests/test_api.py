from rest.tests.base import TestApi
from metadata.api import *
from metadata.tests.assets import Assets
from gndata_api.fake import update_keys_for_model


class TestMetadataApi(TestApi):
    """
    Metadata resource API test class.
    """
    def setUp(self):
        super(TestMetadataApi, self).setUp()
        self.resources = [
            ValueResource, PropertyResource, SectionResource, DocumentResource
        ]
        for resource in self.resources:
            update_keys_for_model(resource.Meta.object_class)
        self.assets = Assets().fill()