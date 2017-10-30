#!/usr/bin/env python
# -*- coding: utf-8 -*-


def fitter_jr(items):
    dict_rtn = {}
    for var in items:
        if var["flightNo"] not in dict_rtn:
            # dict_rtn[var["flightNo"]] = var
            dict_rtn[var["flightNo"]] = []
            dict_rtn[var["flightNo"]].append(var)
        else:
            bool_tag = True
            for item in dict_rtn[var["flightNo"]]:
                if var["cabinId"] == item["cabinId"]:
                    bool_tag = False
                    if int(var["price"]) < int(item["price"]):
                        if var["price"] == "99":
                            print "99"
                        item["price"] = var["price"]
            if bool_tag:
                dict_rtn[var["flightNo"]].append(var)
    items = []
    for var_item in dict_rtn:
        for var_info in dict_rtn[var_item]:
            items.append(var_info)
    return items
