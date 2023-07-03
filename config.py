client_string = 'mongodb+srv://GiuDiMax:iiZBB9JYW07nqQcp@lbdcluster.bqbva.mongodb.net/Letterboxd?retryWrites=true&w=majority'

field2 = ['actors', 'crew.director', 'crew.co-director', 'crew.additional-directing', 'crew.producer',
          'crew.executive-producer', 'crew.writer', 'crew.original-writer', 'crew.casting', 'crew.editor',
          'crew.cinematography', 'crew.additional-photography', 'crew.production-design', 'crew.art-direction',
          'crew.set-decoration', 'crew.special-effects', 'crew.visual-effects', 'crew.stunts', 'crew.choreography',
          'crew.composer', 'crew.songs', 'crew.sound', 'crew.costume-design', 'crew.makeup', 'crew.hairstyling',
          'crew.studio']

field3 = ['country', 'studio', 'language', 'genres.main', 'genres.theme', 'genres.nanogenre'] #, 'genres.mini-themes']

field4 = ['country', 'year']

field5 = ['']

api_tmdb = '6fff7e293df6a808b97101a26c86a545'

listsSelection = [
    ['dave/list/official-top-250-narrative-feature-films', 'Letterboxd Top 250', 1],
    ['jake_ziegler/list/academy-award-winners-for-best-picture', 'Oscar Best Picture Winners', 2],
    ['dave/list/imdb-top-250', 'IMDb Top 250', 3],
    ['matthew/list/box-office-mojo-all-time-worldwide', 'Box Office Mojo All Time 100', 4],
    ['bfi/list/sight-and-sounds-greatest-films-of-all-time', 'Sight & Sound Top 100', 5],
    ['moseschan/list/afi-100-years-100-movies', 'AFI 100 Years 100 Movies', 6],
    ['crew/list/edgar-wrights-1000-favorite-movies', 'Edgar Wright’s 1,000 Favorites', 7],
    ['gubarenko/list/1001-movies-you-must-see-before-you-die-2021', '1,001 To See Before You Die', 8],
    ['jack/list/official-top-250-documentary-films', 'Top 250 Documentaries', 9],
    ['darrencb/list/letterboxds-top-250-horror-films', 'Top 250 Horror', 10],
    ['jack/list/women-directors-the-official-top-100-narrative', 'Top 100 Women-Directed', 11],
    ['lifeasfiction/list/letterboxd-100-animation', 'Top 100 Animation', 12]
]

# ['liveandrew/list/bfi-2012-critics-top-250-films', 'Sight & Sound Top 250', 5],

crew_html = [
    ['crew_co-director', 'co-director', 'co-director'],
    ['crew_additional-directing', 'additional-directing', 'additional-directing'],
    ['crew_producer', 'producer', 'producer'], ['crew_executive-producer', 'executive-producer', 'executive-producer'],
    ['crew_writer', 'writer', 'writer'], ['crew_original-writer', 'original-writer', 'original-writer'],
    ['crew_casting', 'casting', 'casting'], ['crew_editor', 'editor', 'editor'],
    ['crew_cinematography', 'cinematography', 'cinematography'],
    ['crew_additional-photography', 'additional-photography', 'additional-photography'],
    ['crew_production-design', 'production-design', 'production-design'],
    ['crew_art-direction', 'art-direction', 'art-direction'],
    ['crew_set-decoration', 'set-decoration', 'set-decoration'],
    ['crew_special-effects', 'special-effects', 'special-effects'],
    ['crew_visual-effects', 'visual-effects', 'visual-effects'], ['crew_stunts', 'stunts', 'stunts'],
    ['crew_choreography', 'choreography', 'choreography'], ['crew_composer', 'composer', 'composer'],
    ['crew_songs', 'songs', 'songs'], ['crew_sound', 'sound', 'sound'],
    ['crew_costume-design', 'costume-design', 'costume-design'], ['crew_makeup', 'makeup', 'makeup'],
    ['crew_hairstyling', 'hairstyling', 'hairstyling'], ['studio', 'studio', 'studio']
]

exclude_people = ['mickie-mcgowan', 'stan-lee', 'jack-angel', 'sherry-lynn', 'fred-tatasciore', 'jim-cummings',
                  'frank-welker', 'laraine-newman', 'bob-bergen', 'jess-harnell', 'jan-rabson', 'bob-peterson',
                  'fred-tatasciore', 'dee-bradley-baker', 'grey-delisle', 'tara-strong', 'scott-menville',
                  'mona-marshall', 'danny-mann', 'bill-farmer', 'terri-douglas', 'david-cowgill', 'lori-alan',
                  'debi-derryberry', 'kari-wahlgren', 'john-cygan', 'jackie-gonneau']

users_list_url = 'https://gist.githubusercontent.com/GiuDiMax/84c8ba608c932d4671d5fe83d5f5e9c4/raw/users_lbd'

"""
for f in field2:
    if "." in f:
        print("['")
        print(f.replace(".", "_"))
        print("', '")
        print(f.split(".", 1)[1])
        print("', '")
        print(f.split(".", 1)[1])
        print("'], ")
"""