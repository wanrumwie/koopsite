from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

def delete_content_types_for_removed_apps_or_models():
    # List of deleted apps
    DEL_APPS = ["app-you-deleted", "second-app-deleted"]
    # List of deleted models (that are not in the app deleted) In lowercase!
    DEL_MODELS = ["model-you-deleted", "second-model-deleted"]

    ct = ContentType.objects.all().order_by("app_label", "model")

    for c in ct:
        if (c.app_label in DEL_APPS) or (c.model in DEL_MODELS):
            print("Deleting Content Type %s %s" % (c.app_label, c.model))
            c.delete()

class ContentTypesTest(TestCase):

    def test_content_types(self):
        ct = ContentType.objects.all().order_by("app_label", "model")
        print('Content types:')
        print('-'*61)
        print("%-30s %-30s" % ('application', 'model'))
        print('-'*61)
        for c in ct:
            print("%-30s %-30s" % (c.app_label, c.model))
        print('-'*61)
        # self.assertEqual(view_func(0), 'passed')
        # self.assertEqual(decorated(view_func)(self.request, pk='3'), 'passed')
        # self.assertEqual(type(decorated(view_func)(self.request, pk='4')), HttpResponseRedirect)


