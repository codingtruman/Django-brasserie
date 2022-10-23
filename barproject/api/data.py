import json
from django.db import IntegrityError
from .models import *


class LoadData(object):

    def __init__(self, data_source):
        with open(data_source, "r") as file:
            self.data = json.load(file)

    def load_beer(self):
        for beer in self.data:
            try:
                Beer.objects.create(
                    ref         = beer["ref"],
                    name        = beer["name"],
                    description = beer["description"]
                )
            except IntegrityError:
                return "Already loaded beer ref data! "
            else:
                return "Success! "

    def load_counter(self):
        for counter in self.data:
            try:
                Counter.objects.create(
                    name = counter["name"]
                )
            except IntegrityError:
                return "Already loaded bar counter data! "
            else:
                return "Success! "

    def load_stock(self):
        for stock in self.data:
            try:
                b = Beer.objects.get(id = stock["reference"])
                c = Counter.objects.get(id = stock["bar"])
                Stock.objects.create(reference = b, bar = c, stock = stock["stock"])
            except IntegrityError:
                return "Already loaded stock data! "
            else:
                return "Success! "

if __name__ == "__main__":
    from os.path import join
    def load(request):
        file_method = (("references.json", "load_beer"), ("counters.json", "load_counter"), ("stocks.json", "load_stock"))
        result = []
        for file, method in file_method:
            # get the absolute path of each json file
            data_source = join(TEMPLATES[0]["DIRS"][0], file)
            # construct the object and call each method to load data
            result += eval("LoadData(data_source)." + method + "()")
        return HttpResponse(result)