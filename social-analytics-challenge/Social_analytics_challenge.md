

```python
# Dependencies
import tweepy
import json
import numpy as np
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt

#Get key values from config file
from config import consumer_key
from config import consumer_secret
from config import access_token
from config import access_token_secret

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

```


```python

#List of news outlets
news_outlets = ("@BBCNews", "@CBSNews", "@CNN",
                "@FoxNews", "@nytimes")

#Initialize master dataframe
master_df = pd.DataFrame()

#Loop through each news outlet and get tweets
for news_outlet in news_outlets:
    #Initialize largest id and counter
    largest_id = None
    tweet_counter = 0
    
    #Arrays to hold tweets, sentiments, counter
    tweet_text = []
    tweet_created = []
    tweets_ago = []
    compound = []
    pos = []
    neg = []
    neu = []
    
    #Be patient
    time.sleep(5)
    
    #Loop through pages of tweets
    for page in tweepy.Cursor(api.search, q=news_outlet, count=25, result_type = 'recent', max_id = largest_id).pages(4):

        if not largest_id:
            largest_id = page[0].id #this is the ID of the tweet
            
        #Loop through tweets on a page
        for tweet in page:
            #Set and increment counter
            tweets_ago.append(tweet_counter)
            tweet_counter +=1
            
            #Get tweet text
            tweet = tweet._json
            target_text = tweet['text']
            #Append to list
            tweet_text.append(target_text)
            
            #Get tweet created date time
            converted_datetime = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y')
            #Convert and append to list
            tweet_created.append(converted_datetime.strftime('%Y-%d-%m %H:%M:%S'))

            #  Run Vader Analysis on each tweet and populate arrays
            vader = analyzer.polarity_scores(target_text)

            compound.append(vader["compound"])
            pos.append(vader["pos"])
            neu.append(vader["neu"])
            neg.append(vader["neg"])

    # Create dataframe with tweets and sentiment analyses
    df = pd.DataFrame({'source_account':news_outlet, 'text' :tweet_text, 'tweets_ago': tweets_ago, 'date' :tweet_created, 'compound':compound, 'pos':pos, 'neg':neg, 'neu':neu})
    #Add to master dataframe
    master_df = master_df.append(df)
    
    #Display master dataframe
    print(master_df)

        





```

        compound                 date    neg    neu    pos source_account  \
    0    -0.4019  2018-29-03 04:12:30  0.130  0.870  0.000       @BBCNews   
    1     0.4215  2018-29-03 04:11:39  0.000  0.865  0.135       @BBCNews   
    2     0.0000  2018-29-03 04:11:32  0.000  1.000  0.000       @BBCNews   
    3     0.3818  2018-29-03 04:11:13  0.000  0.885  0.115       @BBCNews   
    4    -0.7096  2018-29-03 04:11:10  0.290  0.710  0.000       @BBCNews   
    5     0.0000  2018-29-03 04:11:08  0.000  1.000  0.000       @BBCNews   
    6     0.0000  2018-29-03 04:10:33  0.000  1.000  0.000       @BBCNews   
    7     0.3400  2018-29-03 04:10:25  0.056  0.833  0.111       @BBCNews   
    8     0.0000  2018-29-03 04:10:24  0.000  1.000  0.000       @BBCNews   
    9     0.0000  2018-29-03 04:10:11  0.000  1.000  0.000       @BBCNews   
    10    0.0000  2018-29-03 04:09:59  0.000  1.000  0.000       @BBCNews   
    11   -0.1779  2018-29-03 04:09:51  0.133  0.763  0.104       @BBCNews   
    12    0.4767  2018-29-03 04:09:48  0.077  0.737  0.186       @BBCNews   
    13   -0.6908  2018-29-03 04:09:38  0.170  0.830  0.000       @BBCNews   
    14    0.1531  2018-29-03 04:09:38  0.085  0.793  0.122       @BBCNews   
    15    0.0000  2018-29-03 04:09:33  0.000  1.000  0.000       @BBCNews   
    16   -0.6908  2018-29-03 04:08:17  0.170  0.830  0.000       @BBCNews   
    17    0.2960  2018-29-03 04:08:17  0.045  0.861  0.094       @BBCNews   
    18   -0.6908  2018-29-03 04:07:37  0.170  0.830  0.000       @BBCNews   
    19   -0.6908  2018-29-03 04:06:59  0.170  0.830  0.000       @BBCNews   
    20   -0.7003  2018-29-03 04:06:32  0.195  0.805  0.000       @BBCNews   
    21    0.0000  2018-29-03 04:06:29  0.000  1.000  0.000       @BBCNews   
    22    0.1531  2018-29-03 04:06:16  0.062  0.848  0.089       @BBCNews   
    23    0.2732  2018-29-03 04:05:17  0.000  0.811  0.189       @BBCNews   
    24    0.0000  2018-29-03 04:05:11  0.000  1.000  0.000       @BBCNews   
    25    0.0000  2018-29-03 04:05:04  0.000  1.000  0.000       @BBCNews   
    26   -0.2023  2018-29-03 04:04:59  0.184  0.816  0.000       @BBCNews   
    27   -0.6808  2018-29-03 04:04:55  0.204  0.796  0.000       @BBCNews   
    28    0.2960  2018-29-03 04:03:20  0.083  0.793  0.124       @BBCNews   
    29   -0.6705  2018-29-03 04:02:22  0.271  0.586  0.143       @BBCNews   
    ..       ...                  ...    ...    ...    ...            ...   
    70    0.0000  2018-29-03 03:45:31  0.000  1.000  0.000       @BBCNews   
    71    0.0000  2018-29-03 03:45:06  0.000  1.000  0.000       @BBCNews   
    72    0.5918  2018-29-03 03:44:52  0.156  0.567  0.277       @BBCNews   
    73    0.0000  2018-29-03 03:44:05  0.000  1.000  0.000       @BBCNews   
    74   -0.6908  2018-29-03 03:42:37  0.170  0.830  0.000       @BBCNews   
    75    0.0000  2018-29-03 03:42:35  0.000  1.000  0.000       @BBCNews   
    76   -0.6908  2018-29-03 03:42:12  0.170  0.830  0.000       @BBCNews   
    77    0.0000  2018-29-03 03:41:21  0.000  1.000  0.000       @BBCNews   
    78    0.0000  2018-29-03 03:39:52  0.000  1.000  0.000       @BBCNews   
    79   -0.6908  2018-29-03 03:39:47  0.170  0.830  0.000       @BBCNews   
    80   -0.6908  2018-29-03 03:39:41  0.170  0.830  0.000       @BBCNews   
    81   -0.6908  2018-29-03 03:39:41  0.170  0.830  0.000       @BBCNews   
    82    0.1695  2018-29-03 03:38:43  0.000  0.919  0.081       @BBCNews   
    83    0.0000  2018-29-03 03:38:24  0.000  1.000  0.000       @BBCNews   
    84    0.0000  2018-29-03 03:38:07  0.000  1.000  0.000       @BBCNews   
    85    0.0000  2018-29-03 03:38:04  0.000  1.000  0.000       @BBCNews   
    86    0.0000  2018-29-03 03:38:01  0.000  1.000  0.000       @BBCNews   
    87   -0.5574  2018-29-03 03:38:00  0.159  0.841  0.000       @BBCNews   
    88    0.0000  2018-29-03 03:37:57  0.000  1.000  0.000       @BBCNews   
    89    0.0000  2018-29-03 03:37:43  0.000  1.000  0.000       @BBCNews   
    90   -0.1553  2018-29-03 03:37:28  0.130  0.761  0.108       @BBCNews   
    91    0.4215  2018-29-03 03:37:11  0.000  0.865  0.135       @BBCNews   
    92   -0.6908  2018-29-03 03:36:20  0.170  0.830  0.000       @BBCNews   
    93    0.0000  2018-29-03 03:36:03  0.000  1.000  0.000       @BBCNews   
    94   -0.2732  2018-29-03 03:35:42  0.160  0.840  0.000       @BBCNews   
    95   -0.4939  2018-29-03 03:35:11  0.106  0.894  0.000       @BBCNews   
    96   -0.5106  2018-29-03 03:34:25  0.148  0.852  0.000       @BBCNews   
    97    0.4019  2018-29-03 03:34:16  0.000  0.828  0.172       @BBCNews   
    98   -0.6908  2018-29-03 03:34:09  0.170  0.830  0.000       @BBCNews   
    99    0.0000  2018-29-03 03:32:56  0.000  1.000  0.000       @BBCNews   
    
                                                     text  tweets_ago  
    0   RT @elise_tallaron: @BenPBradshaw @BestForBrit...           0  
    1   @BBCNews that article will show why im against...           1  
    2   RT @NewPlasticsEcon: Deposit return schemes we...           2  
    3   RT @VeroVero777: @DameWritesalot @BenPBradshaw...           3  
    4   RT @BBCNews: John Worboys: Court to rule on bl...           4  
    5   RT @joannaccherry: Is it just me or do @BBCNew...           5  
    6   RT @atmphillips: @ChristopherJor5 @Remain_Labo...           6  
    7   RT @Siemens: #AI, #BigData &amp; #Cloud techno...           7  
    8   RT @eloisetodd: Sticky tape in the pocket of a...           8  
    9   RT @ChristopherJor5: @BenPBradshaw @Remain_Lab...           9  
    10  RT @SatbirLSingh: - Theresa May has swapped he...          10  
    11  RT @iandonald_psych: Why is @theresa_may faili...          11  
    12  RT @BenPBradshaw: Dear @BBCNews All your trail...          12  
    13  RT @KTHopkins: If 100 Pakistani Muslim men rap...          13  
    14  @BBCNews you cant tell people we ,pay 6 billio...          14  
    15  RT @SandraDunn1955: @BBC @BBC_Joe_Lynam @BBCBr...          15  
    16  RT @KTHopkins: If 100 Pakistani Muslim men rap...          16  
    17  RT @tommyptoronto: For my entire life the BBC ...          17  
    18  RT @KTHopkins: If 100 Pakistani Muslim men rap...          18  
    19  RT @KTHopkins: If 100 Pakistani Muslim men rap...          19  
    20  RT @reb_les: This is where we are at today.\nT...          20  
    21                         @BBCNews alohg these lines          21  
    22  @BBCNews goverment aid is also called foreign ...          22  
    23  @ianmack2 @BBCNews @hendopolis Well get jumpin...          23  
    24  RT @joannaccherry: Is it just me or do @BBCNew...          24  
    25      @BBCNews In other words....too many patients.          25  
    26  RT @BBCNews: Hatton Garden heist: Man, 57, cha...          26  
    27  @BBCNews hey mofos, your Brits girls are raped...          27  
    28  RT @pleaseuseaussie: #auspol If you are PC inc...          28  
    29  RT @Greekboy8: OH LOOK, @UKLabour support surg...          29  
    ..                                                ...         ...  
    70  @BBCNews Or to put it another way, we have ple...          70  
    71  RT @Imamofpeace: Is there a city in Pakistan c...          71  
    72  #bbchardtalk wow that presenter, the blond guy...          72  
    73  RT @BBCNews: Musicians hit by management fee '...          73  
    74  RT @KTHopkins: If 100 Pakistani Muslim men rap...          74  
    75  RT @BBCNews: MPs to probe Russian money launde...          75  
    76  RT @KTHopkins: If 100 Pakistani Muslim men rap...          76  
    77  RT @Uhorzum09: DELİLLERİ NEDEN SADECE BEN BULU...          77  
    78  RT @Imamofpeace: Is there a city in Pakistan c...          78  
    79  RT @KTHopkins: If 100 Pakistani Muslim men rap...          79  
    80  RT @KTHopkins: If 100 Pakistani Muslim men rap...          80  
    81  RT @KTHopkins: If 100 Pakistani Muslim men rap...          81  
    82  @GazStant @BBCNews So nothing to do with Natur...          82  
    83  RT @BBCNews: Musicians hit by management fee '...          83  
    84  RT @Animal_Watch: Police commissioner makes se...          84  
    85  RT @chrisinsilico: Just did @BBCNews and @BBCr...          85  
    86  RT @kristieHphoto: Bexhill during a sunset 🌅 \...          86  
    87  RT @chrisinsilico: Hey @BBCNews and @BBCr4toda...          87  
    88  After 8 years of #austerity our public service...          88  
    89  RT @CrackingLeaders: @BBCNews @BBCNewsbeat @th...          89  
    90  Should it be illegal for a nation's leader to ...          90  
    91  RT @LadyMercia: @CllrBSilvester @lads_alliance...          91  
    92  RT @KTHopkins: If 100 Pakistani Muslim men rap...          92  
    93  RT @BBCNews: Musicians hit by management fee '...          93  
    94  @thehill The #TrumpEffect and the corrupt bias...          94  
    95  RT @UK4Europe: The @BBCNews are now waking up ...          95  
    96  RT @Ak__Ashii: @KTHopkins @thehugheslady @BBCN...          96  
    97  RT @BBCNews: Jeremy Corbyn told to act on 'sta...          97  
    98  RT @KTHopkins: If 100 Pakistani Muslim men rap...          98  
    99  RT @BBCNews: Musicians hit by management fee '...          99  
    
    [100 rows x 8 columns]
        compound                 date    neg    neu    pos source_account  \
    0    -0.4019  2018-29-03 04:12:30  0.130  0.870  0.000       @BBCNews   
    1     0.4215  2018-29-03 04:11:39  0.000  0.865  0.135       @BBCNews   
    2     0.0000  2018-29-03 04:11:32  0.000  1.000  0.000       @BBCNews   
    3     0.3818  2018-29-03 04:11:13  0.000  0.885  0.115       @BBCNews   
    4    -0.7096  2018-29-03 04:11:10  0.290  0.710  0.000       @BBCNews   
    5     0.0000  2018-29-03 04:11:08  0.000  1.000  0.000       @BBCNews   
    6     0.0000  2018-29-03 04:10:33  0.000  1.000  0.000       @BBCNews   
    7     0.3400  2018-29-03 04:10:25  0.056  0.833  0.111       @BBCNews   
    8     0.0000  2018-29-03 04:10:24  0.000  1.000  0.000       @BBCNews   
    9     0.0000  2018-29-03 04:10:11  0.000  1.000  0.000       @BBCNews   
    10    0.0000  2018-29-03 04:09:59  0.000  1.000  0.000       @BBCNews   
    11   -0.1779  2018-29-03 04:09:51  0.133  0.763  0.104       @BBCNews   
    12    0.4767  2018-29-03 04:09:48  0.077  0.737  0.186       @BBCNews   
    13   -0.6908  2018-29-03 04:09:38  0.170  0.830  0.000       @BBCNews   
    14    0.1531  2018-29-03 04:09:38  0.085  0.793  0.122       @BBCNews   
    15    0.0000  2018-29-03 04:09:33  0.000  1.000  0.000       @BBCNews   
    16   -0.6908  2018-29-03 04:08:17  0.170  0.830  0.000       @BBCNews   
    17    0.2960  2018-29-03 04:08:17  0.045  0.861  0.094       @BBCNews   
    18   -0.6908  2018-29-03 04:07:37  0.170  0.830  0.000       @BBCNews   
    19   -0.6908  2018-29-03 04:06:59  0.170  0.830  0.000       @BBCNews   
    20   -0.7003  2018-29-03 04:06:32  0.195  0.805  0.000       @BBCNews   
    21    0.0000  2018-29-03 04:06:29  0.000  1.000  0.000       @BBCNews   
    22    0.1531  2018-29-03 04:06:16  0.062  0.848  0.089       @BBCNews   
    23    0.2732  2018-29-03 04:05:17  0.000  0.811  0.189       @BBCNews   
    24    0.0000  2018-29-03 04:05:11  0.000  1.000  0.000       @BBCNews   
    25    0.0000  2018-29-03 04:05:04  0.000  1.000  0.000       @BBCNews   
    26   -0.2023  2018-29-03 04:04:59  0.184  0.816  0.000       @BBCNews   
    27   -0.6808  2018-29-03 04:04:55  0.204  0.796  0.000       @BBCNews   
    28    0.2960  2018-29-03 04:03:20  0.083  0.793  0.124       @BBCNews   
    29   -0.6705  2018-29-03 04:02:22  0.271  0.586  0.143       @BBCNews   
    ..       ...                  ...    ...    ...    ...            ...   
    70    0.6124  2018-29-03 04:05:06  0.000  0.706  0.294       @CBSNews   
    71    0.6808  2018-29-03 04:05:05  0.184  0.468  0.348       @CBSNews   
    72   -0.3400  2018-29-03 04:05:03  0.103  0.897  0.000       @CBSNews   
    73    0.4939  2018-29-03 04:04:48  0.000  0.862  0.138       @CBSNews   
    74    0.0000  2018-29-03 04:04:41  0.000  1.000  0.000       @CBSNews   
    75   -0.5994  2018-29-03 04:04:35  0.151  0.849  0.000       @CBSNews   
    76    0.0000  2018-29-03 04:04:33  0.000  1.000  0.000       @CBSNews   
    77   -0.3400  2018-29-03 04:04:28  0.103  0.897  0.000       @CBSNews   
    78   -0.4767  2018-29-03 04:04:21  0.608  0.392  0.000       @CBSNews   
    79    0.0000  2018-29-03 04:04:19  0.000  1.000  0.000       @CBSNews   
    80    0.0000  2018-29-03 04:04:11  0.000  1.000  0.000       @CBSNews   
    81    0.0000  2018-29-03 04:04:08  0.000  1.000  0.000       @CBSNews   
    82    0.6124  2018-29-03 04:04:06  0.000  0.706  0.294       @CBSNews   
    83    0.2960  2018-29-03 04:04:04  0.000  0.694  0.306       @CBSNews   
    84    0.6124  2018-29-03 04:04:03  0.000  0.706  0.294       @CBSNews   
    85    0.0000  2018-29-03 04:03:57  0.000  1.000  0.000       @CBSNews   
    86    0.0000  2018-29-03 04:03:53  0.000  1.000  0.000       @CBSNews   
    87    0.0000  2018-29-03 04:03:50  0.000  1.000  0.000       @CBSNews   
    88    0.0000  2018-29-03 04:03:44  0.000  1.000  0.000       @CBSNews   
    89    0.0790  2018-29-03 04:03:43  0.136  0.717  0.147       @CBSNews   
    90    0.0000  2018-29-03 04:03:32  0.000  1.000  0.000       @CBSNews   
    91    0.6124  2018-29-03 04:03:22  0.000  0.706  0.294       @CBSNews   
    92    0.5983  2018-29-03 04:03:19  0.000  0.551  0.449       @CBSNews   
    93   -0.3400  2018-29-03 04:03:11  0.103  0.897  0.000       @CBSNews   
    94   -0.1531  2018-29-03 04:02:57  0.150  0.727  0.123       @CBSNews   
    95    0.0000  2018-29-03 04:02:51  0.000  1.000  0.000       @CBSNews   
    96   -0.2263  2018-29-03 04:02:49  0.147  0.853  0.000       @CBSNews   
    97    0.0000  2018-29-03 04:02:47  0.000  1.000  0.000       @CBSNews   
    98   -0.4019  2018-29-03 04:02:45  0.120  0.824  0.056       @CBSNews   
    99    0.6124  2018-29-03 04:02:37  0.000  0.800  0.200       @CBSNews   
    
                                                     text  tweets_ago  
    0   RT @elise_tallaron: @BenPBradshaw @BestForBrit...           0  
    1   @BBCNews that article will show why im against...           1  
    2   RT @NewPlasticsEcon: Deposit return schemes we...           2  
    3   RT @VeroVero777: @DameWritesalot @BenPBradshaw...           3  
    4   RT @BBCNews: John Worboys: Court to rule on bl...           4  
    5   RT @joannaccherry: Is it just me or do @BBCNew...           5  
    6   RT @atmphillips: @ChristopherJor5 @Remain_Labo...           6  
    7   RT @Siemens: #AI, #BigData &amp; #Cloud techno...           7  
    8   RT @eloisetodd: Sticky tape in the pocket of a...           8  
    9   RT @ChristopherJor5: @BenPBradshaw @Remain_Lab...           9  
    10  RT @SatbirLSingh: - Theresa May has swapped he...          10  
    11  RT @iandonald_psych: Why is @theresa_may faili...          11  
    12  RT @BenPBradshaw: Dear @BBCNews All your trail...          12  
    13  RT @KTHopkins: If 100 Pakistani Muslim men rap...          13  
    14  @BBCNews you cant tell people we ,pay 6 billio...          14  
    15  RT @SandraDunn1955: @BBC @BBC_Joe_Lynam @BBCBr...          15  
    16  RT @KTHopkins: If 100 Pakistani Muslim men rap...          16  
    17  RT @tommyptoronto: For my entire life the BBC ...          17  
    18  RT @KTHopkins: If 100 Pakistani Muslim men rap...          18  
    19  RT @KTHopkins: If 100 Pakistani Muslim men rap...          19  
    20  RT @reb_les: This is where we are at today.\nT...          20  
    21                         @BBCNews alohg these lines          21  
    22  @BBCNews goverment aid is also called foreign ...          22  
    23  @ianmack2 @BBCNews @hendopolis Well get jumpin...          23  
    24  RT @joannaccherry: Is it just me or do @BBCNew...          24  
    25      @BBCNews In other words....too many patients.          25  
    26  RT @BBCNews: Hatton Garden heist: Man, 57, cha...          26  
    27  @BBCNews hey mofos, your Brits girls are raped...          27  
    28  RT @pleaseuseaussie: #auspol If you are PC inc...          28  
    29  RT @Greekboy8: OH LOOK, @UKLabour support surg...          29  
    ..                                                ...         ...  
    70  RT @CBSNews: Paul Manafort bets on presidentia...          70  
    71  RT @CBSNews: A boy with down syndrome who is a...          71  
    72  RT @adrianasdiaz: Students for gun reform hold...          72  
    73  RT @adrianasdiaz: On @CBSThisMorning: Inspired...          73  
    74  @CBSNews Where are Andy McCabe and @Comey 's i...          74  
    75  RT @CBSNews: In the wake of the shooting death...          75  
    76  RT @MinnTransplant: @CBSNews Don’t tell @realD...          76  
    77  RT @adrianasdiaz: Students for gun reform hold...          77  
    78                                 @CBSNews Fake News          78  
    79  RT @CBSNews: 2 airline pilots report seeing UF...          79  
    80  RT @CBSNews: 2 airline pilots report seeing UF...          80  
    81  RT @CBSNews: 2 airline pilots report seeing UF...          81  
    82  RT @CBSNews: Paul Manafort bets on presidentia...          82  
    83          @CBSNews One Felon helping another Felon.          83  
    84  RT @CBSNews: Paul Manafort bets on presidentia...          84  
    85  RT @CBSNews: Mega Millions jackpot hits $502 m...          85  
    86  RT @CBSNews: 2 airline pilots report seeing UF...          86  
    87  RT @CBSNews: 2 airline pilots report seeing UF...          87  
    88  @SueErikson @realdebfarmer @maddow @Lawrence @...          88  
    89  @CBSNews I just watched a video about the conc...          89  
    90  RT @CBSNews: 2 airline pilots report seeing UF...          90  
    91  RT @CBSNews: Paul Manafort bets on presidentia...          91  
    92     @CBSNews They are coming for Trump, thank god!          92  
    93  RT @adrianasdiaz: Students for gun reform hold...          93  
    94  RT @CBSNews: Boy with sick father turns to Pre...          94  
    95  RT @CBSNews: The reboot of "Roseanne" nabbed s...          95  
    96  RT @CBSNews: Stephon Clark shooting: Protests ...          96  
    97  RT @CBSNews: Mega Millions jackpot hits $502 m...          97  
    98  RT @CBSNews: A man named "Mad Mike" Hughes lau...          98  
    99  RT @CBSNews: Facebook controlled its privacy s...          99  
    
    [200 rows x 8 columns]
        compound                 date    neg    neu    pos source_account  \
    0    -0.4019  2018-29-03 04:12:30  0.130  0.870  0.000       @BBCNews   
    1     0.4215  2018-29-03 04:11:39  0.000  0.865  0.135       @BBCNews   
    2     0.0000  2018-29-03 04:11:32  0.000  1.000  0.000       @BBCNews   
    3     0.3818  2018-29-03 04:11:13  0.000  0.885  0.115       @BBCNews   
    4    -0.7096  2018-29-03 04:11:10  0.290  0.710  0.000       @BBCNews   
    5     0.0000  2018-29-03 04:11:08  0.000  1.000  0.000       @BBCNews   
    6     0.0000  2018-29-03 04:10:33  0.000  1.000  0.000       @BBCNews   
    7     0.3400  2018-29-03 04:10:25  0.056  0.833  0.111       @BBCNews   
    8     0.0000  2018-29-03 04:10:24  0.000  1.000  0.000       @BBCNews   
    9     0.0000  2018-29-03 04:10:11  0.000  1.000  0.000       @BBCNews   
    10    0.0000  2018-29-03 04:09:59  0.000  1.000  0.000       @BBCNews   
    11   -0.1779  2018-29-03 04:09:51  0.133  0.763  0.104       @BBCNews   
    12    0.4767  2018-29-03 04:09:48  0.077  0.737  0.186       @BBCNews   
    13   -0.6908  2018-29-03 04:09:38  0.170  0.830  0.000       @BBCNews   
    14    0.1531  2018-29-03 04:09:38  0.085  0.793  0.122       @BBCNews   
    15    0.0000  2018-29-03 04:09:33  0.000  1.000  0.000       @BBCNews   
    16   -0.6908  2018-29-03 04:08:17  0.170  0.830  0.000       @BBCNews   
    17    0.2960  2018-29-03 04:08:17  0.045  0.861  0.094       @BBCNews   
    18   -0.6908  2018-29-03 04:07:37  0.170  0.830  0.000       @BBCNews   
    19   -0.6908  2018-29-03 04:06:59  0.170  0.830  0.000       @BBCNews   
    20   -0.7003  2018-29-03 04:06:32  0.195  0.805  0.000       @BBCNews   
    21    0.0000  2018-29-03 04:06:29  0.000  1.000  0.000       @BBCNews   
    22    0.1531  2018-29-03 04:06:16  0.062  0.848  0.089       @BBCNews   
    23    0.2732  2018-29-03 04:05:17  0.000  0.811  0.189       @BBCNews   
    24    0.0000  2018-29-03 04:05:11  0.000  1.000  0.000       @BBCNews   
    25    0.0000  2018-29-03 04:05:04  0.000  1.000  0.000       @BBCNews   
    26   -0.2023  2018-29-03 04:04:59  0.184  0.816  0.000       @BBCNews   
    27   -0.6808  2018-29-03 04:04:55  0.204  0.796  0.000       @BBCNews   
    28    0.2960  2018-29-03 04:03:20  0.083  0.793  0.124       @BBCNews   
    29   -0.6705  2018-29-03 04:02:22  0.271  0.586  0.143       @BBCNews   
    ..       ...                  ...    ...    ...    ...            ...   
    70    0.6808  2018-29-03 04:12:17  0.000  0.349  0.651           @CNN   
    71   -0.7074  2018-29-03 04:12:15  0.549  0.451  0.000           @CNN   
    72    0.0000  2018-29-03 04:12:14  0.000  1.000  0.000           @CNN   
    73   -0.7486  2018-29-03 04:12:14  0.275  0.642  0.083           @CNN   
    74    0.0000  2018-29-03 04:12:14  0.000  1.000  0.000           @CNN   
    75   -0.0772  2018-29-03 04:12:14  0.075  0.925  0.000           @CNN   
    76    0.4588  2018-29-03 04:12:12  0.000  0.875  0.125           @CNN   
    77   -0.5106  2018-29-03 04:12:12  0.355  0.645  0.000           @CNN   
    78    0.0000  2018-29-03 04:12:10  0.000  1.000  0.000           @CNN   
    79   -0.4215  2018-29-03 04:12:08  0.272  0.570  0.158           @CNN   
    80   -0.2960  2018-29-03 04:12:08  0.104  0.896  0.000           @CNN   
    81   -0.1761  2018-29-03 04:12:07  0.158  0.842  0.000           @CNN   
    82    0.0000  2018-29-03 04:12:07  0.000  1.000  0.000           @CNN   
    83    0.0000  2018-29-03 04:12:07  0.000  1.000  0.000           @CNN   
    84    0.3400  2018-29-03 04:12:04  0.153  0.617  0.231           @CNN   
    85    0.0000  2018-29-03 04:12:04  0.000  1.000  0.000           @CNN   
    86    0.0258  2018-29-03 04:12:02  0.000  0.952  0.048           @CNN   
    87    0.0000  2018-29-03 04:12:01  0.000  1.000  0.000           @CNN   
    88    0.5574  2018-29-03 04:12:00  0.000  0.796  0.204           @CNN   
    89    0.6351  2018-29-03 04:12:00  0.000  0.794  0.206           @CNN   
    90   -0.2023  2018-29-03 04:11:59  0.070  0.930  0.000           @CNN   
    91   -0.7650  2018-29-03 04:11:59  0.398  0.602  0.000           @CNN   
    92    0.6908  2018-29-03 04:11:58  0.000  0.749  0.251           @CNN   
    93    0.0000  2018-29-03 04:11:56  0.000  1.000  0.000           @CNN   
    94    0.0000  2018-29-03 04:11:55  0.258  0.484  0.258           @CNN   
    95    0.4588  2018-29-03 04:11:54  0.000  0.700  0.300           @CNN   
    96    0.0258  2018-29-03 04:11:53  0.000  0.952  0.048           @CNN   
    97    0.0258  2018-29-03 04:11:53  0.000  0.952  0.048           @CNN   
    98    0.0000  2018-29-03 04:11:51  0.000  1.000  0.000           @CNN   
    99    0.0000  2018-29-03 04:11:51  0.000  1.000  0.000           @CNN   
    
                                                     text  tweets_ago  
    0   RT @elise_tallaron: @BenPBradshaw @BestForBrit...           0  
    1   @BBCNews that article will show why im against...           1  
    2   RT @NewPlasticsEcon: Deposit return schemes we...           2  
    3   RT @VeroVero777: @DameWritesalot @BenPBradshaw...           3  
    4   RT @BBCNews: John Worboys: Court to rule on bl...           4  
    5   RT @joannaccherry: Is it just me or do @BBCNew...           5  
    6   RT @atmphillips: @ChristopherJor5 @Remain_Labo...           6  
    7   RT @Siemens: #AI, #BigData &amp; #Cloud techno...           7  
    8   RT @eloisetodd: Sticky tape in the pocket of a...           8  
    9   RT @ChristopherJor5: @BenPBradshaw @Remain_Lab...           9  
    10  RT @SatbirLSingh: - Theresa May has swapped he...          10  
    11  RT @iandonald_psych: Why is @theresa_may faili...          11  
    12  RT @BenPBradshaw: Dear @BBCNews All your trail...          12  
    13  RT @KTHopkins: If 100 Pakistani Muslim men rap...          13  
    14  @BBCNews you cant tell people we ,pay 6 billio...          14  
    15  RT @SandraDunn1955: @BBC @BBC_Joe_Lynam @BBCBr...          15  
    16  RT @KTHopkins: If 100 Pakistani Muslim men rap...          16  
    17  RT @tommyptoronto: For my entire life the BBC ...          17  
    18  RT @KTHopkins: If 100 Pakistani Muslim men rap...          18  
    19  RT @KTHopkins: If 100 Pakistani Muslim men rap...          19  
    20  RT @reb_les: This is where we are at today.\nT...          20  
    21                         @BBCNews alohg these lines          21  
    22  @BBCNews goverment aid is also called foreign ...          22  
    23  @ianmack2 @BBCNews @hendopolis Well get jumpin...          23  
    24  RT @joannaccherry: Is it just me or do @BBCNew...          24  
    25      @BBCNews In other words....too many patients.          25  
    26  RT @BBCNews: Hatton Garden heist: Man, 57, cha...          26  
    27  @BBCNews hey mofos, your Brits girls are raped...          27  
    28  RT @pleaseuseaussie: #auspol If you are PC inc...          28  
    29  RT @Greekboy8: OH LOOK, @UKLabour support surg...          29  
    ..                                                ...         ...  
    70                @CNN What a warm, wonderful person.          70  
    71   @CNN FN racist idiots!!! https://t.co/wnEwbx86nN          71  
    72                      @CNN  https://t.co/wYavy1yYDn          72  
    73  @CNN If i’m not fucking mistaken police works ...          73  
    74  @CNN Shopping off of the #FauxNews channel jus...          74  
    75  @WontShootUrDog @Kelly830fps @CNN Oh right, he...          75  
    76  @MarkDice @CNN Who wants to look down the barr...          76  
    77       @Markie066 @CNN This is incoherent and dumb.          77  
    78  @carolynedgar I went to mute on @andersoncoope...          78  
    79  @CNN Nothing like making a bunch of #BLOOD💰💰💰💰...          79  
    80  @CNN They're right.... If someone is breaking ...          80  
    81  @CNN Another “probe” with very vague and broad...          81  
    82                     @CNN Is Obama still president?          82  
    83  @Brower24 @m27731630 @KaziMuhaimen @irving_cla...          83  
    84  RT @AliCDonaldson: Wow. Over 36 years after hi...          84  
    85                             @CNN Because it is....          85  
    86  RT @CNN: The White House calls police shooting...          86  
    87  RT @rameshchahal: #SaintMSG_Initiative57\n#मुफ...          87  
    88  RT @JennaMC_Laugh: DOJ Pardon Attorney's Offic...          88  
    89  @CNN Please ask Comey?Why did he put out sh-- ...          89  
    90  RT @RealCandaceO: I believe this is the second...          90  
    91  @CNN Santorum just proved his an idiot and a s...          91  
    92  @bealone4runner @CNN Or the fact that it is th...          92  
    93  @Lawrence @washingtonpost Also @RickSantorum A...          93  
    94  @Ultrastar1970wh @CNN I’m laughing AT YOU! You...          94  
    95           @CNN Oh sweet baby jeezus. Just go away.          95  
    96  RT @CNN: The White House calls police shooting...          96  
    97  RT @CNN: The White House calls police shooting...          97  
    98  @KatyTurNBC @MSNBC @CNN @AriMelber @JoyAnnReid...          98  
    99  @cnn @brianstelter There ya go... https://t.co...          99  
    
    [300 rows x 8 columns]
        compound                 date    neg    neu    pos source_account  \
    0    -0.4019  2018-29-03 04:12:30  0.130  0.870  0.000       @BBCNews   
    1     0.4215  2018-29-03 04:11:39  0.000  0.865  0.135       @BBCNews   
    2     0.0000  2018-29-03 04:11:32  0.000  1.000  0.000       @BBCNews   
    3     0.3818  2018-29-03 04:11:13  0.000  0.885  0.115       @BBCNews   
    4    -0.7096  2018-29-03 04:11:10  0.290  0.710  0.000       @BBCNews   
    5     0.0000  2018-29-03 04:11:08  0.000  1.000  0.000       @BBCNews   
    6     0.0000  2018-29-03 04:10:33  0.000  1.000  0.000       @BBCNews   
    7     0.3400  2018-29-03 04:10:25  0.056  0.833  0.111       @BBCNews   
    8     0.0000  2018-29-03 04:10:24  0.000  1.000  0.000       @BBCNews   
    9     0.0000  2018-29-03 04:10:11  0.000  1.000  0.000       @BBCNews   
    10    0.0000  2018-29-03 04:09:59  0.000  1.000  0.000       @BBCNews   
    11   -0.1779  2018-29-03 04:09:51  0.133  0.763  0.104       @BBCNews   
    12    0.4767  2018-29-03 04:09:48  0.077  0.737  0.186       @BBCNews   
    13   -0.6908  2018-29-03 04:09:38  0.170  0.830  0.000       @BBCNews   
    14    0.1531  2018-29-03 04:09:38  0.085  0.793  0.122       @BBCNews   
    15    0.0000  2018-29-03 04:09:33  0.000  1.000  0.000       @BBCNews   
    16   -0.6908  2018-29-03 04:08:17  0.170  0.830  0.000       @BBCNews   
    17    0.2960  2018-29-03 04:08:17  0.045  0.861  0.094       @BBCNews   
    18   -0.6908  2018-29-03 04:07:37  0.170  0.830  0.000       @BBCNews   
    19   -0.6908  2018-29-03 04:06:59  0.170  0.830  0.000       @BBCNews   
    20   -0.7003  2018-29-03 04:06:32  0.195  0.805  0.000       @BBCNews   
    21    0.0000  2018-29-03 04:06:29  0.000  1.000  0.000       @BBCNews   
    22    0.1531  2018-29-03 04:06:16  0.062  0.848  0.089       @BBCNews   
    23    0.2732  2018-29-03 04:05:17  0.000  0.811  0.189       @BBCNews   
    24    0.0000  2018-29-03 04:05:11  0.000  1.000  0.000       @BBCNews   
    25    0.0000  2018-29-03 04:05:04  0.000  1.000  0.000       @BBCNews   
    26   -0.2023  2018-29-03 04:04:59  0.184  0.816  0.000       @BBCNews   
    27   -0.6808  2018-29-03 04:04:55  0.204  0.796  0.000       @BBCNews   
    28    0.2960  2018-29-03 04:03:20  0.083  0.793  0.124       @BBCNews   
    29   -0.6705  2018-29-03 04:02:22  0.271  0.586  0.143       @BBCNews   
    ..       ...                  ...    ...    ...    ...            ...   
    70    0.3818  2018-29-03 04:12:38  0.000  0.885  0.115       @FoxNews   
    71   -0.2732  2018-29-03 04:12:38  0.199  0.663  0.138       @FoxNews   
    72    0.5574  2018-29-03 04:12:37  0.000  0.827  0.173       @FoxNews   
    73    0.0000  2018-29-03 04:12:37  0.000  1.000  0.000       @FoxNews   
    74   -0.2732  2018-29-03 04:12:36  0.199  0.663  0.138       @FoxNews   
    75    0.0000  2018-29-03 04:12:36  0.000  1.000  0.000       @FoxNews   
    76   -0.3818  2018-29-03 04:12:35  0.115  0.885  0.000       @FoxNews   
    77    0.0000  2018-29-03 04:12:35  0.000  1.000  0.000       @FoxNews   
    78    0.6249  2018-29-03 04:12:34  0.000  0.773  0.227       @FoxNews   
    79   -0.8531  2018-29-03 04:12:33  0.345  0.609  0.047       @FoxNews   
    80   -0.2732  2018-29-03 04:12:33  0.199  0.663  0.138       @FoxNews   
    81   -0.2732  2018-29-03 04:12:33  0.199  0.663  0.138       @FoxNews   
    82    0.0000  2018-29-03 04:12:32  0.000  1.000  0.000       @FoxNews   
    83    0.4201  2018-29-03 04:12:31  0.000  0.642  0.358       @FoxNews   
    84    0.4019  2018-29-03 04:12:31  0.000  0.828  0.172       @FoxNews   
    85   -0.2732  2018-29-03 04:12:30  0.199  0.663  0.138       @FoxNews   
    86   -0.6369  2018-29-03 04:12:30  0.154  0.846  0.000       @FoxNews   
    87   -0.2732  2018-29-03 04:12:30  0.199  0.663  0.138       @FoxNews   
    88    0.0000  2018-29-03 04:12:29  0.000  1.000  0.000       @FoxNews   
    89    0.9371  2018-29-03 04:12:29  0.000  0.493  0.507       @FoxNews   
    90    0.9041  2018-29-03 04:12:28  0.000  0.556  0.444       @FoxNews   
    91   -0.7351  2018-29-03 04:12:27  0.323  0.677  0.000       @FoxNews   
    92   -0.3400  2018-29-03 04:12:26  0.324  0.676  0.000       @FoxNews   
    93   -0.2732  2018-29-03 04:12:26  0.199  0.663  0.138       @FoxNews   
    94   -0.4767  2018-29-03 04:12:26  0.140  0.860  0.000       @FoxNews   
    95    0.1680  2018-29-03 04:12:25  0.146  0.664  0.190       @FoxNews   
    96   -0.2732  2018-29-03 04:12:23  0.199  0.663  0.138       @FoxNews   
    97   -0.2732  2018-29-03 04:12:22  0.199  0.663  0.138       @FoxNews   
    98    0.0000  2018-29-03 04:12:22  0.000  1.000  0.000       @FoxNews   
    99   -0.2732  2018-29-03 04:12:21  0.199  0.663  0.138       @FoxNews   
    
                                                     text  tweets_ago  
    0   RT @elise_tallaron: @BenPBradshaw @BestForBrit...           0  
    1   @BBCNews that article will show why im against...           1  
    2   RT @NewPlasticsEcon: Deposit return schemes we...           2  
    3   RT @VeroVero777: @DameWritesalot @BenPBradshaw...           3  
    4   RT @BBCNews: John Worboys: Court to rule on bl...           4  
    5   RT @joannaccherry: Is it just me or do @BBCNew...           5  
    6   RT @atmphillips: @ChristopherJor5 @Remain_Labo...           6  
    7   RT @Siemens: #AI, #BigData &amp; #Cloud techno...           7  
    8   RT @eloisetodd: Sticky tape in the pocket of a...           8  
    9   RT @ChristopherJor5: @BenPBradshaw @Remain_Lab...           9  
    10  RT @SatbirLSingh: - Theresa May has swapped he...          10  
    11  RT @iandonald_psych: Why is @theresa_may faili...          11  
    12  RT @BenPBradshaw: Dear @BBCNews All your trail...          12  
    13  RT @KTHopkins: If 100 Pakistani Muslim men rap...          13  
    14  @BBCNews you cant tell people we ,pay 6 billio...          14  
    15  RT @SandraDunn1955: @BBC @BBC_Joe_Lynam @BBCBr...          15  
    16  RT @KTHopkins: If 100 Pakistani Muslim men rap...          16  
    17  RT @tommyptoronto: For my entire life the BBC ...          17  
    18  RT @KTHopkins: If 100 Pakistani Muslim men rap...          18  
    19  RT @KTHopkins: If 100 Pakistani Muslim men rap...          19  
    20  RT @reb_les: This is where we are at today.\nT...          20  
    21                         @BBCNews alohg these lines          21  
    22  @BBCNews goverment aid is also called foreign ...          22  
    23  @ianmack2 @BBCNews @hendopolis Well get jumpin...          23  
    24  RT @joannaccherry: Is it just me or do @BBCNew...          24  
    25      @BBCNews In other words....too many patients.          25  
    26  RT @BBCNews: Hatton Garden heist: Man, 57, cha...          26  
    27  @BBCNews hey mofos, your Brits girls are raped...          27  
    28  RT @pleaseuseaussie: #auspol If you are PC inc...          28  
    29  RT @Greekboy8: OH LOOK, @UKLabour support surg...          29  
    ..                                                ...         ...  
    70  @FoxNews Tomorrow they’re gonna have a big pol...          70  
    71  RT @funder: Laura Ingraham should be fired fro...          71  
    72  RT @FoxNews: Gordon Chang on meeting between C...          72  
    73  RT @FoxNews: .@michellemalkin on 2020 census t...          73  
    74  RT @funder: Laura Ingraham should be fired fro...          74  
    75  RT @YourAnonNews: #FoxNewsChallenge To those o...          75  
    76  @FoxNews @TomiLahren You spreading this same c...          76  
    77  RT @FoxNews: .@DevinNunes: “The Left has conti...          77  
    78  RT @DanielT45441843: @FoxNews @DevinNunes Grea...          78  
    79  @IngrahamAngle @FoxNews This poor excuse for a...          79  
    80  RT @funder: Laura Ingraham should be fired fro...          80  
    81  RT @funder: Laura Ingraham should be fired fro...          81  
    82  RT @FoxNews: .@michellemalkin on 2020 census t...          82  
    83  @FoxNews @SteveHiltonx @foxnewsnight Highly ag...          83  
    84  RT @FoxNews: .@DonaldJTrumpJr tweets his suppo...          84  
    85  RT @funder: Laura Ingraham should be fired fro...          85  
    86  RT @FoxNews: .@RepGoodlatte on alleged FISA ab...          86  
    87  RT @funder: Laura Ingraham should be fired fro...          87  
    88  RT @FoxNews: .@DevinNunes: “The Left has conti...          88  
    89  @FoxNews @michellemalkin Hi @michellemalkin  l...          89  
    90  RT @AngelLight2U: A great big, beautiful wall!...          90  
    91  RT @FoxNews: Oklahoma man captures 6-foot ratt...          91  
    92  @FoxNews you should fire @IngrahamAngle https:...          92  
    93  RT @funder: Laura Ingraham should be fired fro...          93  
    94  Since when do MAJOR NETWORKS attack kids? @CNN...          94  
    95  @davidfinnerty @FoxNews @realDonaldTrump No mo...          95  
    96  RT @funder: Laura Ingraham should be fired fro...          96  
    97  RT @funder: Laura Ingraham should be fired fro...          97  
    98  RT @FoxNews: .@DevinNunes: “The Left has conti...          98  
    99  RT @funder: Laura Ingraham should be fired fro...          99  
    
    [400 rows x 8 columns]
        compound                 date    neg    neu    pos source_account  \
    0    -0.4019  2018-29-03 04:12:30  0.130  0.870  0.000       @BBCNews   
    1     0.4215  2018-29-03 04:11:39  0.000  0.865  0.135       @BBCNews   
    2     0.0000  2018-29-03 04:11:32  0.000  1.000  0.000       @BBCNews   
    3     0.3818  2018-29-03 04:11:13  0.000  0.885  0.115       @BBCNews   
    4    -0.7096  2018-29-03 04:11:10  0.290  0.710  0.000       @BBCNews   
    5     0.0000  2018-29-03 04:11:08  0.000  1.000  0.000       @BBCNews   
    6     0.0000  2018-29-03 04:10:33  0.000  1.000  0.000       @BBCNews   
    7     0.3400  2018-29-03 04:10:25  0.056  0.833  0.111       @BBCNews   
    8     0.0000  2018-29-03 04:10:24  0.000  1.000  0.000       @BBCNews   
    9     0.0000  2018-29-03 04:10:11  0.000  1.000  0.000       @BBCNews   
    10    0.0000  2018-29-03 04:09:59  0.000  1.000  0.000       @BBCNews   
    11   -0.1779  2018-29-03 04:09:51  0.133  0.763  0.104       @BBCNews   
    12    0.4767  2018-29-03 04:09:48  0.077  0.737  0.186       @BBCNews   
    13   -0.6908  2018-29-03 04:09:38  0.170  0.830  0.000       @BBCNews   
    14    0.1531  2018-29-03 04:09:38  0.085  0.793  0.122       @BBCNews   
    15    0.0000  2018-29-03 04:09:33  0.000  1.000  0.000       @BBCNews   
    16   -0.6908  2018-29-03 04:08:17  0.170  0.830  0.000       @BBCNews   
    17    0.2960  2018-29-03 04:08:17  0.045  0.861  0.094       @BBCNews   
    18   -0.6908  2018-29-03 04:07:37  0.170  0.830  0.000       @BBCNews   
    19   -0.6908  2018-29-03 04:06:59  0.170  0.830  0.000       @BBCNews   
    20   -0.7003  2018-29-03 04:06:32  0.195  0.805  0.000       @BBCNews   
    21    0.0000  2018-29-03 04:06:29  0.000  1.000  0.000       @BBCNews   
    22    0.1531  2018-29-03 04:06:16  0.062  0.848  0.089       @BBCNews   
    23    0.2732  2018-29-03 04:05:17  0.000  0.811  0.189       @BBCNews   
    24    0.0000  2018-29-03 04:05:11  0.000  1.000  0.000       @BBCNews   
    25    0.0000  2018-29-03 04:05:04  0.000  1.000  0.000       @BBCNews   
    26   -0.2023  2018-29-03 04:04:59  0.184  0.816  0.000       @BBCNews   
    27   -0.6808  2018-29-03 04:04:55  0.204  0.796  0.000       @BBCNews   
    28    0.2960  2018-29-03 04:03:20  0.083  0.793  0.124       @BBCNews   
    29   -0.6705  2018-29-03 04:02:22  0.271  0.586  0.143       @BBCNews   
    ..       ...                  ...    ...    ...    ...            ...   
    70    0.2263  2018-29-03 04:10:04  0.223  0.457  0.320       @nytimes   
    71   -0.3400  2018-29-03 04:09:51  0.103  0.897  0.000       @nytimes   
    72   -0.4588  2018-29-03 04:09:50  0.115  0.885  0.000       @nytimes   
    73    0.0000  2018-29-03 04:09:45  0.000  1.000  0.000       @nytimes   
    74    0.0000  2018-29-03 04:09:40  0.000  1.000  0.000       @nytimes   
    75    0.5994  2018-29-03 04:09:39  0.000  0.795  0.205       @nytimes   
    76    0.5719  2018-29-03 04:09:38  0.000  0.802  0.198       @nytimes   
    77   -0.3612  2018-29-03 04:09:36  0.197  0.692  0.111       @nytimes   
    78    0.0000  2018-29-03 04:09:33  0.000  1.000  0.000       @nytimes   
    79    0.0000  2018-29-03 04:09:27  0.000  1.000  0.000       @nytimes   
    80   -0.7783  2018-29-03 04:09:26  0.430  0.570  0.000       @nytimes   
    81   -0.5267  2018-29-03 04:09:23  0.246  0.658  0.096       @nytimes   
    82   -0.2960  2018-29-03 04:09:20  0.180  0.820  0.000       @nytimes   
    83   -0.8625  2018-29-03 04:09:13  0.375  0.625  0.000       @nytimes   
    84   -0.5267  2018-29-03 04:09:12  0.269  0.625  0.106       @nytimes   
    85    0.8176  2018-29-03 04:09:07  0.000  0.694  0.306       @nytimes   
    86    0.5994  2018-29-03 04:09:06  0.000  0.795  0.205       @nytimes   
    87    0.0000  2018-29-03 04:09:05  0.000  1.000  0.000       @nytimes   
    88   -0.2960  2018-29-03 04:09:04  0.180  0.820  0.000       @nytimes   
    89    0.2263  2018-29-03 04:09:04  0.223  0.457  0.320       @nytimes   
    90   -0.3182  2018-29-03 04:09:04  0.150  0.850  0.000       @nytimes   
    91    0.0000  2018-29-03 04:09:03  0.000  1.000  0.000       @nytimes   
    92    0.3313  2018-29-03 04:09:03  0.000  0.856  0.144       @nytimes   
    93   -0.7906  2018-29-03 04:09:02  0.412  0.588  0.000       @nytimes   
    94    0.0000  2018-29-03 04:09:02  0.000  1.000  0.000       @nytimes   
    95    0.0000  2018-29-03 04:09:01  0.000  1.000  0.000       @nytimes   
    96    0.0000  2018-29-03 04:08:59  0.000  1.000  0.000       @nytimes   
    97    0.9047  2018-29-03 04:08:58  0.045  0.548  0.407       @nytimes   
    98    0.0000  2018-29-03 04:08:58  0.000  1.000  0.000       @nytimes   
    99    0.0000  2018-29-03 04:08:55  0.000  1.000  0.000       @nytimes   
    
                                                     text  tweets_ago  
    0   RT @elise_tallaron: @BenPBradshaw @BestForBrit...           0  
    1   @BBCNews that article will show why im against...           1  
    2   RT @NewPlasticsEcon: Deposit return schemes we...           2  
    3   RT @VeroVero777: @DameWritesalot @BenPBradshaw...           3  
    4   RT @BBCNews: John Worboys: Court to rule on bl...           4  
    5   RT @joannaccherry: Is it just me or do @BBCNew...           5  
    6   RT @atmphillips: @ChristopherJor5 @Remain_Labo...           6  
    7   RT @Siemens: #AI, #BigData &amp; #Cloud techno...           7  
    8   RT @eloisetodd: Sticky tape in the pocket of a...           8  
    9   RT @ChristopherJor5: @BenPBradshaw @Remain_Lab...           9  
    10  RT @SatbirLSingh: - Theresa May has swapped he...          10  
    11  RT @iandonald_psych: Why is @theresa_may faili...          11  
    12  RT @BenPBradshaw: Dear @BBCNews All your trail...          12  
    13  RT @KTHopkins: If 100 Pakistani Muslim men rap...          13  
    14  @BBCNews you cant tell people we ,pay 6 billio...          14  
    15  RT @SandraDunn1955: @BBC @BBC_Joe_Lynam @BBCBr...          15  
    16  RT @KTHopkins: If 100 Pakistani Muslim men rap...          16  
    17  RT @tommyptoronto: For my entire life the BBC ...          17  
    18  RT @KTHopkins: If 100 Pakistani Muslim men rap...          18  
    19  RT @KTHopkins: If 100 Pakistani Muslim men rap...          19  
    20  RT @reb_les: This is where we are at today.\nT...          20  
    21                         @BBCNews alohg these lines          21  
    22  @BBCNews goverment aid is also called foreign ...          22  
    23  @ianmack2 @BBCNews @hendopolis Well get jumpin...          23  
    24  RT @joannaccherry: Is it just me or do @BBCNew...          24  
    25      @BBCNews In other words....too many patients.          25  
    26  RT @BBCNews: Hatton Garden heist: Man, 57, cha...          26  
    27  @BBCNews hey mofos, your Brits girls are raped...          27  
    28  RT @pleaseuseaussie: #auspol If you are PC inc...          28  
    29  RT @Greekboy8: OH LOOK, @UKLabour support surg...          29  
    ..                                                ...         ...  
    70  RT @nytimes: Mireille Knoll, Murdered Holocaus...          70  
    71  RT @nytimes: In Opinion,\nIsabelle Robinson, a...          71  
    72  RT @carlzimmer: Chile’s scientists are up in a...          72  
    73  RT @Lawrence: Today’s @nytimes editorial:\n\n“...          73  
    74  RT @nytimes: Anbang Was Seized by China. Now, ...          74  
    75  RT @nytimes: Trump’s lawyer discussed pardons ...          75  
    76  @hbarkey @nytimes I once showed " Babette's Fe...          76  
    77  RT @nytimes: Tanzina Vega is the new host of “...          77  
    78  RT @katwomanfifi: @nytimes @marhoiland she rem...          78  
    79            RT @Bella_ofA: @Reaper_004 @nytimes 😂😂😂          79  
    80  Trump’s Heartless Transgender Military Ban Get...          80  
    81  RT @DemocratsSpain: @twit_grim @BrandonNLB17 @...          81  
    82  RT @nytimes: Ecuador cuts off Julian Assange’s...          82  
    83  RT @nytimes: New police finding in Skripal poi...          83  
    84  @twit_grim @BrandonNLB17 @gcorralvandamme @nyt...          84  
    85  RT @SteiniBrown: Congratulations to my colleag...          85  
    86  RT @nytimes: Trump’s lawyer discussed pardons ...          86  
    87  @nytimes I would also say the comment about th...          87  
    88  RT @nytimes: Ecuador cuts off Julian Assange’s...          88  
    89  RT @nytimes: Mireille Knoll, Murdered Holocaus...          89  
    90  Persecuted on land, Cambodia's ethnic Vietname...          90  
    91  RT @nytimes: Anbang Was Seized by China. Now, ...          91  
    92  @CNN Isn't the NRA tax exempt??? Why? \n\n@CNN...          92  
    93  Woman Becomes First South African Imprisoned f...          93  
    94  RT @krupashanker: @DavidCooked1 @abdu_rafiq @m...          94  
    95  RT @Lawrence: Today’s @nytimes editorial:\n\n“...          95  
    96  RT @monk_asian: @WangSiYun9 @DavidCooked1 @abd...          96  
    97  @nytimes Thank you Thank you Thank you for bei...          97  
    98  RT @nytimes: Anbang Was Seized by China. Now, ...          98  
    99     @JoePalooka4 @nytimes Oh wait...a bot #blocked          99  
    
    [500 rows x 8 columns]



```python
#Group by news outlet
grouped = master_df.groupby('source_account')

#Get data for BBC
BBC_x_axis = grouped.get_group('@BBCNews')['tweets_ago'].tolist()
BBC_data = grouped.get_group('@BBCNews')['compound'].tolist()

#Get data for CBS
CBS_x_axis = grouped.get_group('@CBSNews')['tweets_ago'].tolist()
CBS_data = grouped.get_group('@CBSNews')['compound'].tolist()

#Get data for CNN
CNN_x_axis = grouped.get_group('@CNN')['tweets_ago'].tolist()
CNN_data = grouped.get_group('@CNN')['compound'].tolist()

#Get data for FOX
FOX_x_axis = grouped.get_group('@FoxNews')['tweets_ago'].tolist()
FOX_data = grouped.get_group('@FoxNews')['compound'].tolist()

#Get data for NYT
NYT_x_axis = grouped.get_group('@nytimes')['tweets_ago'].tolist()
NYT_data = grouped.get_group('@nytimes')['compound'].tolist()

#Create scatter plots
BBC_scatter = plt.scatter(BBC_x_axis, BBC_data, marker="o", facecolor="cyan", edgecolor='black', linewidth='1', s=100, alpha=0.7)
CBS_scatter = plt.scatter(CBS_x_axis, CBS_data, marker="o", facecolor="green", edgecolor='black', linewidth='1', s=100, alpha=0.7)
CNN_scatter = plt.scatter(CNN_x_axis, CNN_data, marker="o", facecolor="red", edgecolor='black', linewidth='1', s=100, alpha=0.7)
FOX_scatter = plt.scatter(FOX_x_axis, FOX_data, marker="o", facecolor="blue", edgecolor='black', linewidth='1', s=100, alpha=0.7)
NYT_scatter = plt.scatter(NYT_x_axis, NYT_data, marker="o", facecolor="yellow", edgecolor='black', linewidth='1', s=100, alpha=0.7)

#Format plot
plt.grid()
plt.ylim(-1, 1)
plt.xlim(105,-5)
plt.title("Sentiment Analysis of Media Tweets (03/28/2018)")
plt.xlabel("Tweets Ago")
plt.ylabel("Tweet Polarity")

#Add Legend
D_id_color = {'BBC': u'cyan', 'CBS': u'green', 'CNN': u'red', 'Fox': u'blue', 'NYT': u'yellow'}
markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='', markeredgecolor='black', markersize=10) for color in D_id_color.values()]
plt.legend(markers, D_id_color.keys(), numpoints=1, bbox_to_anchor=(1.15,1), loc="upper right", frameon = False)

#Set figure size
fig = plt.gcf()
fig.set_size_inches(8, 5, forward=True)


#Save figure
fig.savefig('News_Sentiment_Analysis.png', dpi=100)

#Show plot
plt.show()

```


![png](output_2_0.png)



```python
#Get mean of sentiment compound by news outlet and add to list
news_outlet_average = []

news_outlet_average.append(round(np.mean(grouped.get_group('@BBCNews')['compound']),2))
news_outlet_average.append(round(np.mean(grouped.get_group('@CBSNews')['compound']),2))
news_outlet_average.append(round(np.mean(grouped.get_group('@CNN')['compound']),2))
news_outlet_average.append(round(np.mean(grouped.get_group('@FoxNews')['compound']),2))
news_outlet_average.append(round(np.mean(grouped.get_group('@nytimes')['compound']),2))

news_outlet_names = ['BBC', 'CBS', 'CNN', 'Fox', 'NYT']

#Plot bar chart
barlist = plt.bar(news_outlet_names, news_outlet_average, width=1.0, linestyle=None)

#Format chart
plt.xlabel("Tweet Polarity")
plt.ylabel("News Outlets")
plt.title("Overall Media Sentiment based on Twitter (03/28/2017)")

#Set bar colors
barlist[0].set_color('cyan')
barlist[1].set_color('green')
barlist[2].set_color('red')
barlist[3].set_color('blue')
barlist[4].set_color('yellow')

#Display values for bars 
for a,b in zip(news_outlet_names, news_outlet_average):
    if b>0:
        plt.text(a, b, str(b), ha='center', va='bottom')
    else:
        plt.text(a, b, str(b), ha='center', va='top')

#Add horizontal line for 0
#plt.axhline(y=0, color='black', linestyle='-')

#Set figure size
fig = plt.gcf()
fig.set_size_inches(6, 5, forward=True)


for spine in plt.gca().spines.values():
    spine.set_visible(False)

plt.tight_layout()

#Save figure
fig.savefig('News_Overall_Sentiment_Analysis.png', dpi=100)


plt.show()

```


![png](output_3_0.png)

