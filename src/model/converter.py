import os
import re
import ConfigParser

EVENTGEN_CONF_BASE = "eventgen_confs"
EVENTGEN_CONF_PATH = "default/eventgen.conf"
EVENTGEN_CONF_SAMPLE_PATH = "samples"
EVENTGEN_SAMPLES_PATH = "eventgen_samples"
OPTION_NAMES = ["earliest", "latest", "breaker",
                "perDayVolume", "sourcetype", "source"]


class ModelConverter(object):
    def __init__(self, home=None):
        if home is not None:
            self._home = home
        else:
            self._home = os.path.abspath(os.path.join(os.path.dirname(
                os.path.realpath(__file__)), os.pardir, os.pardir))

        self._eventgen_samples_path = os.path.join(self._home, EVENTGEN_SAMPLES_PATH)

        self._replacement_cache = dict()

    def _get_samples(self, name):
        sample_path = os.path.join(self._home, EVENTGEN_CONF_BASE, name, EVENTGEN_CONF_SAMPLE_PATH)
        sample_files = [name for name in os.listdir(sample_path)
                        if not os.path.isdir(os.path.join(sample_path, name))]
        result = dict()
        for sample_file in sample_files:
            with open(os.path.join(sample_path, sample_file), "r") as f:
                result[sample_file] = f.read()
        return result

    def _get_conf(self, name):
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(self._home, EVENTGEN_CONF_BASE, name, EVENTGEN_CONF_PATH))
        return config

    def _get_replacement_values(self, type, replacement):
        result = list()
        if type == "file" or type == "mvfile":
            key = type+":"+replacement
            if key in self._replacement_cache:
                return key
            with open(replacement.replace("/opt/splunk/etc/apps/SA-Eventgen", self._eventgen_samples_path), "r") as f:
                content = f.read()
                for line in content.split("\n"):
                    result.append(line)
            self._replacement_cache[key] = result
            return key
        return result

    def _get_all_tokens(self, section, config):
        tokens = list()
        for opt in config.options(section):
            if re.match("token\.\d\.token", opt) is not None:
                token = dict()
                token['id'] = opt.split(".")[1]
                token["value"] = config.get(section, opt)
                token['type'] = config.get(
                    section, "token.{}.replacementType".format(token['id']))
                token['replacement'] = config.get(
                    section, "token.{}.replacement".format(token['id']))
                token['replacement_values'] = self._get_replacement_values(
                    token['type'], token['replacement'])
                tokens.append(token)

        return tokens

    def _get_tokens(self, name, sample, config):
        tokens = list()
        for s in config.sections():
            if re.match(s, name) is not None:
                for t in self._get_all_tokens(s, config):
                    tokens.append(t)
        return tokens

    def _get_option(self, name, option, sample, config):
        result = None
        for s in config.sections():
            if re.match(s, name) is not None:
                try:
                    result = config.get(s, option)
                except:
                    pass
        return result

    def _convert_sample(self, name, sample, config):
        result = dict()
        result["name"] = name
        result["pattern"] = list()

        for opt in OPTION_NAMES:
            opt_value = self._get_option(name, opt, sample, config)
            if opt_value is not None:
                result[opt] = opt_value

        tokens = self._get_tokens(name, sample, config)

        for token in tokens:
            for matchObj in re.finditer(token["value"], sample):
                item = dict()
                item["token"] = token
                item["start"] = matchObj.start()
                item["end"] = item["start"] + len(matchObj.group())
                item["value"] = matchObj.group()

                if token["type"] == "random":
                    toreplace = re.findall(token["value"], matchObj.group())
                    if len(toreplace) > 0:
                        item["token"]["value"] = matchObj.group(
                        ).replace(toreplace[0], "@@token@@")
                    else:
                        item["token"]["value"] = "@@token@@"

                result["pattern"].append(item)

        token_starts = [(t["start"], t["end"]) for t in result["pattern"]]
        token_starts_sorted = sorted(token_starts, key=lambda x: x[0])

        for i in range(len(token_starts_sorted) - 1):
            non_token = sample[token_starts_sorted[i]
                               [1]:token_starts_sorted[i + 1][0]]
            item = dict()
            item["start"] = token_starts_sorted[i][1]
            item["end"] = token_starts_sorted[i + 1][0]
            item["value"] = non_token
            result["pattern"].append(item)

        item = dict()
        item["start"] = token_starts_sorted[len(token_starts_sorted) - 1][1]
        item["end"] = len(sample)
        item["value"] = sample[token_starts_sorted[len(
            token_starts_sorted) - 1][1]:]
        result["pattern"].append(item)
        result["pattern"] = sorted(result["pattern"], key=lambda x: x["start"])
        return result

    def convert(self, name):
        result = dict()
        result["name"] = name
        result["patterns"] = list()
        result["replacement"] = self._replacement_cache
        # contain all the samples from eventgen samples
        samples = self._get_samples(name)
        config = self._get_conf(name)

        for k, v in samples.iteritems():
            result["patterns"].append(self._convert_sample(k, v, config))
        return result
