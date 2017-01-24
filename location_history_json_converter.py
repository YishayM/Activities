from __future__ import division

import sys
import json
import math
from argparse import ArgumentParser
import argparse
from datetime import datetime

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def dateCheck(timestampms):
    global args
    dt = datetime.fromtimestamp(int(timestampms) / 1000)
    if args.startdate and args.startdate > dt : return False
    if args.enddate and args.enddate < dt : return False
    return True

def convert_json_and_save(path):
    args =[]
    input = path
    output = path[:-5] + "Parsed.json"
    format ='json'

    try:
        json_data = open(input).read()
    except:
        print("Error opening input file")
        return

    try:
        data = json.loads(json_data)
    except:
        print("Error decoding json")
        return

    if "locations" in data and len(data["locations"]) > 0:
        try:
            f_out = open(output, "w")
        except:
            print("Error creating output file for writing")
            return

        items = data["locations"]

        if format == "json":
            f_out.write("{\n")
            f_out.write("  \"data\": {\n")
            f_out.write("    \"items\": [\n")
            first = True

            for item in items:
                if first:
                    first = False
                else:
                    f_out.write(",\n")
                f_out.write("      {\n")
                f_out.write("         \"timestampMs\": %s,\n" % item["timestampMs"])
                f_out.write("         \"latitude\": %s,\n" % (item["latitudeE7"] / 10000000))
                f_out.write("         \"longitude\": %s\n" % (item["longitudeE7"] / 10000000))
                f_out.write("      }")
            f_out.write("\n    ]\n")
            f_out.write("  }\n}")
            if format == "js":
                f_out.write(";")




        f_out.close()

    else:
        print("No data found in json")
        return

