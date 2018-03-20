import time
import random
import socket
import struct
import re
import csv
import json


class Generator(object):
    def __init__(self, model):
        self._model = model

    def generate(self, patterns, number):
        events = list()
        for i in range(number):
            random_pattern = patterns[random.randint(0, len(patterns)) - 1]
            for p in self._model["patterns"]:
                if p["name"] == random_pattern:
                    event = dict()
                    event["value"] = self._gen_event(p["pattern"])
                    event["name"] = self._model["name"]
                    event["type"] = p["sourcetype"]
                    event["file"] = p["name"]
                    if "breaker" in p:
                        event["breaker"] = p["breaker"]
                    events.append(event)
        return events

    def _gen_event(self, pattern):
        event = ""
        for p in pattern:
            if "token" not in p:
                event += p["value"]
            else:
                token = p["token"]
                ttype = token["type"]
                if ttype == "file" or ttype == "mvfile":
                    event += self._gen_replacement(token["replacement_values"])
                elif ttype == "timestamp":
                    event += self._gen_timestamp(token["replacement"])
                elif ttype == "random":
                    event += self._gen_random(token["replacement"])
        # TODO: need break event into multiple events in case it contains multiple events
        return event

    def _gen_replacement(self, key):
        values = self._model["replacement"][key]
        return values[random.randint(0, len(values)) - 1]

    def _gen_timestamp(self, format):
        return time.strftime(format)

    def _gen_random(self, format):
        if format == "ipv4":
            return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

        if format.startswith("integer"):
            scope = re.findall(r"integer\[(\d+):(\d+)\]", format)[0]

            result = random.randint(int(scope[0]), int(scope[1]))
            return str(result)

        return format


class BatchFileGenerator(Generator):
    def __init__(self, model, path):
        Generator.__init__(self, model)
        self._path = path

    def generate(self, patterns, number):
        events = super(BatchFileGenerator, self).generate(patterns, number)
        with open(self._path, "w") as output:
            for event in events:
                output.write(event["value"])
                output.write("\n")


class CSVFileGenerator(Generator):
    def __init__(self, model, path):
        Generator.__init__(self, model)
        self._path = path

    def generate(self, patterns, number):
        events = super(CSVFileGenerator, self).generate(patterns, number)
        with open(self._path, "wb") as output:
             writer = csv.writer(output)
             writer.writerow(events[0].keys())
             for event in events:
                writer.writerow(event.values())


class JSONFileGenerator(Generator):
    def __init__(self, model, path):
        Generator.__init__(self, model)
        self._path = path

    def generate(self, patterns, number):
        events = super(JSONFileGenerator, self).generate(patterns, number)
        with open(self._path, "w") as output:
            output.write(json.dumps(events))
