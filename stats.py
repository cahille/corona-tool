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
    'Afghanistan' : 38928346,
    'Albania' : 2877797,
    'Algeria' : 43851044,
    'American Samoa' : 55191,
    'Andorra' : 77265,
    'Angola' : 32866272,
    'Anguilla' : 15003,
    'Antigua and Barbuda' : 97929,
    'Argentina' : 45195774,
    'Armenia' : 2963243,
    'Aruba' : 106766,
    'Australia' : 25499884,
    'Austria' : 9006398,
    'Azerbaijan' : 10139177,
    'Bahamas' : 393244,
    'Bahrain' : 1701575,
    'Bangladesh' : 164689383,
    'Barbados' : 287375,
    'Belarus' : 9449323,
    'Belgium' : 11589623,
    'Belize' : 397628,
    'Benin' : 12123200,
    'Bermuda' : 62278,
    'Bhutan' : 771608,
    'Bolivia' : 11673021,
    'Bosnia and Herzegovina' : 3280819,
    'Botswana' : 2351627,
    'Brazil' : 212559417,
    'British Virgin Islands' : 30231,
    'Brunei' : 437479,
    'Bulgaria' : 6948445,
    'Burkina Faso' : 20903273,
    'Burma' : 54409800,
    'Burundi' : 11890784,
    'Cabo Verde' : 555987,
    'Cambodia' : 16718965,
    'Cameroon' : 26545863,
    'Canada' : 37742154,
    'Caribbean Netherlands' : 26223,
    'Cayman Islands' : 65722,
    'Central African Republic' : 4829767,
    'Chad' : 16425864,
    'Channel Islands' : 173863,
    'Chile' : 19116201,
    'China' : 1439323776,
    'Colombia' : 50882891,
    'Comoros' : 869601,
    'Congo' : 5518087,
    'Congo (Brazzaville)' : 1284609,
    'Congo (Kinshasa)' : 14342000,
    'Cook Islands' : 17564,
    'Costa Rica' : 5094118,
    'Croatia' : 4105267,
    'Cuba' : 11326616,
    'Curacao' : 164093,
    'Cyprus' : 1207359,
    'Czechia' :10708981,
    'Czech Republic (Czechia)' :10708981,
    'Cote d\'Ivoire' : 26378274,
    'Denmark' : 5792202,
    'Diamond Princess' : 2000,
    'Djibouti' : 988000,
    'Dominica' : 71986,
    'Dominican Republic' : 10847910,
    'DR Congo' : 89561403,
    'Ecuador' : 17643054,
    'Egypt' : 102334404,
    'El Salvador' : 6486205,
    'Equatorial Guinea' : 1402985,
    'Eritrea' : 3546421,
    'Estonia' : 1326535,
    'Eswatini' : 1160164,
    'Ethiopia' : 114963588,
    'Faeroe Islands' : 48863,
    'Falkland Islands' : 3480,
    'Fiji' : 896445,
    'Finland' : 5540720,
    'France' : 65273511,
    'French Guiana' : 298682,
    'French Polynesia' : 280908,
    'Gabon' : 2225734,
    'Gambia' : 2416668,
    'Georgia' : 3989167,
    'Germany' : 83783942,
    'Ghana' : 31072940,
    'Gibraltar' : 33691,
    'Greece' : 10423054,
    'Greenland' : 56770,
    'Grenada' : 112523,
    'Guadeloupe' : 400124,
    'Guam' : 168775,
    'Guatemala' : 17915568,
    'Guinea' : 13132795,
    'Guinea-Bissau' : 1968001,
    'Guyana' : 786552,
    'Haiti' : 11402528,
    'Holy See' : 801,
    'Honduras' : 9904607,
    'Hong Kong' : 7496981,
    'Hungary' : 9660351,
    'Iceland' : 341243,
    'India' : 1380004385,
    'Indonesia' : 273523615,
    'Iran' : 83992949,
    'Iraq' : 40222493,
    'Ireland' : 4937786,
    'Isle of Man' : 85033,
    'Israel' : 8655535,
    'Italy' : 60461826,
    'Jamaica' : 2961167,
    'Japan' : 126476461,
    'Jordan' : 10203134,
    'Kazakhstan' : 18776707,
    'Kenya' : 53771296,
    'Kiribati' : 119449,
    'Kosovo' : 1810366,
    'Kuwait' : 4270571,
    'Kyrgyzstan' : 6524195,
    'Laos' : 7275560,
    'Latvia' : 1886198,
    'Lebanon' : 6825445,
    'Lesotho' : 2142249,
    'Liberia' : 5057681,
    'Libya' : 6871292,
    'Liechtenstein' : 38128,
    'Lithuania' : 2722289,
    'Luxembourg' : 625978,
    'MS Zaandam' : 1200,
    'Macao' : 649335,
    'Madagascar' : 27691018,
    'Malawi' : 19129952,
    'Malaysia' : 32365999,
    'Maldives' : 540544,
    'Mali' : 20250833,
    'Malta' : 441543,
    'Marshall Islands' : 59190,
    'Martinique' : 375265,
    'Mauritania' : 4649658,
    'Mauritius' : 1271768,
    'Mayotte' : 272815,
    'Mexico' : 128932753,
    'Micronesia' : 115023,
    'Moldova' : 4033963,
    'Monaco' : 39242,
    'Mongolia' : 3278290,
    'Montenegro' : 628066,
    'Montserrat' : 4992,
    'Morocco' : 36910560,
    'Mozambique' : 31255435,
    'Myanmar' : 54409800,
    'Namibia' : 2540905,
    'Nauru' : 10824,
    'Nepal' : 29136808,
    'Netherlands' : 17134872,
    'New Caledonia' : 285498,
    'New Zealand' : 4822233,
    'Nicaragua' : 6624554,
    'Niger' : 24206644,
    'Nigeria' : 206139589,
    'Niue' : 1626,
    'North Korea' : 25778816,
    'North Macedonia' : 2083374,
    'Northern Mariana Islands' : 57559,
    'Norway' : 5421241,
    'Oman' : 5106626,
    'Pakistan' : 220892340,
    'Palau' : 18094,
    'Panama' : 4314767,
    'Papua New Guinea' : 8947024,
    'Paraguay' : 7132538,
    'Peru' : 32971854,
    'Philippines' : 109581078,
    'Poland' : 37846611,
    'Portugal' : 10196709,
    'Puerto Rico' : 2860853,
    'Qatar' : 2881053,
    'Romania' : 19237691,
    'Russia' : 145934462,
    'Rwanda' : 12952218,
    'Reunion' : 895312,
    'Saint Barthelemy' : 9877,
    'Saint Helena' : 6077,
    'Saint Kitts and Nevis' : 53199,
    'Saint Kitts & Nevis' : 53199,
    'Saint Lucia' : 183627,
    'Saint Martin' : 38666,
    'Saint Pierre and Miquelon' : 5794,
    'Saint Pierre & Miquelon' : 5794,
    'Samoa' : 198414,
    'San Marino' : 33931,
    'Sao Tome and Principe' : 219159,
    'Sao Tome & Principe' : 219159,
    'Saudi Arabia' : 34813871,
    'Senegal' : 16743927,
    'Serbia' : 8737371,
    'Seychelles' : 98347,
    'Sierra Leone' : 7976983,
    'Singapore' : 5850342,
    'Sint Maarten' : 42876,
    'Slovakia' : 5459642,
    'Slovenia' : 2078938,
    'Solomon Islands' : 686884,
    'Somalia' : 15893222,
    'South Africa' : 59308690,
    'South Korea' : 51269185,
    'Korea, South' : 51269185,
    'South Sudan' : 11193725,
    'Spain' : 46754778,
    'Sri Lanka' : 21413249,
    'Saint Vincent and the Grenadines' : 110940,
    'Saint Vincent and Grenadines' : 110940,
    'St. Vincent and Grenadines' : 110940,
    'St. Vincent & Grenadines' : 110940,
    'State of Palestine' : 5101414,
    'Sudan' : 43849260,
    'Suriname' : 586632,
    'Sweden' : 10099265,
    'Switzerland' : 8654622,
    'Syria' : 17500658,
    'Taiwan' : 23816775,
    'Taiwan*' : 23816775,
    'Tajikistan' : 9537645,
    'Tanzania' : 59734218,
    'Thailand' : 69799978,
    'Timor-Leste' : 1318445,
    'Togo' : 8278724,
    'Tokelau' : 1357,
    'Tonga' : 105695,
    'Trinidad and Tobago' : 1399488,
    'Tunisia' : 11818619,
    'Turkey' : 84339067,
    'Turkmenistan' : 6031200,
    'Turks and Caicos' : 38717,
    'Tuvalu' : 11792,
    'U.S. Virgin Islands' : 104425,
    'Uganda' : 45741007,
    'Ukraine' : 43733762,
    'United Arab Emirates' : 9890402,
    'United Kingdom' : 67886011,
    'US' : 331002651,
    'United States' : 331002651,
    'Uruguay' : 3473730,
    'Uzbekistan' : 33469203,
    'Vanuatu' : 307145,
    'Venezuela' : 28435940,
    'Vietnam' : 97338579,
    'Wallis & Futuna' : 11239,
    'West Bank and Gaza' : 5000000,
    'Western Sahara' : 597339,
    'Yemen' : 29825964,
    'Zambia' : 18383955,
    'Zimbabwe' : 14862924
}

parser = argparse.ArgumentParser(
    description='A tool for parsing and attempting find insights in the Johns Hopkins COVID-19 data',
    usage='%(prog)s --countries US Italy --covid-path ~/dev/COVID-19 [--recent-days 1]'
)
parser.add_argument('--covid-path', type=str, help='path to where the COVID repository was cloned')
parser.add_argument('--county', type=bool, nargs='?', help='report on worst counties')
parser.add_argument('--countries', type=str, nargs='+', help='countries to include in by-day report')
parser.add_argument('--recent-days', type=int, nargs='?', help='include this many recent days')
parser.add_argument('--worst-country-count', type=int, nargs='?', help='number of countries to include in the worst list', default=10)
parser.add_argument('--worst-days', type=int, nargs='?', help='number of days to show the worst confirmed and death numberds ')

args = parser.parse_args()

if args.covid_path == None:
    parser.print_help()
    sys.exit()

covid_path = args.covid_path

recent_days = args.recent_days

county = args.county

pp = pprint.PrettyPrinter(indent=4)

def get_per_k(country, number, k):
    if country in populations:
        population = populations[country]
        if population < 1000 * k:
            return None
        ks = population / (k * 1000)
        return number / ks
    else:
        print "Add population for %s" % country
        return None

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

        print
        print 'Worst %s over the last %d days' % (ref['name'].lower(), worst_days)
        print '%35s\t\t%10s\t%11s' % ('Country', ref['name'], 'Per ' + ('Million' if(ref['k'] == 1000) else str(ref['k']) + 'k'))

        for country in ref['dictionary'].keys():
            day_totals = []

            yesterday = 0
            for day in sorted(ref['dictionary'][country].keys(), cmp=my_sort):
                day_total = ref['dictionary'][country][day]

                diff = day_total - yesterday
                day_totals.append(diff)
                yesterday = day_total

            worst_index = worst_days if worst_days < len(day_totals) else len(day_totals)

            totals[country] = sum(day_totals[len(day_totals) - worst_index:len(day_totals)])

        printed = 0

        per_ks = {}

        for country, total in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
            per_k = get_per_k(country, totals[country], ref['k'])

            if per_k != None:
                per_ks[country] = per_k

            if(printed < worst_country_count):
                print "%35s\t\t%10s\t%11s" % (country, totals[country], get_per_k(country, totals[country], ref['k']))
                printed = printed + 1

        print
        print 'Worst %s per/%dk over the last %d days' % (ref['name'], ref['k'], worst_days)

        printed = 0

        for country, per_k in sorted(per_ks.items(), key=lambda kv: kv[1], reverse=True):
            print "%35s\t\t%10s" % (country, per_ks[country])
            printed = printed + 1
            if printed >= worst_country_count:
                break

def populate(path, county=False):
    country_day_hash = {}
    
    with open(path) as csvfile:
        filereader = csv.reader(csvfile)

        headers = None

        for row in filereader:
            match = re.search(", \w\w$", row[0])
            if county:
                pp.pprint(row)
                if match:
                    pp.pprint(row)
                else:
                    continue
            else:
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

#if(county):
#    confirmeds = populate(os.path.join(covid_path, 'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_covid19_confirmed_US.csv'), True)
#    deaths = populate(os.path.join(covid_path,  'csse_covid_19_data', 'csse_covid_19_time_series', 'time_series_covid19_deaths_global.csv'), True)
#
#    pp.pprint(confirmeds)
#    pp.pprint(deaths)
