from django.core.management import BaseCommand, CommandError
from django.db.models import get_model
import re


class Command(BaseCommand):
    """
    Updates a model's instances to have unique ascending order values.  Useful when applying the OrderedModel base
    class to a model with existing data.

    If applying the OrderedModel base class to an existing model, run this command after your schema migration.
    """

    def handle(self, *args, **kwargs):
        try:
            if not re.match(r'[a-zA-Z0-9_]+\.[a-z_A-Z0-9_]', args[0]):
                raise CommandError("First argument must be a model name")
        except IndexError:
            raise CommandError("Command requires a model as argument, denoted by app_label.Model")

        model_name = args[0]
        model_class = get_model(model_name.split(".")[0], model_name.split(".")[1])

        if model_class is None:
            raise CommandError("Could not retrieve model denoted by %s" % model_name)

        # use the default ordering
        objects = model_class.objects.all()
        order = 1
        for o in objects:
            o.order = order
            o.save()
            order += 1

        print "Successfully updated order for %d %s objects" % (order - 1, model_name)