#!/usr/bin/python

import argparse
import csv
import operator
import os
import pprint
import re
import sys

parser = argparse.ArgumentParser(
    description='A tool for parsing and attempting find insights in the Johns Hopkins COVID-19 data',
    usage='%(prog)s --countries US Italy --covid-path ~/dev/COVID-19 [--recent-days 1]'
)
parser.add_argument('--covid-path', type=str, nargs=1, help='path to where the COVID repository was cloned')
parser.add_argument('--countries', type=str, nargs='+', help='countries to include in by-day report')
parser.add_argument('--recent-days', type=int, nargs='?', help='include this many recent days')
parser.add_argument('--worst-country-count', type=int, nargs='?', help='number of countries to include in the worst list', default=10)
parser.add_argument('--worst-days', type=int, nargs='?', help='number of days to show the worst confirmed and death numberds ')

args = parser.parse_args()

if args.covid_path == None:
    parser.print_help()
    sys.exit()

covid_path = args.covid_path[0]

recent_days = args.recent_days

pp = pprint.PrettyPrinter(indent=4)

def worst_func(confirmeds, deaths, worst_day, worst_country_count):

    for ref in [
        {
            'dictionary' : confirmeds,
            'name'       : 'confirmeds'
        },
        {
            'dictionary' : deaths,
            'name'       : 'deaths'
        }
    ]:
        totals = {}

        print 'worst %s over the last %d days' % (ref['name'], worst_days)

        for country in ref['dictionary'].keys():
            day_totals = []

            yesterday = 0
            for day in sorted(ref['dictionary'][country].keys(), cmp=my_sort):
                day_total = ref['dictionary'][country][day]
                diff = day_total - yesterday
                day_totals.append(diff)
                yesterday = day_total

            totals[country] = sum(day_totals[len(day_totals) - worst_days:len(day_totals)])

        printed = 0
        for country, total in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
            print "%s -> %s" % (country, totals[country])
            printed = printed + 1
            if(printed > worst_country_count):
                break

        print

def populate(path):
    country_day_hash = {}
    
    with open(path) as csvfile:
        filereader = csv.reader(csvfile)

        headers = None

        for row in filereader:
            match = re.search(", \w\w$", row[0])
            if match:
                continue

            if headers == None:
                headers = {}
                for i in range(0,  (len(row) - 1)):
                    headers[i] = row[i]
            else:
                country  = row[1]

                for i in range(4, (len(row) - 1)):
                    this_day = headers[i]
                    day_total = row[i]

                    if country not in country_day_hash:
                        country_hash = {}
                        country_day_hash[country] = country_hash

                    if this_day not in country_day_hash[country]:
                        country_day_hash[country][this_day] = 0

                    country_day_hash[country][this_day] = int(country_day_hash[country][this_day]) + int(row[i])

    return country_day_hash

def my_sort(a, b):
   a_values = a.split('/')
   b_values = b.split('/')

   return int(a_values[2]) - int(b_values[2]) or int(a_values[0]) - int(b_values[0]) or int(a_values[1]) - int(b_values[1])

def show_country(country, confirmed, deaths):
    print country + "\n\tDay\t\t%-8s\t%9s\t%8s\t%6s\t\t%8s" % ("Date", "Confirmed", "Increase", "Deaths", "Increase")

    yesterday_deaths = 0;
    yesterday_confirmeds = 0;
    days = 0;

    day_strings = []

    for day in sorted(confirmed[country].keys(), cmp=my_sort):
        confirmed_today_total = confirmed[country][day]

        if not confirmed_today_total:
            continue

        death_today_total = deaths[country][day]

        days = days + 1

        death_diff = (death_today_total - yesterday_deaths) if death_today_total else 0
        confirmed_diff = confirmed_today_total - yesterday_confirmeds

        day_strings.append("\t%3s\t\t%8s\t%9s\t%8s\t%6s\t\t%8s" % (days, day, confirmed_today_total, confirmed_diff, death_today_total, death_diff))

        yesterday_confirmeds = confirmed_today_total;
        yesterday_deaths = death_today_total;

    if(recent_days != None and len(day_strings) > recent_days):
        day_strings = day_strings[len(day_strings) - recent_days:len(day_strings)]

    for day_string in day_strings:
        print day_string

    print "\n"

    
confirmeds = populate(os.path.join(covid_path, 'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_19-covid-Confirmed.csv'))
deaths = populate(os.path.join(covid_path,  'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_19-covid-Deaths.csv'))

for country in args.countries:
    show_country(country, confirmeds, deaths)

worst_days = args.worst_days
worst_country_count = args.worst_country_count

if(worst_days != None):
    worst_func(confirmeds, deaths, worst_days, worst_country_count)
