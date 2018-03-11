#!/usr/bin/env python3
from datetime import timedelta
from fitparse import FitFile
import pytz

MAX_HEART_RATE = 190


def semicircles_to_degrees(pos):
    if pos is None:
        return None
    return pos * (180 / pow(2, 31))


def m_per_s_to_min_per_km(mps):
    if mps == 0 or mps is None:
        return 0
    return 100 / (6 * mps)


def get_structured_activity(fitfile):
    sn = list(fitfile.get_messages("file_id"))[0].as_dict()['fields'][0]
    raw_session = list(fitfile.get_messages("session"))[0].as_dict()['fields']
    session_fields = [
        "timestamp",
        "start_time",
        "start_position_lat",
        "start_position_long",
        "end_position_lat",
        "end_position_long",
        "total_elapsed_time",
        "total_timer_time",
        "total_distance",
        "total_calories",
        "avg_speed",
        "max_speed",
        "total_ascent",
        "total_descent",
        "num_laps",
        "sport",
        "avg_heart_rate",
        "max_heart_rate"
    ]
    session = {"serial_number": sn}
    for f in raw_session:
        if f['name'] in session_fields:
            if str(f['units']).lower() == "semicircles":
                session[f['name']] = {
                    'unit': "deg", 'value': semicircles_to_degrees(f['value'])}
            elif str(f['units']).lower() == "m/s":
                session[f['name']] = {
                    'unit': "min/km", 'value': m_per_s_to_min_per_km(f['value'])}
            else:
                session[f['name']] = {'unit': f['units'], 'value': f['value']}

    lap_fields = [
        "timestamp",
        "start_time",
        "start_position_lat",
        "start_position_long",
        "end_position_lat",
        "end_position_long",
        "total_elapsed_time",
        "total_timer_time",
        "total_distance",
        "total_calories",
        "avg_speed",
        "max_speed",
        "total_ascent",
        "total_descent",
        "avg_heart_rate",
        "max_heart_rate",
        "lap_trigger",
    ]
    laps = []
    for record in fitfile.get_messages("lap"):
        lap = {"activities": {"value": [], "unit": None}}
        for f in record.as_dict()['fields']:
            if f['name'] in lap_fields:
                if str(f['units']).lower() == "semicircles":
                    lap[f['name']] = {
                        'unit': "deg", 'value': semicircles_to_degrees(f['value'])}
                elif str(f['units']).lower() == "m/s":
                    lap[f['name']] = {
                        'unit': "min/km", 'value': m_per_s_to_min_per_km(f['value'])}
                else:
                    lap[f['name']] = {'unit': f['units'], 'value': f['value']}
        lap["end_time"] = {
            "value": lap["start_time"]["value"] + timedelta(seconds=int(lap["total_elapsed_time"]["value"])),
            "unit": None}
        laps.append(lap)
    session['laps'] = laps

    record_fields = [
        "timestamp",
        "position_lat",
        "position_long",
        "distance",
        "altitude",
        "speed",
        "heart_rate",
    ]

    records = []
    for record in fitfile.get_messages("record"):
        point = {}
        for f in record.as_dict()['fields']:
            if f['name'] in record_fields:
                if str(f['units']).lower() == "semicircles":
                    point[f['name']] = {
                        'unit': "deg", 'value': semicircles_to_degrees(f['value'])}
                elif str(f['units']).lower() == "m/s":
                    point[f['name']] = {
                        'unit': "min/km", 'value': m_per_s_to_min_per_km(f['value'])}
                else:
                    point[f['name']] = {'unit': f['units'], 'value': f['value']}
        records.append(point)

    session['data'] = records

    # Make time fields timezone aware
    time_fields = [
        "timestamp",
        "start_time",
        "end_time",
    ]
    for f in time_fields:
        try:
            session[f]['value'] = session[f]['value'].replace(tzinfo=pytz.utc)
        except KeyError:
            pass
    for lap in session['laps']:
        for f in time_fields:
            try:
                lap[f]['value'] = lap[f]['value'].replace(tzinfo=pytz.utc)
            except KeyError:
                pass
    for data in session['data']:
        for f in time_fields:
            try:
                data[f]['value'] = data[f]['value'].replace(tzinfo=pytz.utc)
            except KeyError:
                pass
    return session


def clean_data(activity):
    sum_heart_rate = 0
    heart_rate_count = 0
    activity['max_heart_rate_clock'] = {"unit": "bmp", "value": activity['max_heart_rate']['value']}
    activity['avg_heart_rate_clock'] = {"unit": "bmp", "value": activity['avg_heart_rate']['value']}
    try:
        if activity['max_heart_rate']['value'] > MAX_HEART_RATE:
            activity['max_heart_rate']['value'] = 0
    except TypeError:
        pass
    for d in activity['data']:
        try:
            if d['heart_rate']['value'] > MAX_HEART_RATE:
                d['heart_rate']['value'] = None
            else:
                sum_heart_rate += d['heart_rate']['value']
                heart_rate_count += 1
        except KeyError:
            pass
        except TypeError:
            pass
        for l in activity['laps']:
            if l['end_time']['value'] > d["timestamp"]["value"] > l["start_time"]["value"]:
                l["activities"]["value"].append(d)
    try:
        activity['avg_heart_rate'] = {"unit": "bmp", "value": round(sum_heart_rate / heart_rate_count, 0)}
    except ZeroDivisionError:
        activity['avg_heart_rate'] = {"unit": "bmp", "value": 0}

    for l in activity['laps']:
        l['max_heart_rate_clock'] = {"unit": "bmp", "value": l['max_heart_rate']['value']}
        l['avg_heart_rate_clock'] = {"unit": "bmp", "value": l['avg_heart_rate']['value']}
        try:
            if l['max_heart_rate']['value'] > MAX_HEART_RATE:
                l['max_heart_rate']['value'] = None
            else:
                activity['max_heart_rate']['value'] = max(activity['max_heart_rate']['value'], l['max_heart_rate']['value'])
        except KeyError:
            pass
        except TypeError:
            pass
        max_heart_rate_lap = 0
        sum_heart_rate_lap = 0
        heart_rate_count_lap = 0
        for d in l["activities"]["value"]:
            try:
                if d['heart_rate']['value']:
                    max_heart_rate_lap = max(max_heart_rate_lap, d['heart_rate']['value'])
                    sum_heart_rate_lap += d['heart_rate']['value']
                    heart_rate_count_lap += 1
            except KeyError:
                pass
        del l["activities"]
        try:
            l['avg_heart_rate'] = {"unit": "bmp", "value": round(sum_heart_rate_lap / heart_rate_count_lap, 0)}
            l['max_heart_rate'] = {"unit": "bmp", "value": max_heart_rate_lap}
        except ZeroDivisionError:
            l['avg_heart_rate'] = {"unit": "bmp", "value": 0}


def convert(fit_file):
    file = FitFile(fit_file)
    activity = get_structured_activity(file)
    clean_data(activity)
    return activity


def strip_units(activity):
    new_activity = {k: v['value'] for k, v in activity.items() if type(v) != list}
    new_activity['laps'] = []
    new_activity['data'] = []
    for lap in activity['laps']:
        new_activity['laps'].append({k: v['value'] for k, v in lap.items()})
    for data in activity['data']:
        new_activity['data'].append({k: v['value'] for k, v in data.items()})
    return new_activity
