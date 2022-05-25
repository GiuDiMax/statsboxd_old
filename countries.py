from mongodb import db

x = {
    'AF': {
        'count': 165,
        'label': 'Afghanistan',
        'url': 'afghanistan'
    },

    'AL': {
        'count': 321,
        'label': 'Albania',
        'url': 'albania'
    },

    'DZ': {
        'count': 287,
        'label': 'Algeria',
        'url': 'algeria'
    },

    'AS': {
        'count': 7,
        'label': 'American Samoa',
        'url': 'american-samoa'
    },

    'AD': {
        'count': 17,
        'label': 'Andorra',
        'url': 'andorra'
    },

    'AO': {
        'count': 63,
        'label': 'Angola',
        'url': 'angola'
    },

    'AI': {
        'count': 4,
        'label': 'Anguilla',
        'url': 'anguilla'
    },

    'AQ': {
        'count': 13,
        'label': 'Antarctica',
        'url': 'antarctica'
    },

    'AG': {
        'count': 9,
        'label': 'Antigua and Barbuda',
        'url': 'antigua-and-barbuda'
    },

    'AR': {
        'count': 6420,
        'label': 'Argentina',
        'url': 'argentina'
    },

    'AM': {
        'count': 155,
        'label': 'Armenia',
        'url': 'armenia'
    },

    'AW': {
        'count': 17,
        'label': 'Aruba',
        'url': 'aruba'
    },

    'AU': {
        'count': 5395,
        'label': 'Australia',
        'url': 'australia'
    },

    'AT': {
        'count': 4307,
        'label': 'Austria',
        'url': 'austria'
    },

    'AZ': {
        'count': 137,
        'label': 'Azerbaijan',
        'url': 'azerbaijan'
    },

    'BS': {
        'count': 32,
        'label': 'Bahamas',
        'url': 'bahamas-the'
    },

    'BH': {
        'count': 23,
        'label': 'Bahrain',
        'url': 'bahrain'
    },

    'BD': {
        'count': 573,
        'label': 'Bangladesh',
        'url': 'bangladesh'
    },

    'BB': {
        'count': 23,
        'label': 'Barbados',
        'url': 'barbados'
    },

    'BY': {
        'count': 344,
        'label': 'Belarus',
        'url': 'belarus'
    },

    'BE': {
        'count': 4066,
        'label': 'Belgium',
        'url': 'belgium'
    },

    'BZ': {
        'count': 12,
        'label': 'Belize',
        'url': 'belize'
    },

    'BJ': {
        'count': 29,
        'label': 'Benin',
        'url': 'benin'
    },

    'BM': {
        'count': 9,
        'label': 'Bermuda',
        'url': 'bermuda'
    },

    'BT': {
        'count': 34,
        'label': 'Bhutan',
        'url': 'bhutan'
    },

    'VE': {
        'count': 437,
        'label': 'Bolivarian Republic of Venezuela',
        'url': 'bolivarian-republic-of-venezuela'
    },

    'BO': {
        'count': 181,
        'label': 'Bolivia',
        'url': 'bolivia'
    },

    'BA': {
        'count': 386,
        'label': 'Bosnia and Herzegovina',
        'url': 'bosnia-and-herzegovina'
    },

    'BW': {
        'count': 27,
        'label': 'Botswana',
        'url': 'botswana'
    },

    'BV': {
        'count': 2,
        'label': 'Bouvet Island',
        'url': 'bouvet-island'
    },

    'BR': {
        'count': 11688,
        'label': 'Brazil',
        'url': 'brazil'
    },

    'IO': {
        'count': 2,
        'label': 'British Indian Ocean Territory',
        'url': 'british-indian-ocean-territory'
    },

    'VG': {
        'count': 6,
        'label': 'British Virgin Islands',
        'url': 'virgin-islands-british'
    },

    'BN': {
        'count': 18,
        'label': 'Brunei Darussalam',
        'url': 'brunei-darussalam'
    },

    'BG': {
        'count': 840,
        'label': 'Bulgaria',
        'url': 'bulgaria'
    },

    'BF': {
        'count': 115,
        'label': 'Burkina Faso',
        'url': 'burkina-faso'
    },

    'BI': {
        'count': 11,
        'label': 'Burundi',
        'url': 'burundi'
    },

    'KH': {
        'count': 205,
        'label': 'Cambodia',
        'url': 'cambodia'
    },

    'CM': {
        'count': 109,
        'label': 'Cameroon',
        'url': 'cameroon'
    },

    'CA': {
        'count': 16183,
        'label': 'Canada',
        'url': 'canada'
    },

    'CV': {
        'count': 29,
        'label': 'Cape Verde',
        'url': 'cape-verde'
    },

    'KY': {
        'count': 9,
        'label': 'Cayman Islands',
        'url': 'cayman-islands'
    },

    'CF': {
        'count': 21,
        'label': 'Central African Republic',
        'url': 'central-african-republic'
    },

    'TD': {
        'count': 27,
        'label': 'Chad',
        'url': 'chad'
    },

    'CL': {
        'count': 1801,
        'label': 'Chile',
        'url': 'chile'
    },

    'CN': {
        'count': 7796,
        'label': 'China',
        'url': 'china'
    },

    'CX': {
        'count': 4,
        'label': 'Christmas Island',
        'url': 'christmas-island'
    },

    'CC': {
        'count': 1,
        'label': 'Cocos (Keeling) Islands',
        'url': 'cocos-keeling-islands'
    },

    'CO': {
        'count': 1022,
        'label': 'Colombia',
        'url': 'colombia'
    },

    'KM': {
        'count': 7,
        'label': 'Comoros',
        'url': 'comoros'
    },

    'CG': {
        'count': 24,
        'label': 'Congo',
        'url': 'congo'
    },

    'CK': {
        'count': 6,
        'label': 'Cook Islands',
        'url': 'cook-islands'
    },

    'CR': {
        'count': 190,
        'label': 'Costa Rica',
        'url': 'costa-rica'
    },

    'HR': {
        'count': 860,
        'label': 'Croatia',
        'url': 'croatia'
    },

    'CU': {
        'count': 645,
        'label': 'Cuba',
        'url': 'cuba'
    },

    'CY': {
        'count': 103,
        'label': 'Cyprus',
        'url': 'cyprus'
    },

    'CZ': {
        'count': 2564,
        'label': 'Czechia',
        'url': 'czechia'
    },

    'XC': {
        'count': 4305,
        'label': 'Czechoslovakia',
        'url': 'czechoslovakia'
    },

    'CD': {
        'count': 86,
        'label': 'Democratic Republic of Congo',
        'url': 'democratic-republic-of-congo'
    },

    'DK': {
        'count': 4018,
        'label': 'Denmark',
        'url': 'denmark'
    },

    'DJ': {
        'count': 8,
        'label': 'Djibouti',
        'url': 'djibouti'
    },

    'DM': {
        'count': 11,
        'label': 'Dominica',
        'url': 'dominica'
    },

    'DO': {
        'count': 282,
        'label': 'Dominican Republic',
        'url': 'dominican-republic'
    },

    'XG': {
        'count': 920,
        'label': 'East Germany',
        'url': 'east-germany'
    },

    'EC': {
        'count': 311,
        'label': 'Ecuador',
        'url': 'ecuador'
    },

    'EG': {
        'count': 1750,
        'label': 'Egypt',
        'url': 'egypt'
    },

    'SV': {
        'count': 54,
        'label': 'El Salvador',
        'url': 'el-salvador'
    },

    'GQ': {
        'count': 10,
        'label': 'Equatorial Guinea',
        'url': 'equatorial-guinea'
    },

    'ER': {
        'count': 15,
        'label': 'Eritrea',
        'url': 'eritrea'
    },

    'EE': {
        'count': 682,
        'label': 'Estonia',
        'url': 'estonia'
    },

    'ET': {
        'count': 112,
        'label': 'Ethiopia',
        'url': 'ethiopia'
    },

    'FK': {
        'count': 5,
        'label': 'Falkland Islands',
        'url': 'falkland-islands'
    },

    'FO': {
        'count': 27,
        'label': 'Faroe Islands',
        'url': 'faroe-islands'
    },

    'FM': {
        'count': 3,
        'label': 'Federated States of Micronesia',
        'url': 'federated-states-of-micronesia'
    },

    'FJ': {
        'count': 19,
        'label': 'Fiji',
        'url': 'fiji'
    },

    'FI': {
        'count': 3200,
        'label': 'Finland',
        'url': 'finland'
    },

    'FR': {
        'count': 32337,
        'label': 'France',
        'url': 'france'
    },

    'GF': {
        'count': 9,
        'label': 'French Guiana',
        'url': 'french-guiana'
    },

    'PF': {
        'count': 15,
        'label': 'French Polynesia',
        'url': 'french-polynesia'
    },

    'TF': {
        'count': 1,
        'label': 'French Southern Territories',
        'url': 'french-southern-territories'
    },

    'GA': {
        'count': 19,
        'label': 'Gabon',
        'url': 'gabon'
    },

    'GM': {
        'count': 10,
        'label': 'Gambia',
        'url': 'gambia'
    },

    'GE': {
        'count': 260,
        'label': 'Georgia',
        'url': 'georgia'
    },

    'DE': {
        'count': 32698,
        'label': 'Germany',
        'url': 'germany'
    },

    'GH': {
        'count': 167,
        'label': 'Ghana',
        'url': 'ghana'
    },

    'GI': {
        'count': 3,
        'label': 'Gibraltar',
        'url': 'gibraltar'
    },

    'GR': {
        'count': 2843,
        'label': 'Greece',
        'url': 'greece'
    },

    'GL': {
        'count': 45,
        'label': 'Greenland',
        'url': 'greenland'
    },

    'GD': {
        'count': 9,
        'label': 'Grenada',
        'url': 'grenada'
    },

    'GP': {
        'count': 15,
        'label': 'Guadeloupe',
        'url': 'guadeloupe'
    },

    'GU': {
        'count': 10,
        'label': 'Guam',
        'url': 'guam'
    },

    'GT': {
        'count': 124,
        'label': 'Guatemala',
        'url': 'guatemala'
    },

    'GN': {
        'count': 23,
        'label': 'Guinea',
        'url': 'guinea'
    },

    'GW': {
        'count': 23,
        'label': 'Guinea-Bissau',
        'url': 'guinea-bissau'
    },

    'GY': {
        'count': 12,
        'label': 'Guyana',
        'url': 'guyana'
    },

    'HT': {
        'count': 67,
        'label': 'Haiti',
        'url': 'haiti'
    },

    'HM': {
        'count': 2,
        'label': 'Heard Island and McDonald Islands',
        'url': 'heard-island-and-mcdonald-islands'
    },

    'VA': {
        'count': 8,
        'label': 'Holy See',
        'url': 'holy-see'
    },

    'HN': {
        'count': 65,
        'label': 'Honduras',
        'url': 'honduras'
    },

    'HK': {
        'count': 5479,
        'label': 'Hong Kong',
        'url': 'hong-kong'
    },

    'HU': {
        'count': 2330,
        'label': 'Hungary',
        'url': 'hungary'
    },

    'IS': {
        'count': 533,
        'label': 'Iceland',
        'url': 'iceland'
    },

    'IN': {
        'count': 16130,
        'label': 'India',
        'url': 'india'
    },

    'ID': {
        'count': 3026,
        'label': 'Indonesia',
        'url': 'indonesia'
    },

    'IR': {
        'count': 2103,
        'label': 'Iran',
        'url': 'iran'
    },

    'IQ': {
        'count': 151,
        'label': 'Iraq',
        'url': 'iraq'
    },

    'IE': {
        'count': 1732,
        'label': 'Ireland',
        'url': 'ireland'
    },

    'IL': {
        'count': 1689,
        'label': 'Israel',
        'url': 'israel'
    },

    'IT': {
        'count': 14187,
        'label': 'Italy',
        'url': 'italy'
    },

    'CI': {
        'count': 39,
        'label': 'Ivory Coast',
        'url': 'ivory-coast'
    },

    'JM': {
        'count': 62,
        'label': 'Jamaica',
        'url': 'jamaica'
    },

    'JP': {
        'count': 26172,
        'label': 'Japan',
        'url': 'japan'
    },

    'JO': {
        'count': 93,
        'label': 'Jordan',
        'url': 'jordan'
    },

    'KZ': {
        'count': 277,
        'label': 'Kazakhstan',
        'url': 'kazakhstan'
    },

    'KE': {
        'count': 133,
        'label': 'Kenya',
        'url': 'kenya'
    },

    'KI': {
        'count': 10,
        'label': 'Kiribati',
        'url': 'kiribati'
    },

    'XK': {
        'count': 86,
        'label': 'Kosovo',
        'url': 'kosovo'
    },

    'KW': {
        'count': 89,
        'label': 'Kuwait',
        'url': 'kuwait'
    },

    'KG': {
        'count': 62,
        'label': 'Kyrgyzstan',
        'url': 'kyrgyzstan'
    },

    'LA': {
        'count': 41,
        'label': 'Lao People\'s Democratic Republic',
        'url': 'lao-peoples-democratic-republic'
    },

    'LV': {
        'count': 1103,
        'label': 'Latvia',
        'url': 'latvia'
    },

    'LB': {
        'count': 489,
        'label': 'Lebanon',
        'url': 'lebanon'
    },

    'LS': {
        'count': 14,
        'label': 'Lesotho',
        'url': 'lesotho'
    },

    'LR': {
        'count': 13,
        'label': 'Liberia',
        'url': 'liberia'
    },

    'LY': {
        'count': 26,
        'label': 'Libya',
        'url': 'libya'
    },

    'LI': {
        'count': 33,
        'label': 'Liechtenstein',
        'url': 'liechtenstein'
    },

    'LT': {
        'count': 471,
        'label': 'Lithuania',
        'url': 'lithuania'
    },

    'LU': {
        'count': 408,
        'label': 'Luxembourg',
        'url': 'luxembourg'
    },

    'MO': {
        'count': 145,
        'label': 'Macao',
        'url': 'macao'
    },

    'MK': {
        'count': 413,
        'label': 'Macedonia',
        'url': 'macedonia'
    },

    'MG': {
        'count': 33,
        'label': 'Madagascar',
        'url': 'madagascar'
    },

    'MW': {
        'count': 17,
        'label': 'Malawi',
        'url': 'malawi'
    },

    'MY': {
        'count': 1221,
        'label': 'Malaysia',
        'url': 'malaysia'
    },

    'MV': {
        'count': 19,
        'label': 'Maldives',
        'url': 'maldives'
    },

    'ML': {
        'count': 62,
        'label': 'Mali',
        'url': 'mali'
    },

    'MT': {
        'count': 65,
        'label': 'Malta',
        'url': 'malta'
    },

    'MH': {
        'count': 10,
        'label': 'Marshall Islands',
        'url': 'marshall-islands'
    },

    'MQ': {
        'count': 15,
        'label': 'Martinique',
        'url': 'martinique'
    },

    'MR': {
        'count': 26,
        'label': 'Mauritania',
        'url': 'mauritania'
    },

    'MU': {
        'count': 17,
        'label': 'Mauritius',
        'url': 'mauritius'
    },

    'YT': {
        'count': 6,
        'label': 'Mayotte',
        'url': 'mayotte'
    },

    'MX': {
        'count': 9801,
        'label': 'Mexico',
        'url': 'mexico'
    },

    'MC': {
        'count': 33,
        'label': 'Monaco',
        'url': 'monaco'
    },

    'MN': {
        'count': 114,
        'label': 'Mongolia',
        'url': 'mongolia'
    },

    'ME': {
        'count': 77,
        'label': 'Montenegro',
        'url': 'montenegro'
    },

    'MS': {
        'count': 4,
        'label': 'Montserrat',
        'url': 'montserrat'
    },

    'MA': {
        'count': 388,
        'label': 'Morocco',
        'url': 'morocco'
    },

    'MZ': {
        'count': 61,
        'label': 'Mozambique',
        'url': 'mozambique'
    },

    'MM': {
        'count': 108,
        'label': 'Myanmar',
        'url': 'myanmar'
    },

    'NA': {
        'count': 43,
        'label': 'Namibia',
        'url': 'namibia'
    },

    'NR': {
        'count': 3,
        'label': 'Nauru',
        'url': 'nauru'
    },

    'NP': {
        'count': 225,
        'label': 'Nepal',
        'url': 'nepal'
    },

    'NL': {
        'count': 4777,
        'label': 'Netherlands',
        'url': 'netherlands'
    },

    'AN': {
        'count': 14,
        'label': 'Netherlands Antilles',
        'url': 'netherlands-antilles'
    },

    'NC': {
        'count': 18,
        'label': 'New Caledonia',
        'url': 'new-caledonia'
    },

    'NZ': {
        'count': 1136,
        'label': 'New Zealand',
        'url': 'new-zealand'
    },

    'NI': {
        'count': 62,
        'label': 'Nicaragua',
        'url': 'nicaragua'
    },

    'NE': {
        'count': 42,
        'label': 'Niger',
        'url': 'niger'
    },

    'NG': {
        'count': 472,
        'label': 'Nigeria',
        'url': 'nigeria'
    },

    'NU': {
        'count': 3,
        'label': 'Niue',
        'url': 'niue'
    },

    'NF': {
        'count': 1,
        'label': 'Norfolk Island',
        'url': 'norfolk-island'
    },

    'MP': {
        'count': 7,
        'label': 'Northern Mariana Islands',
        'url': 'northern-mariana-islands'
    },

    'KP': {
        'count': 126,
        'label': 'North Korea',
        'url': 'north-korea'
    },

    'NO': {
        'count': 2999,
        'label': 'Norway',
        'url': 'norway'
    },

    'OM': {
        'count': 15,
        'label': 'Oman',
        'url': 'oman'
    },

    'PK': {
        'count': 452,
        'label': 'Pakistan',
        'url': 'pakistan'
    },

    'PW': {
        'count': 5,
        'label': 'Palau',
        'url': 'palau'
    },

    'PA': {
        'count': 79,
        'label': 'Panama',
        'url': 'panama'
    },

    'PG': {
        'count': 43,
        'label': 'Papua New Guinea',
        'url': 'papua-new-guinea'
    },

    'PY': {
        'count': 109,
        'label': 'Paraguay',
        'url': 'paraguay'
    },

    'PE': {
        'count': 715,
        'label': 'Peru',
        'url': 'peru'
    },

    'PH': {
        'count': 5395,
        'label': 'Philippines',
        'url': 'philippines'
    },

    'PN': {
        'count': 2,
        'label': 'Pitcairn',
        'url': 'pitcairn'
    },

    'PL': {
        'count': 3497,
        'label': 'Poland',
        'url': 'poland'
    },

    'PT': {
        'count': 3181,
        'label': 'Portugal',
        'url': 'portugal'
    },

    'PR': {
        'count': 1089,
        'label': 'Puerto Rico',
        'url': 'puerto-rico'
    },

    'QA': {
        'count': 241,
        'label': 'Qatar',
        'url': 'qatar'
    },

    'MD': {
        'count': 45,
        'label': 'Republic of Moldova',
        'url': 'moldova-the-republic-of'
    },

    'RE': {
        'count': 13,
        'label': 'Réunion',
        'url': 'reunion'
    },

    'RO': {
        'count': 1468,
        'label': 'Romania',
        'url': 'romania'
    },

    'RU': {
        'count': 7414,
        'label': 'Russian Federation',
        'url': 'russian-federation'
    },

    'RW': {
        'count': 49,
        'label': 'Rwanda',
        'url': 'rwanda'
    },

    'SH': {
        'count': 3,
        'label': 'Saint Helena, Ascension and Tristan da Cunha',
        'url': 'saint-helena-ascension-and-tristan-da-cunha'
    },

    'KN': {
        'count': 5,
        'label': 'Saint Kitts and Nevis',
        'url': 'saint-kitts-and-nevis'
    },

    'LC': {
        'count': 7,
        'label': 'Saint Lucia',
        'url': 'saint-lucia'
    },

    'PM': {
        'count': 2,
        'label': 'Saint Pierre and Miquelon',
        'url': 'saint-pierre-and-miquelon'
    },

    'VC': {
        'count': 6,
        'label': 'Saint Vincent and the Grenadines',
        'url': 'saint-vincent-and-the-grenadines'
    },

    'WS': {
        'count': 10,
        'label': 'Samoa',
        'url': 'samoa'
    },

    'SM': {
        'count': 7,
        'label': 'San Marino',
        'url': 'san-marino'
    },

    'ST': {
        'count': 6,
        'label': 'Sao Tome and Principe',
        'url': 'sao-tome-and-principe'
    },

    'SA': {
        'count': 209,
        'label': 'Saudi Arabia',
        'url': 'saudi-arabia'
    },

    'SN': {
        'count': 161,
        'label': 'Senegal',
        'url': 'senegal'
    },

    'RS': {
        'count': 906,
        'label': 'Serbia',
        'url': 'serbia'
    },

    'CS': {
        'count': 23,
        'label': 'Serbia and Montenegro',
        'url': 'serbia-and-montenegro'
    },

    'SC': {
        'count': 6,
        'label': 'Seychelles',
        'url': 'seychelles'
    },

    'SL': {
        'count': 11,
        'label': 'Sierra Leone',
        'url': 'sierra-leone'
    },

    'SG': {
        'count': 830,
        'label': 'Singapore',
        'url': 'singapore'
    },

    'SK': {
        'count': 554,
        'label': 'Slovakia',
        'url': 'slovakia'
    },

    'SI': {
        'count': 640,
        'label': 'Slovenia',
        'url': 'slovenia'
    },

    'SB': {
        'count': 12,
        'label': 'Solomon Islands',
        'url': 'solomon-islands'
    },

    'SO': {
        'count': 19,
        'label': 'Somalia',
        'url': 'somalia'
    },

    'ZA': {
        'count': 1204,
        'label': 'South Africa',
        'url': 'south-africa'
    },

    'GS': {
        'count': 1,
        'label': 'South Georgia and the South Sandwich Islands',
        'url': 'south-georgia-and-the-south-sandwich-islands'
    },

    'KR': {
        'count': 7219,
        'label': 'South Korea',
        'url': 'south-korea'
    },

    'SS': {
        'count': 12,
        'label': 'South Sudan',
        'url': 'south-sudan'
    },

    'ES': {
        'count': 11789,
        'label': 'Spain',
        'url': 'spain'
    },

    'LK': {
        'count': 202,
        'label': 'Sri Lanka',
        'url': 'sri-lanka'
    },

    'PS': {
        'count': 372,
        'label': 'State of Palestine',
        'url': 'state-of-palestine'
    },

    'SD': {
        'count': 57,
        'label': 'Sudan',
        'url': 'sudan'
    },

    'SR': {
        'count': 16,
        'label': 'Suriname',
        'url': 'suriname'
    },

    'SJ': {
        'count': 5,
        'label': 'Svalbard and Jan Mayen',
        'url': 'svalbard-and-jan-mayen'
    },

    'SZ': {
        'count': 11,
        'label': 'Swaziland',
        'url': 'swaziland'
    },

    'SE': {
        'count': 6516,
        'label': 'Sweden',
        'url': 'sweden'
    },

    'CH': {
        'count': 3340,
        'label': 'Switzerland',
        'url': 'switzerland'
    },

    'SY': {
        'count': 175,
        'label': 'Syrian Arab Republic',
        'url': 'syrian-arab-republic'
    },

    'TW': {
        'count': 2743,
        'label': 'Taiwan',
        'url': 'taiwan'
    },

    'TJ': {
        'count': 26,
        'label': 'Tajikistan',
        'url': 'tajikistan'
    },

    'TH': {
        'count': 1960,
        'label': 'Thailand',
        'url': 'thailand'
    },

    'TL': {
        'count': 11,
        'label': 'Timor-Leste',
        'url': 'timor-leste'
    },

    'TG': {
        'count': 19,
        'label': 'Togo',
        'url': 'togo'
    },

    'TK': {
        'count': 3,
        'label': 'Tokelau',
        'url': 'tokelau'
    },

    'TO': {
        'count': 9,
        'label': 'Tonga',
        'url': 'tonga'
    },

    'TT': {
        'count': 63,
        'label': 'Trinidad and Tobago',
        'url': 'trinidad-and-tobago'
    },

    'TN': {
        'count': 257,
        'label': 'Tunisia',
        'url': 'tunisia'
    },

    'TR': {
        'count': 3322,
        'label': 'Turkey',
        'url': 'turkey'
    },

    'TM': {
        'count': 20,
        'label': 'Turkmenistan',
        'url': 'turkmenistan'
    },

    'TC': {
        'count': 6,
        'label': 'Turks and Caicos Islands',
        'url': 'turks-and-caicos-islands'
    },

    'TV': {
        'count': 5,
        'label': 'Tuvalu',
        'url': 'tuvalu'
    },

    'UG': {
        'count': 80,
        'label': 'Uganda',
        'url': 'uganda'
    },

    'GB': {
        'count': 29648,
        'label': 'UK',
        'url': 'uk'
    },

    'UA': {
        'count': 1557,
        'label': 'Ukraine',
        'url': 'ukraine'
    },

    'AE': {
        'count': 259,
        'label': 'United Arab Emirates',
        'url': 'united-arab-emirates'
    },

    'TZ': {
        'count': 60,
        'label': 'United Republic of Tanzania',
        'url': 'united-republic-of-tanzania'
    },

    'UM': {
        'count': 2,
        'label': 'United States Minor Outlying Islands',
        'url': 'united-states-minor-outlying-islands'
    },

    'UY': {
        'count': 582,
        'label': 'Uruguay',
        'url': 'uruguay'
    },

    'US': {
        'count': 117145,
        'label': 'USA',
        'url': 'usa'
    },

    'SU': {
        'count': 7166,
        'label': 'USSR',
        'url': 'ussr'
    },

    'VI': {
        'count': 9,
        'label': 'US Virgin Islands',
        'url': 'us-virgin-islands'
    },

    'UZ': {
        'count': 76,
        'label': 'Uzbekistan',
        'url': 'uzbekistan'
    },

    'VU': {
        'count': 15,
        'label': 'Vanuatu',
        'url': 'vanuatu'
    },

    'VN': {
        'count': 470,
        'label': 'Vietnam',
        'url': 'vietnam'
    },

    'WF': {
        'count': 1,
        'label': 'Wallis and Futuna',
        'url': 'wallis-and-futuna'
    },

    'EH': {
        'count': 8,
        'label': 'Western Sahara',
        'url': 'western-sahara'
    },

    'YE': {
        'count': 23,
        'label': 'Yemen',
        'url': 'yemen'
    },

    'YU': {
        'count': 1959,
        'label': 'Yugoslavia',
        'url': 'yugoslavia'
    },

    'ZM': {
        'count': 26,
        'label': 'Zambia',
        'url': 'zambia'
    },

    'ZW': {
        'count': 57,
        'label': 'Zimbabwe',
        'url': 'zimbabwe'
    },

    'BL': {
        'count': 0,
        'label': 'Saint Barthélemy',
        'url': 'saint-barthelemy'
    },

    'BQ': {
        'count': 0,
        'label': 'Bonaire, Sint Eustatius and Saba',
        'url': 'bonaire-sint-eustatius-and-saba'
    },

    'CW': {
        'count': 0,
        'label': 'Curaçao',
        'url': 'curacao'
    },

    'GG': {
        'count': 0,
        'label': 'Guernsey',
        'url': 'guernsey'
    },

    'AX': {
        'count': 0,
        'label': 'Åland Islands',
        'url': 'aland-islands'
    },

    'IM': {
        'count': 0,
        'label': 'Isle of Man',
        'url': 'isle-of-man'
    },

    'JE': {
        'count': 0,
        'label': 'Jersey',
        'url': 'jersey'
    },

    'MF': {
        'count': 0,
        'label': 'Saint Martin (French part)',
        'url': 'saint-martin-french-part'
    },

    'SX': {
        'count': 0,
        'label': 'Sint Maarten (Dutch part)',
        'url': 'sint-maarten-dutch-part'
    }
}

y = []

for c in x:
    y.append({'_id': c, 'name': x[c]['label'], 'uri': x[c]['url']})

db.Countries.insert_many(y)