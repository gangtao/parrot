import time
import random
import socket
import struct
import re

class BatchFileGenerator(object):
    def __init__(self, model, path):
        self._model = model
        self._path = path

    def generate(self, patterns, number):
        with open(self._path, "w") as output:
            for i in range(number):
                random_pattern = patterns[random.randint(0, len(patterns))-1]
                for p in self._model["patterns"]:
                    if p["name"] == random_pattern:
                        event = self._gen_event(p["pattern"])
                        output.write(event)
                        output.write("\n")

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
        return event

    def _gen_replacement(self, key):
        values = self._model["replacement"][key]
        return values[random.randint(0, len(values))-1]

    def _gen_timestamp(self, format):
        return time.strftime(format)

    def _gen_random(self, format):
        if format == "ipv4":
            return  socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

        if format.startswith("integer"):
            scope = re.findall(r"integer\[(\d+):(\d+)\]", format)[0]
            
            result =  random.randint(int(scope[0]),int(scope[1]))
            return str(result)

        return format