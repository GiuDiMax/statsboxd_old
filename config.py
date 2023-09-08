client_string = 'mongodb+srv://GiuDiMax:iiZBB9JYW07nqQcp@lbdcluster.bqbva.mongodb.net/Letterboxd?retryWrites=true&w=majority'
adminpsw = 'amicizia123'

field2 = ['actors', 'crew.director', 'crew.co-director', 'crew.additional-directing', 'crew.producer',
          'crew.executive-producer', 'crew.writer', 'crew.original-writer', 'crew.casting', 'crew.editor',
          'crew.cinematography', 'crew.additional-photography', 'crew.production-design', 'crew.art-direction',
          'crew.set-decoration', 'crew.special-effects', 'crew.visual-effects', 'crew.stunts', 'crew.choreography',
          'crew.composer', 'crew.songs', 'crew.sound', 'crew.costume-design', 'crew.makeup', 'crew.hairstyling']
          #'crew.studio']

field3 = ['country', 'studio', 'language', 'genres.main', 'genres.theme', 'genres.nanogenre'] #, 'genres.mini-themes']

field4 = ['country', 'year']

field5 = ['']

gen_l = ['drama', 'comedy', 'thriller', 'action', 'romance', 'animation', 'horror', 'documentary', 'crime', 'family', 'adventure', 'science-fiction', 'fantasy', 'mystery', 'music', 'tv-movie', 'history', 'war', 'western']
lan_l = ['no-spoken-language', 'english', 'japanese', 'french', 'italian', 'spanish', 'hindi', 'german', 'portuguese', 'russian', 'korean', 'malayalam', 'chinese', 'tamil', 'telugu', 'cantonese', 'swedish', 'arabic', 'turkish', 'no-spoken-language', 'polish', 'tagalog', 'bengali-bangla', 'dutch', 'danish', 'thai', 'norwegian', 'indonesian', 'czech', 'persianfarsi', 'greekmodern', 'hungarian', 'serbian', 'serbo-croatian', 'finnish', 'kannada', 'romanian', 'hebrewmodern', 'ukrainian', 'marathi-marathi', 'icelandic', 'georgian', 'malay', 'vietnamese', 'slovene', 'catalan', 'urdu', 'lithuanian', 'slovak', 'eastern-punjabi-eastern-panjabi', 'croatian', 'estonian', 'kazakh', 'albanian', 'bulgarian', 'armenian', 'galician', 'mongolian', 'basque', 'gujarati', 'latvian', 'macedonian', 'bosnian', 'amharic', 'kurdish', 'wolof', 'norwegian-bokmal', 'nepali', 'khmer', 'latin', 'afrikaans', 'tibetan-standard-tibetan-central', 'azerbaijani', 'irish', 'javanese', 'dzongkha', 'somali', 'kyrgyz', 'southern-sotho', 'quechua', 'burmese', 'pashto-pushto', 'lingala', 'bambara', 'assamese', 'kashmiri', 'sinhalese-sinhala', 'swahili', 'akan', 'lao', 'fula-fulah-pulaar-pular', 'belarusian', 'yiddish', 'northern-sami', 'maori', 'inuktitut', 'moldavian', 'zulu', 'aymara', 'kinyarwanda', 'hausa', 'navajo-navaho', 'xhosa', 'sardinian', 'tajik', 'inupiaq', 'samoan', 'igbo', 'tswana', 'uzbek', 'oromo', 'welsh', 'abkhaz', 'kalaallisut-greenlandic', 'esperanto', 'malagasy', 'maltese', 'twi', 'sundanese', 'haitian-haitian-creole']
cou_l = ['usa', 'france', 'uk', 'japan', 'india', 'italy', 'germany', 'canada', 'brazil', 'spain', 'south-korea', 'hong-kong', 'belgium', 'sweden', 'china', 'australia', 'russian-federation', 'mexico', 'argentina', 'ussr', 'netherlands', 'denmark', 'poland', 'turkey', 'switzerland', 'philippines', 'norway', 'ireland', 'egypt', 'austria', 'thailand', 'portugal', 'greece', 'taiwan', 'indonesia', 'chile', 'hungary', 'iran', 'finland', 'czechoslovakia', 'yugoslavia', 'new-zealand', 'czechia', 'romania', 'south-africa', 'serbia', 'israel', 'luxembourg', 'peru', 'colombia', 'qatar', 'ukraine', 'bulgaria', 'iceland', 'singapore', 'bangladesh', 'malaysia', 'croatia', 'morocco', 'slovenia', 'united-arab-emirates', 'cuba', 'uruguay', 'lithuania', 'estonia', 'slovakia', 'kazakhstan', 'lebanon', 'vietnam', 'latvia', 'state-of-palestine', 'dominican-republic', 'tunisia', 'algeria', 'bosnia-and-herzegovina', 'georgia', 'bolivarian-republic-of-venezuela', 'macedonia', 'pakistan', 'east-germany', 'senegal', 'cambodia', 'puerto-rico', 'nigeria', 'albania', 'saudi-arabia', 'ghana', 'malta', 'ecuador', 'kenya', 'afghanistan', 'mongolia', 'costa-rica', 'bolivia', 'jordan', 'iraq', 'belarus', 'montenegro', 'liechtenstein', 'ethiopia', 'kosovo', 'nepal', 'syrian-arab-republic', 'democratic-republic-of-congo', 'burkina-faso', 'guatemala', 'monaco', 'uganda', 'myanmar', 'paraguay', 'cyprus', 'north-korea', 'macao', 'panama', 'sri-lanka', 'angola', 'mali', 'haiti', 'rwanda', 'mauritania', 'cameroon', 'chad', 'kuwait', 'armenia', 'yemen', 'jamaica', 'lao-peoples-democratic-republic', 'libya', 'azerbaijan', 'sudan', 'bahamas-the', 'bhutan', 'ivory-coast', 'somalia', 'aruba', 'guinea-bissau', 'uzbekistan', 'greenland', 'kyrgyzstan', 'namibia', 'zimbabwe', 'tajikistan', 'nicaragua', 'djibouti', 'niger', 'eswatini', 'botswana', 'mozambique', 'madagascar', 'trinidad-and-tobago', 'moldova-the-republic-of', 'cape-verde', 'benin', 'congo', 'antarctica', 'malawi', 'zambia', 'lesotho', 'el-salvador', 'french-guiana', 'equatorial-guinea', 'martinique', 'guinea', 'guadeloupe', 'liberia', 'central-african-republic', 'guyana', 'svalbard-and-jan-mayen', 'serbia-and-montenegro', 'timor-leste', 'solomon-islands', 'netherlands-antilles', 'bahrain', 'suriname', 'andorra', 'honduras', 'papua-new-guinea', 'new-caledonia', 'oman', 'virgin-islands-british', 'faroe-islands', 'anguilla', 'antigua-and-barbuda', 'sierra-leone', 'fiji', 'brunei-darussalam', 'sao-tome-and-principe', 'tuvalu', 'san-marino', 'grenada', 'gambia', 'turks-and-caicos-islands', 'samoa', 'dominica', 'barbados', 'nauru', 'french-southern-territories', 'cocos-keeling-islands', 'vanuatu', 'french-polynesia', 'palau', 'holy-see', 'eritrea', 'cayman-islands', 'heard-island-and-mcdonald-islands', 'american-samoa', 'togo', 'christmas-island', 'mauritius', 'saint-pierre-and-miquelon', 'burundi', 'south-sudan', 'pitcairn', 'western-sahara', 'belize', 'gabon', 'swaziland', 'wallis-and-futuna', 'sint-maarten-dutch-part', 'gibraltar', 'saint-barthelemy', 'bonaire-sint-eustatius-and-saba', 'guernsey', 'aland-islands', 'bouvet-island', 'norfolk-island', 'curacao', 'kiribati', 'maldives', 'mayotte', 'niue', 'cook-islands', 'saint-lucia', 'saint-martin-french-part', 'federated-states-of-micronesia', 'reunion', 'saint-vincent-and-the-grenadines', 'united-states-minor-outlying-islands', 'jersey', 'montserrat', 'northern-mariana-islands', 'saint-kitts-and-nevis', 'south-georgia-and-the-south-sandwich-islands', 'tonga', 'isle-of-man', 'british-indian-ocean-territory', 'comoros', 'guam', 'marshall-islands', 'saint-helena-ascension-and-tristan-da-cunha', 'seychelles', 'us-virgin-islands', 'bermuda', 'turkmenistan', 'united-republic-of-tanzania', 'falkland-islands', 'tokelau']

api_tmdb = '6fff7e293df6a808b97101a26c86a545'

listsSelection = [
    ['dave/list/official-top-250-narrative-feature-films', 'Letterboxd Top 250', 1],
    ['dave/list/imdb-top-250', 'IMDb Top 250', 2],
    ['jake_ziegler/list/academy-award-winners-for-best-picture', 'Oscar Best Picture Winners', 3],
    ['brsan/list/cannes-palme-dor-winners', 'Cannes’ Palme d’Or Winners', 4],
    ['matthew/list/box-office-mojo-all-time-worldwide', 'Box Office Mojo All Time 100', 5],
    ['moseschan/list/afi-100-years-100-movies', 'AFI 100 Years 100 Movies', 6],
    ['bfi/list/sight-and-sounds-greatest-films-of-all-time', 'Sight & Sound Greatest Films', 7],
    ['gubarenko/list/1001-movies-you-must-see-before-you-die-2021', '1,001 To See Before You Die', 8],
    ['crew/list/edgar-wrights-1000-favorite-movies', 'Edgar Wright’s 1,000 Favorites', 9],
    ['dvideostor/list/roger-eberts-great-movies', 'Roger Ebert’s Great Movies', 10],
    ['jack/list/women-directors-the-official-top-250-narrative', 'Top 250 Women-Directed', 11],
    ['jack/list/black-directors-the-official-top-100-narrative', 'Top 100 Black-Directed', 12],
    ['jack/list/official-top-250-films-with-the-most-fans', 'Top 250 Most Fans', 14],
    ['jack/list/official-top-250-documentary-films', 'Top 250 Documentaries', 14],
    ['lifeasfiction/list/letterboxd-100-animation', 'Top 100 Animation', 15],
    ['darrencb/list/letterboxds-top-250-horror-films', 'Top 250 Horror', 16],
]

crew_html = [
    ['crew_co-director', 'co-director', 'Co-Directors'],
    ['crew_additional-directing', 'additional-directing', 'Add. Directing'],
    ['crew_producer', 'producer', 'Producers'], ['crew_executive-producer', 'executive-producer', 'Exec. Producer'],
    ['crew_writer', 'writer', 'Writers'], ['crew_original-writer', 'original-writer', 'Original Writers'],
    ['crew_casting', 'casting', 'Casting'], ['crew_editor', 'editor', 'Editors'],
    ['crew_cinematography', 'cinematography', 'cinematography'],
    ['crew_additional-photography', 'additional-photography', 'Add. Photography'],
    ['crew_production-design', 'production-design', 'Production Design'],
    ['crew_art-direction', 'art-direction', 'Art Direction'],
    ['crew_set-decoration', 'set-decoration', 'Set Decoration'],
    ['crew_special-effects', 'special-effects', 'Special Effects'],
    ['crew_visual-effects', 'visual-effects', 'Visual Effects'], ['crew_stunts', 'stunts', 'Stunts'],
    ['crew_choreography', 'choreography', 'Choreography'], ['crew_composer', 'composer', 'Composers'],
    ['crew_songs', 'songs', 'Songs'], ['crew_sound', 'sound', 'Sound'],
    ['crew_costume-design', 'costume-design', 'Costume Design'], ['crew_makeup', 'makeup', 'Makeup'],
    ['crew_hairstyling', 'hairstyling', 'Hairstyling'], ['studio', 'studio', 'Studios']
]

exclude_people_old = [155375, 85155, 95749, 77577]

exclude_people = ['mickie-mcgowan', 'stan-lee', 'jack-angel', 'sherry-lynn', 'fred-tatasciore', 'jim-cummings',
                      'frank-welker', 'laraine-newman', 'bob-bergen', 'jess-harnell', 'jan-rabson', 'bob-peterson',
                      'fred-tatasciore', 'dee-bradley-baker', 'grey-delisle', 'tara-strong', 'scott-menville',
                      'mona-marshall', 'danny-mann', 'bill-farmer', 'terri-douglas', 'david-cowgill', 'lori-alan',
                      'debi-derryberry', 'kari-wahlgren', 'john-cygan', 'jackie-gonneau']

users_list_url = 'https://gist.githubusercontent.com/GiuDiMax/84c8ba608c932d4671d5fe83d5f5e9c4/raw/users_lbd'
