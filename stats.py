#!/usr/bin/python

import argparse
import csv
import operator
import os
import pprint
import re
import sys

# populations from https://www.worldometers.info/world-population/population-by-country/
# as of March 30, 2020

populations = {
    'Australia'          : 25499884,
    'Austria'            : 9006398,
    'Belgium'            : 11589623,
    'Brazil'             : 212559417,
    'Canada'             : 37742154,
    'Chile'              : 19116201,
    'China'              : 1439323776,
    'Denmark'            : 5792202,
    'Dominican Republic' : 10847910, 
    'Ecuador'            : 17643054,
    'France'             : 65273511,
    'Germany'            : 83783942,
    'Greece'             : 10423054,
    'Indonesia'          : 273523615,
    'Iran'               : 83992949,
    'Ireland'            : 4937786,
    'Israel'             : 8655535,
    'Italy'              : 60461826,
    'Korea, South'       : 51269185,
    'Malaysia'           : 32365999,
    'Netherlands'        : 17134872,
    'Norway'             : 5421241,
    'Philippines'        : 109581078,
    'Poland'             : 37846611,
    'Portugal'           : 10196709,
    'Romania'            : 19237691,
    'Russia'             : 145934462,
    'Spain'              : 46754778,
    'Sweden'             : 10099265,
    'Switzerland'        : 8654622,
    'Turkey'             : 84339067,
    'US'                 : 331002651,
    'United Kingdom'     : 67886011
}

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

def get_per_k(country, number, k):
    population = populations[country]
    ks = population / (k * 1000)
    return number / ks

def worst_func(confirmeds, deaths, worst_day, worst_country_count):

    for ref in [
        {
            'dictionary' : confirmeds,
            'k'          : 100,
            'name'       : 'Confirmeds'
        },
        {
            'dictionary' : deaths,
            'k'          : 1000,
            'name'       : 'Deaths'
        }
    ]:
        totals = {}

        print 'Worst %s over the last %d days' % (ref['name'].lower(), worst_days)
        print '%20s\t\t%10s\t%11s' % ('Country', ref['name'], 'Per ' + ('Million' if(ref['k'] == 1000) else str(ref['k']) + 'k'))

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
            print "%20s\t\t%10s\t%11s" % (country, totals[country], get_per_k(country, totals[country], ref['k']))
            printed = printed + 1
            if(printed >= worst_country_count):
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
    print country + "\n\tDay\t\t%-8s\t%9s\t%8s\t%8s\t%6s\t\t%11s\t%8s" % ("Date", "Confirmed", "Per 100k", "Increase", "Deaths", "Per Million", "Increase")

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

        day_strings.append("\t%3s\t\t%8s\t%9s\t%8s\t%8s\t%6s\t\t%11s\t%8s" % (days, day, confirmed_today_total, get_per_k(country, confirmed_today_total, 100), confirmed_diff, death_today_total, get_per_k(country, death_today_total, 1000), death_diff))

        yesterday_confirmeds = confirmed_today_total;
        yesterday_deaths = death_today_total;

    if(recent_days != None and len(day_strings) > recent_days):
        day_strings = day_strings[len(day_strings) - recent_days:len(day_strings)]

    for day_string in day_strings:
        print day_string

    print "\n"

    
confirmeds = populate(os.path.join(covid_path, 'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_covid19_confirmed_global.csv'))
deaths = populate(os.path.join(covid_path,  'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_covid19_deaths_global.csv'))

for country in args.countries:
    show_country(country, confirmeds, deaths)

worst_days = args.worst_days
worst_country_count = args.worst_country_count

if(worst_days != None):
    worst_func(confirmeds, deaths, worst_days, worst_country_count)
