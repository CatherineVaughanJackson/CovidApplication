#!/usr/bin/env python
# coding: utf-8

# In[ ]:


global Cities_Towns
global Counties
global Region


# In[1]:


Cities_Towns = ['Hartlepool', 'Middlesbrough','Stockton-on-Tees', 'Darlington', 'Halton', 
               'Warrington','Blackpool','Kingston upon Hull, City of', 'York', 'Derby',
               'Leicester', 'Nottingham','Stoke-on-Trent','Bristol, City of','Plymouth',
               'Swindon', 'Peterborough', 'Luton', 'Southend-on-Sea','Reading', 'Slough', 
               'Wokingham', 'Milton Keynes','Portsmouth', 'Southampton','Bedford','Wycombe', 
               'Cambridge', 'Barrow-in-Furness','Carlisle', 'Bolsover', 'Chesterfield', 'Exeter', 
               'Eastbourne', 'Hastings','Lewes', 'Basildon', 'Braintree', 'Brentwood','Chelmsford', 
               'Colchester', 'Harlow', 'Maldon', 'Rochford', 'Cheltenham', 'Gloucester', 'Stroud',
               'Tewkesbury','Eastleigh', 'Fareham', 'Gosport', 'Havant', 'Winchester', 'Broxbourne', 
               'Watford','Ashford', 'Canterbury', 'Dartford', 'Dover','Maidstone', 'Sevenoaks',
               'Tunbridge Wells', 'Burnley','Chorley', 'Lancaster', 'Preston','Boston', 'Lincoln',
               'Breckland', 'Great Yarmouth','Norwich','Corby', 'Daventry','Kettering', 
               'Northampton','Wellingborough', 'Craven', 'Hambleton', 'Harrogate','Scarborough', 
               'Selby', 'Ashfield','Broxtowe', 'Gedling', 'Mansfield','Oxford','Lichfield', 
               'Newcastle-under-Lyme','Stafford','Tamworth', 'Ipswich', 'Elmbridge','Guildford', 
               'Woking','Rugby', 'Stratford-on-Avon', 'Warwick','Chichester', 'Crawley', 
               'Horsham','Worthing', 'Bromsgrove', 'Redditch', 'Worcester','St Albans',
               'Stevenage', 'Bolton', 'Bury', 'Manchester','Oldham', 'Rochdale', 'Salford', 
               'Stockport','Trafford', 'Wigan', 'Knowsley', 'Liverpool', 'St. Helens',
               'Sefton', 'Wirral', 'Barnsley', 'Doncaster', 'Rotherham','Sheffield', 
               'Newcastle upon Tyne' 'Sunderland', 'Birmingham', 'Coventry', 'Dudley','Sandwell',
               'Solihull', 'Walsall', 'Wolverhampton', 'Bradford','Calderdale', 'Kirklees', 
               'Leeds', 'Wakefield', 'Gateshead','Bromley', 'Camden', 'Croydon',
               'Ealing', 'Enfield', 'Greenwich','Hackney and City of London', 
               'Hammersmith and Fulham', 'Haringey','Harrow', 'Havering', 'Hillingdon', 
               'Hounslow', 'Islington','Kensington and Chelsea', 'Kingston upon Thames', 
               'Lambeth','Lewisham', 'Merton', 'Newham', 'Redbridge','Richmond upon Thames', 
               'Southwark', 'Sutton', 'Tower Hamlets','Waltham Forest', 'Wandsworth', 'Westminster']


# In[2]:


Counties=['Redcar and Cleveland','Blackburn with Darwen','East Riding of Yorkshire',
          'North East Lincolnshire', 'North Lincolnshire', 'Rutland', 
          'Herefordshire, County of','Telford and Wrekin','Bath and North East Somerset', 
          'North Somerset', 'South Gloucestershire', 'Torbay','Thurrock','Medway', 
          'Bracknell Forest', 'West Berkshire', 'Windsor and Maidenhead','Brighton and Hove', 
          'Isle of Wight','County Durham', 'Cheshire East', 'Cheshire West and Chester',
          'Shropshire', 'Cornwall and Isles of Scilly', 'Wiltshire','Central Bedfordshire',
          'Northumberland','Bournemouth, Christchurch and Poole', 'Dorset', 'Aylesbury Vale',
          'Chiltern', 'South Bucks', 'East Cambridgeshire', 'Fenland', 'Huntingdonshire',
          'South Cambridgeshire', 'Allerdale', 'Copeland', 'Eden', 'South Lakeland', 
          'Amber Valley','Derbyshire Dales', 'Erewash','High Peak', 'North East Derbyshire', 
          'South Derbyshire','East Devon', 'Mid Devon', 'North Devon', 'South Hams',
          'Teignbridge', 'Torridge', 'West Devon','Rother', 'Wealden', 'Castle Point', 
          'Epping Forest','Tendring', 'Uttlesford','Cotswold', 'Forest of Dean',
          'Basingstoke and Deane', 'East Hampshire','Hart', 'New Forest','Rushmoor', 
          'Test Valley', 'Dacorum','Hertsmere', 'North Hertfordshire', 'Three Rivers', 
          'Gravesham','Folkestone and Hythe', 'Swale','Thanet', 'Tonbridge and Malling', 
          'Fylde', 'Hyndburn', 'Pendle', 'Ribble Valley', 'Rossendale', 'South Ribble', 
          'West Lancashire','Wyre', 'Blaby', 'Charnwood', 'Harborough','Hinckley and Bosworth', 
          'Melton', 'North West Leicestershire','Oadby and Wigston', 'East Lindsey', 
          'North Kesteven', 'South Holland', 'South Kesteven','West Lindsey', 'Broadland', 
          "King's Lynn and West Norfolk", 'North Norfolk', 'South Norfolk',
          'East Northamptonshire','South Northamptonshire','Richmondshire', 'Ryedale', 
          'Bassetlaw', 'Newark and Sherwood', 'Rushcliffe', 'Cherwell', 'South Oxfordshire', 
          'Vale of White Horse', 'West Oxfordshire','Mendip', 'Sedgemoor', 'South Somerset', 
          'Cannock Chase','East Staffordshire', 'South Staffordshire', 
          'Staffordshire Moorlands','Babergh', 'Mid Suffolk', 'Epsom and Ewell', 
          'Mole Valley','Reigate and Banstead', 'Runnymede', 'Spelthorne',
          'Surrey Heath','Tandridge', 'Waverley', 'North Warwickshire','Nuneaton and Bedworth', 
          'Adur', 'Arun', 'Mid Sussex','Malvern Hills', 'Wychavon', 'Wyre Forest', 
          'Welwyn Hatfield','East Hertfordshire', 'East Suffolk', 'West Suffolk',
          'Somerset West and Taunton', 'Tameside','North Tyneside','South Tyneside', 
          'Barking and Dagenham', 'Barnet', 'Bexley', 'Brent''Buckinghamshire', 
          'Cambridgeshire', 'Cumbria', 'Derbyshire','Devon', 'East Sussex', 'Essex', 
          'Gloucestershire', 'Hampshire','Hertfordshire', 'Kent', 'Lancashire', 
          'Leicestershire','Lincolnshire', 'Norfolk', 'Northamptonshire', 
          'North Yorkshire','Nottinghamshire', 'Oxfordshire', 'Somerset', 'Staffordshire',
          'Suffolk', 'Surrey', 'Warwickshire', 'West Sussex','Worcestershire']


# In[ ]:


Region =['North East', 'North West','Yorkshire and The Humber', 'East Midlands', 
         'West Midlands','East of England', 'London', 'South East', 'South West']

