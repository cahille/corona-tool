# corona-tool
A tool for parsing and attempting find insights in the Johns Hopkins COVID-19 data

You will have to have the Johns Hopkins data local, so clone it somewhere, like ~/dev/COVID-19

```bash {cmd}
git clone https://github.com/CSSEGISandData/COVID-19.git
```

Now clone this code, and see stats as per the following command. Note well, the ```--covid-path``` which should point to where you cloned the Johns Hopkins data.

```bash {cmd}
git clone https://github.com/cahille/corona-tool.git
cd corona-tool
./stats.py --county --recent-days 50 --covid-path ~/dev/COVID-19 --locations US Italy Russia India --worst-days 3
```

    US
        Day        Date        Confirmed    Per 100k    Increase    Deaths        Per Million    Increase
        248        20200925      7034931        2135       50585    203750                619         952
        249        20200926      7079803        2149       44872    204490                621         740
        250        20200927      7116225        2160       36422    204756                622         266
        251        20200928      7149537        2170       33312    205072                623         316
        252        20200929      7191637        2183       42100    205986                626         914
        253        20200930      7233042        2195       41405    206932                628         946
        254        20201001      7277791        2209       44749    207790                631         858
        255        20201002      7332297        2225       54506    208697                634         907
        256        20201003      7382341        2241       50044    209384                636         687
        257        20201004      7417845        2251       35504    209721                637         337
    
    
    Italy
        Day        Date        Confirmed    Per 100k    Increase    Deaths        Per Million    Increase
        239        20200925       306235         507        1912     35801                596          20
        240        20200926       308104         510        1869     35818                596          17
        241        20200927       309870         513        1766     35835                597          17
        242        20200928       311364         515        1494     35851                597          16
        243        20200929       313011         518        1647     35875                597          24
        244        20200930       314861         521        1850     35894                598          19
        245        20201001       317409         525        2548     35918                598          24
        246        20201002       319908         529        2499     35941                599          23
        247        20201003       322751         534        2843     35968                599          27
        248        20201004       325329         538        2578     35986                599          18
    
    
    India
        Day        Date        Confirmed    Per 100k    Increase    Deaths        Per Million    Increase
        240        20200925      5903932         427       85362     93379                 67        1089
        241        20200926      5992532         434       88600     94503                 68        1124
        242        20200927      6074702         440       82170     95542                 69        1039
        243        20200928      6145291         445       70589     96318                 69         776
        244        20200929      6225763         451       80472     97497                 70        1179
        245        20200930      6312584         457       86821     98678                 71        1181
        246        20201001      6394068         463       81484     99773                 72        1095
        247        20201002      6473544         469       79476    100842                 73        1069
        248        20201003      6549373         474       75829    101782                 73         940
        249        20201004      6623815         479       74442    102685                 74         903
    
    
    
    Worst country confirmeds over the last 3 days
                                country        Confirmeds       Per 100k
                                  India            229747             16
                                     US            140054             42
                                 Brazil             68197             32
                         United Kingdom             42844             63
                              Argentina             33484             74
                                 Russia             29405             20
                               Colombia             19713             38
                                Ukraine             13799             31
                                 Mexico             13350             10
                                 Israel             13285            154
    
    Worst country confirmeds per/100k over the last 3 days
                             Montenegro               190
                                 Israel               154
                                Bahamas                95
                                Belgium                79
                                Czechia                76
                                Bahrain                75
                              Argentina                74
                            Netherlands                69
                         United Kingdom                63
                                Moldova                62
    
    Worst country deaths over the last 3 days
                                country            Deaths    Per Million
                                  India              2912              2
                                     US              1931              5
                                 Brazil              1672              7
                                 Mexico              1010              7
                              Argentina               730             16
                                   Iran               577              6
                               Colombia               516             10
                                 Russia               464              3
                              Indonesia               295              1
                                Ecuador               214             12
    
    Worst country deaths per/1000k over the last 3 days
                              Argentina                16
                                Ecuador                12
                                 Israel                12
                               Colombia                10
                                Bolivia                 9
                                 Panama                 9
                                   Oman                 8
                                  Chile                 8
                               Paraguay                 8
                                Armenia                 7
    
    Worst county confirmeds over the last 3 days
                                 county        Confirmeds       Per 100k
                      Harris, Texas, US              4278             91
            Los Angeles, California, US              3194             31
                     Cook, Illinois, US              2229             43
                    Salt Lake, Utah, US              1580            143
                      Collin, Texas, US              1459            145
                     Tarrant, Texas, US              1371             65
                      Clark, Nevada, US              1352             61
                Miami-Dade, Florida, US              1323             49
                         Utah, Utah, US              1074            179
              San Diego, California, US               951             28
    
    Worst county confirmeds per/100k over the last 3 days
               Winnebago, Wisconsin, US               573
               Outagamie, Wisconsin, US               401
                   Houston, Alabama, US               385
                   Brown, Wisconsin, US               328
               Centre, Pennsylvania, US               269
            Minnehaha, South Dakota, US               268
                 Cass, North Dakota, US               262
                   Greene, Missouri, US               254
               Vanderburgh, Indiana, US               254
                Jefferson, Missouri, US               240
    
    Worst county deaths over the last 3 days
                                 county            Deaths    Per Million
                Miami-Dade, Florida, US                50             25
            Los Angeles, California, US                37              3
                     Cook, Illinois, US                27              5
                     Duval, Florida, US                22           None
                     Hidalgo, Texas, US                22           None
            Unassigned, Puerto Rico, US                21           None
                  Maricopa, Arizona, US                21              5
                      Harris, Texas, US                19              4
            Santa Clara, California, US                19             19
                 Orange, California, US                18              6
    
    Worst county deaths per/1000k over the last 3 days
                Miami-Dade, Florida, US                25
            Santa Clara, California, US                19
              Hillsborough, Florida, US                17
                     Franklin, Ohio, US                15
                   Broward, Florida, US                14
                Palm Beach, Florida, US                11
                    Orange, Florida, US                11
             Sacramento, California, US                10
           Middlesex, Massachusetts, US                10
                      Clark, Nevada, US                 7
    

