"""lookup tables for UK GTFS locations."""


# # # # CONSTANTS # # # #

REGION_CODE_TO_NAME = {
    "EA": "East Anglia",
    "EM": "East Midlands",
    "SE-LONDON": "South East & London",
    "NE": "North East England",
    "NW": "North West England",
    "S": "Scotland",
    "SW": "South West England",
    "W": "Wales",
    "WM": "West Midlands",
    "Y": "Yorkshire",
}


# This mapping allows a city, county, combined authority, or region name to
# resolve to one of the regional feeds supplied by the repository.
#
# Add further aliases here if you encounter a place that is not recognised.
PLACE_TO_REGION = {
    # -----------------------------------------------------------------------
    # East Anglia
    # -----------------------------------------------------------------------
    "east anglia": "East Anglia",
    "bedford": "East Anglia",
    "bedfordshire": "East Anglia",
    "cambridge": "East Anglia",
    "cambridgeshire": "East Anglia",
    "ely": "East Anglia",
    "ipswich": "East Anglia",
    "luton": "East Anglia",
    "norfolk": "East Anglia",
    "norwich": "East Anglia",
    "peterborough": "East Anglia",
    "suffolk": "East Anglia",

    # -----------------------------------------------------------------------
    # East Midlands
    # -----------------------------------------------------------------------
    "east midlands": "East Midlands",
    "derby": "East Midlands",
    "derbyshire": "East Midlands",
    "leicester": "East Midlands",
    "leicestershire": "East Midlands",
    "lincoln": "East Midlands",
    "lincolnshire": "East Midlands",
    "northampton": "East Midlands",
    "northamptonshire": "East Midlands",
    "nottingham": "East Midlands",
    "nottinghamshire": "East Midlands",
    "rutland": "East Midlands",

    # -----------------------------------------------------------------------
    # South East England and London
    # -----------------------------------------------------------------------
    "south east": "South East & London",
    "south east england": "South East & London",
    "london": "South East & London",
    "greater london": "South East & London",
    "berkshire": "South East & London",
    "brighton": "South East & London",
    "brighton and hove": "South East & London",
    "buckinghamshire": "South East & London",
    "canterbury": "South East & London",
    "chelmsford": "South East & London",
    "east sussex": "South East & London",
    "essex": "South East & London",
    "guildford": "South East & London",
    "hampshire": "South East & London",
    "hertfordshire": "South East & London",
    "isle of wight": "South East & London",
    "kent": "South East & London",
    "medway": "South East & London",
    "milton keynes": "South East & London",
    "oxford": "South East & London",
    "oxfordshire": "South East & London",
    "portsmouth": "South East & London",
    "reading": "South East & London",
    "slough": "South East & London",
    "southampton": "South East & London",
    "surrey": "South East & London",
    "west sussex": "South East & London",

    # -----------------------------------------------------------------------
    # North East England
    # -----------------------------------------------------------------------
    "north east": "North East England",
    "north east england": "North East England",
    "county durham": "North East England",
    "darlington": "North East England",
    "durham": "North East England",
    "gateshead": "North East England",
    "hartlepool": "North East England",
    "middlesbrough": "North East England",
    "newcastle": "North East England",
    "newcastle upon tyne": "North East England",
    "north tyneside": "North East England",
    "northumberland": "North East England",
    "redcar": "North East England",
    "redcar and cleveland": "North East England",
    "south tyneside": "North East England",
    "stockton": "North East England",
    "stockton on tees": "North East England",
    "sunderland": "North East England",
    "tees valley": "North East England",
    "tyne and wear": "North East England",

    # -----------------------------------------------------------------------
    # North West England
    # -----------------------------------------------------------------------
    "north west": "North West England",
    "north west england": "North West England",
    "blackburn": "North West England",
    "blackburn with darwen": "North West England",
    "blackpool": "North West England",
    "bolton": "North West England",
    "bury": "North West England",
    "carlisle": "North West England",
    "chester": "North West England",
    "cheshire": "North West England",
    "cheshire east": "North West England",
    "cheshire west": "North West England",
    "cheshire west and chester": "North West England",
    "cumbria": "North West England",
    "greater manchester": "North West England",
    "halton": "North West England",
    "knowsley": "North West England",
    "lancashire": "North West England",
    "liverpool": "North West England",
    "manchester": "North West England",
    "merseyside": "North West England",
    "oldham": "North West England",
    "preston": "North West England",
    "rochdale": "North West England",
    "salford": "North West England",
    "sefton": "North West England",
    "st helens": "North West England",
    "stockport": "North West England",
    "tameside": "North West England",
    "trafford": "North West England",
    "warrington": "North West England",
    "wigan": "North West England",
    "wirral": "North West England",

    # -----------------------------------------------------------------------
    # Scotland
    # -----------------------------------------------------------------------
    "scotland": "Scotland",
    "aberdeen": "Scotland",
    "aberdeenshire": "Scotland",
    "dundee": "Scotland",
    "edinburgh": "Scotland",
    "falkirk": "Scotland",
    "fife": "Scotland",
    "glasgow": "Scotland",
    "highland": "Scotland",
    "inverness": "Scotland",
    "perth": "Scotland",
    "stirling": "Scotland",

    # -----------------------------------------------------------------------
    # South West England
    # -----------------------------------------------------------------------
    "south west": "South West England",
    "south west england": "South West England",
    "bath": "South West England",
    "bath and north east somerset": "South West England",
    "bournemouth": "South West England",
    "bristol": "South West England",
    "cornwall": "South West England",
    "devon": "South West England",
    "dorset": "South West England",
    "exeter": "South West England",
    "gloucester": "South West England",
    "gloucestershire": "South West England",
    "north somerset": "South West England",
    "plymouth": "South West England",
    "poole": "South West England",
    "somerset": "South West England",
    "south gloucestershire": "South West England",
    "swindon": "South West England",
    "torbay": "South West England",
    "truro": "South West England",
    "wiltshire": "South West England",

    # -----------------------------------------------------------------------
    # Wales
    # -----------------------------------------------------------------------
    "wales": "Wales",
    "aberystwyth": "Wales",
    "bangor": "Wales",
    "bridgend": "Wales",
    "caerphilly": "Wales",
    "cardiff": "Wales",
    "carmarthenshire": "Wales",
    "ceredigion": "Wales",
    "conwy": "Wales",
    "denbighshire": "Wales",
    "flintshire": "Wales",
    "gwynedd": "Wales",
    "merthyr tydfil": "Wales",
    "monmouthshire": "Wales",
    "neath port talbot": "Wales",
    "newport": "Wales",
    "pembrokeshire": "Wales",
    "powys": "Wales",
    "rhondda cynon taf": "Wales",
    "swansea": "Wales",
    "torfaen": "Wales",
    "wrexham": "Wales",

    # -----------------------------------------------------------------------
    # West Midlands
    # -----------------------------------------------------------------------
    "west midlands": "West Midlands",
    "birmingham": "West Midlands",
    "coventry": "West Midlands",
    "dudley": "West Midlands",
    "hereford": "West Midlands",
    "herefordshire": "West Midlands",
    "sandwell": "West Midlands",
    "shropshire": "West Midlands",
    "solihull": "West Midlands",
    "staffordshire": "West Midlands",
    "stoke": "West Midlands",
    "stoke on trent": "West Midlands",
    "telford": "West Midlands",
    "telford and wrekin": "West Midlands",
    "walsall": "West Midlands",
    "warwick": "West Midlands",
    "warwickshire": "West Midlands",
    "wolverhampton": "West Midlands",
    "worcester": "West Midlands",
    "worcestershire": "West Midlands",

    # -----------------------------------------------------------------------
    # Yorkshire
    # -----------------------------------------------------------------------
    "yorkshire": "Yorkshire",
    "barnsley": "Yorkshire",
    "bradford": "Yorkshire",
    "calderdale": "Yorkshire",
    "doncaster": "Yorkshire",
    "east riding": "Yorkshire",
    "east riding of yorkshire": "Yorkshire",
    "halifax": "Yorkshire",
    "harrogate": "Yorkshire",
    "huddersfield": "Yorkshire",
    "hull": "Yorkshire",
    "kingston upon hull": "Yorkshire",
    "kirklees": "Yorkshire",
    "leeds": "Yorkshire",
    "north yorkshire": "Yorkshire",
    "rotherham": "Yorkshire",
    "scarborough": "Yorkshire",
    "sheffield": "Yorkshire",
    "south yorkshire": "Yorkshire",
    "wakefield": "Yorkshire",
    "west yorkshire": "Yorkshire",
    "york": "Yorkshire",
}
