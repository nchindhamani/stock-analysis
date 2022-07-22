# NSE Stocks - Analysis
Financial web application that provides financial charts for NSE stocks and gives a glimpse of Sector-wise latest stock prices. 

Allows Traders and Investors to create account to keep track of their Portfolio and create Wishlist. 

It is built using Flask Framework, SQLite DB, Bootstrap, Html, css.

# REST API - NSE Industry-wise OHLC
This API returns JSON that contains industry-wise OHLC (Open High Low Close) data in the last traded session. 
# API Parameter - 
Required: Industry name. The following values are supported. 

'Electrical Equipment' 
'Gas' 
'Auto Components'
'Pharmaceuticals & Biotechnology' 
'Finance' 
'Chemicals & Petrochemicals'
'Realty' 
'Leisure Services' 
'Textiles & Apparels'
'Industrial Manufacturing' 
'Consumer Durables'
'Agricultural Food & other Products' 
'Automobiles'
'Paper, Forest & Jute Products'
'Agricultural, Commercial & Construction Vehicles' 
'Aerospace & Defense'
'Ferrous Metals' 
'Telecom -  Equipment & Accessories' 
'Capital Markets'
'Industrial Products' 
'Power' 
'Fertilizers & Agrochemicals'
'Personal Products' 
'Petroleum Products' 
'Telecom - Services' 
'Banks'
'Oil' 
'Commercial Services & Supplies' 
'Cigarettes & Tobacco Products'
'Food Products' 
'IT - Hardware' 
'Construction' 
'Non - Ferrous Metals'
'Entertainment' 
'IT - Software' 
'Minerals & Mining'
'Cement & Cement Products' 
'Retailing' 
'Insurance' 
'Transport Services'
'Diversified Metals' 
'Other Consumer Services' 
'IT - Services'
'Diversified FMCG' 
'Other Construction Materials' 
'Household Products'
'Metals & Minerals Trading' 
'Beverages' 
'Diversified'
'Healthcare Services' 
'Printing & Publication' 
'Media'
'Transport Infrastructure' 
'Engineering Services' 
'Consumable Fuels'
'Healthcare Equipment & Supplies' 
'Other Utilities' 
'Others'
'Financial Technology (Fintech)'

# Sample Output for Parameter 'Oil'
{
ABAN: {
CLOSE: 45.35,
Change %: 0.0030000000000000426,
HIGH: 46.7,
LOW: 44.9,
NAME_OF_COMPANY: "Aban Offshore Ltd.,",
OPEN: 45.4
},
ALPHAGEO: {
CLOSE: 284.2,
Change %: 0.06849999999999966,
HIGH: 292,
LOW: 274.9,
NAME_OF_COMPANY: "Alphageo (India)Ltd.",
OPEN: 275
},
ASIANENE: {
CLOSE: 91.35,
Change %: 0.018999999999999916,
HIGH: 92.2,
LOW: 89.4,
NAME_OF_COMPANY: "ASIAN ENERGY SERVICES LTD",
OPEN: 91.15
},
DEEPENR: {
CLOSE: 82.3,
Change %: 0.020999999999999942,
HIGH: 84.2,
LOW: 79.2,
NAME_OF_COMPANY: "DEEP ENERGY RESOURCES LIMITED",
OPEN: 80.95
},
DEEPIND: {
CLOSE: 193.4,
Change %: 0.029000000000000057,
HIGH: 195,
LOW: 190.15,
NAME_OF_COMPANY: "Deep Industries Limited",
OPEN: 190.5
},
GANESHBE: {
CLOSE: 141.1,
Change %: 0.06599999999999995,
HIGH: 142.95,
LOW: 133.5,
NAME_OF_COMPANY: "Ganesh Benzoplast Ltd.,",
OPEN: 134
},
HINDOILEXP: {
CLOSE: 170.5,
Change %: 0.026500000000000058,
HIGH: 173.7,
LOW: 168.95,
NAME_OF_COMPANY: "Hindustan Oil Exploration Co. Ltd.",
OPEN: 171
},
JINDRILL: {
CLOSE: 187.45,
Change %: 0.08849999999999994,
HIGH: 187.5,
LOW: 178.7,
NAME_OF_COMPANY: "Jindal Drilling & Industries Ltd.,",
OPEN: 181
},
OIL: {
CLOSE: 186.6,
Change %: 0.02049999999999983,
HIGH: 189.35,
LOW: 185.05,
NAME_OF_COMPANY: "Oil India Limited",
OPEN: 187
},
ONGC: {
CLOSE: 127.9,
Change %: -0.02,
HIGH: 133.2,
LOW: 124.45,
NAME_OF_COMPANY: "Oil And Natural Gas Corporation Ltd",
OPEN: 130.5
},
SELAN: {
CLOSE: 186.45,
Change %: 0.2125,
HIGH: 193,
LOW: 165.6,
NAME_OF_COMPANY: "Selan Exploration Technology Ltd.",
OPEN: 167.45
}
}

