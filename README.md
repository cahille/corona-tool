# corona-tool
A tool for parsing and attempting find insights in the Johns Hopkins COVID-19 data

You will have to have the Johns Hopkins data local, so clone it somewhere, like ~/dev/COVID-19

```bash {cmd}
git clone https://github.com/CSSEGISandData/COVID-19.git
```

Now clone this code, and see stats as per the following command

```bash {cmd}
git clone https://github.com/cahille/corona-tool.git
cd corona-tool
./stats.py --countries US Italy China --covid-path ~/dev/COVID-19 --recent-days 5
```

US
	Day		Date    	Confirmed	Increase	Deaths		Increase
	 23		 3/17/20	     6421	    1789	   108		      23
	 24		 3/18/20	     7783	    1362	   118		      10
	 25		 3/19/20	    13677	    5894	   200		      82
	 26		 3/20/20	    19100	    5423	   244		      44
	 27		 3/21/20	    25489	    6389	   307		      63


Italy
	Day		Date    	Confirmed	Increase	Deaths		Increase
	 47		 3/17/20	    31506	    3526	  2503		     345
	 48		 3/18/20	    35713	    4207	  2978		     475
	 49		 3/19/20	    41035	    5322	  3405		     427
	 50		 3/20/20	    47021	    5986	  4032		     627
	 51		 3/21/20	    53578	    6557	  4825		     793


China
	Day		Date    	Confirmed	Increase	Deaths		Increase
	 56		 3/17/20	    81058	      25	  3230		      13
	 57		 3/18/20	    81102	      44	  3241		      11
	 58		 3/19/20	    81156	      54	  3249		       8
	 59		 3/20/20	    81250	      94	  3253		       4
	 60		 3/21/20	    81305	      55	  3259		       6
