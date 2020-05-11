#!/usr/bin/python

import argparse
import csv
import operator
import os
import pprint
import re
import sys

# populations from https://www.worldometers.info/world-population/population-by-country/

populations = {}

parser = argparse.ArgumentParser(
    description='A tool for parsing and attempting find insights in the Johns Hopkins COVID-19 data. --covid-path should point to where you cloned the Johns Hopkins COVID-19 repo',
    usage='%(prog)s --county --recent-days 3 --covid-path ~/dev/COVID-19 --locations US Italy Russia --worst-days 3'
)
parser.add_argument('--covid-path', type=str, help='path to where the COVID repository was cloned')
parser.add_argument('--county', action='store_true', help='report on worst counties')
parser.add_argument('--locations', type=str, nargs='+', help='locations to include in by-day report')
parser.add_argument('--recent-days', type=int, nargs='?', help='include this many recent days')
parser.add_argument('--worst-location-count', type=int, nargs='?', help='number of locations to include in the worst list', default=10)
parser.add_argument('--worst-days', type=int, nargs='?', help='number of days to show the worst confirmed and death numberds ')

args = parser.parse_args()

if args.covid_path == None:
    parser.print_help()
    sys.exit()

covid_path = args.covid_path

recent_days = args.recent_days

county = args.county

pp = pprint.PrettyPrinter(indent=4)

def populate_location_populations():
    country_lookup_table_path = os.path.join(covid_path,  'csse_covid_19_data', 'UID_ISO_FIPS_LookUp_Table.csv')

    skip = True

    with open(country_lookup_table_path) as csvfile:
        filereader = csv.reader(csvfile)
        for row in filereader:
            if skip:
                skip = False
                continue

            location   = row[10]
            population = row[11]
            
            if len(population) == 0:
                continue

            populations[location] = population

def get_per_k(location, number, k):
    if location in populations:
        population = int(populations[location])

        if population < 1000 * k:
            return None
        ks = population / (k * 1000)
        return number / ks
    else:
        if location not in ['Diamond Princess', 'MS Zaandam']:
            print "Add population for %s" % location
        return None

def worst_func(confirmeds, deaths, worst_day, worst_location_count, county):

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

        location_type = 'county' if county else 'country'

        print
        print 'Worst %s %s over the last %d days' % (location_type, ref['name'].lower(), worst_days)
        print '%35s\t\t%10s\t%11s' % (location_type, ref['name'], 'Per ' + ('Million' if(ref['k'] == 1000) else str(ref['k']) + 'k'))

        for location in ref['dictionary'].keys():
            day_totals = []

            yesterday = 0
            for day in sorted(ref['dictionary'][location].keys()):
                day_total = ref['dictionary'][location][day]

                diff = day_total - yesterday
                day_totals.append(diff)
                yesterday = day_total

            worst_index = worst_days if worst_days < len(day_totals) else len(day_totals)

            totals[location] = sum(day_totals[len(day_totals) - worst_index:len(day_totals)])

        printed = 0

        per_ks = {}

        for location, total in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
            per_k = get_per_k(location, totals[location], ref['k'])

            if per_k != None:
                per_ks[location] = per_k

            if(printed < worst_location_count):
                print "%35s\t\t%10s\t%11s" % (location, totals[location], get_per_k(location, totals[location], ref['k']))
                printed = printed + 1

        print
        print 'Worst %s %s per/%dk over the last %d days' % (location_type, ref['name'].lower(), ref['k'], worst_days)

        printed = 0

        for location, per_k in sorted(per_ks.items(), key=lambda kv: kv[1], reverse=True):
            print "%35s\t\t%10s" % (location, per_ks[location])
            printed = printed + 1
            if printed >= worst_location_count:
                break

def populate(path, county=False):
    location_day_hash = {}
    
    with open(path) as csvfile:
        filereader = csv.reader(csvfile)

        headers = None

        for row in filereader:
            if headers == None:
                headers = {}
                for i in range(0,  (len(row) - 1)):
                    match = re.search("^(\d{1,2})/(\d{1,2})/(\d{2})$", row[i])
                    if match:
                        month = match.group(1)
                        day   = match.group(2)
                        year  = match.group(3)
                        key   = str(2000 + int(year)) + str(month if len(month) == 2 else '0' + month) + str(day if len(day) == 2 else '0' + day)
                        headers[i] = key
                    else:
                        headers[i] = row[i]
                exit
                continue

            match = re.search(", \w\w$", row[10])

            if county:
                if not match:
                    continue
            else:
                if match:
                    print('skipping')
                    continue


            location = row[10] if county else row[1]

            initial_i = None

            if county:
                if 'deaths' in path:
                    initial_i = 12
                    populations[location] = row[11]
                else:
                    initial_i = 11
            else:
                initial_i = 4

            for i in range(initial_i, (len(row) - 1)):
                this_day = headers[i]
                day_total = row[i]

                if location not in location_day_hash:
                    location_hash = {}
                    location_day_hash[location] = location_hash

                if this_day not in location_day_hash[location]:
                    location_day_hash[location][this_day] = 0

                location_day_hash[location][this_day] = int(location_day_hash[location][this_day]) + int(row[i])

    return location_day_hash

def show_location(location, confirmed, deaths):
    print location + "\n\tDay\t\t%-8s\t%9s\t%8s\t%8s\t%6s\t\t%11s\t%8s" % ("Date", "Confirmed", "Per 100k", "Increase", "Deaths", "Per Million", "Increase")

    yesterday_deaths = 0;
    yesterday_confirmeds = 0;
    days = 0;

    day_strings = []

    for day in sorted(confirmed[location].keys()):
        confirmed_today_total = confirmed[location][day]

        if not confirmed_today_total:
            continue

        death_today_total = deaths[location][day]

        days = days + 1

        death_diff = (death_today_total - yesterday_deaths) if death_today_total else 0
        confirmed_diff = confirmed_today_total - yesterday_confirmeds

        day_strings.append("\t%3s\t\t%8s\t%9s\t%8s\t%8s\t%6s\t\t%11s\t%8s" % (days, day, confirmed_today_total, get_per_k(location, confirmed_today_total, 100), confirmed_diff, death_today_total, get_per_k(location, death_today_total, 1000), death_diff))

        yesterday_confirmeds = confirmed_today_total;
        yesterday_deaths = death_today_total;

    if(recent_days != None and len(day_strings) > recent_days):
        day_strings = day_strings[len(day_strings) - recent_days:len(day_strings)]

    for day_string in day_strings:
        print day_string

    print "\n"

    
populate_location_populations()

confirmeds = populate(os.path.join(covid_path, 'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_covid19_confirmed_global.csv'))
deaths = populate(os.path.join(covid_path,  'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_covid19_deaths_global.csv'))

for location in args.locations:
    show_location(location, confirmeds, deaths)

worst_days = args.worst_days
worst_location_count = args.worst_location_count

if(worst_days != None):
    worst_func(confirmeds, deaths, worst_days, worst_location_count, False)

if(county):
    confirmeds = populate(os.path.join(covid_path, 'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_covid19_confirmed_US.csv'), True)
    deaths = populate(os.path.join(covid_path,  'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_covid19_deaths_US.csv'), True)

    if(worst_days != None):
        worst_func(confirmeds, deaths, worst_days, worst_location_count, True)
