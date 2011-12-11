#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: From command line :
./allocine.py las vegas
[**** ] Las Vegas parano (Fear and Loathing in Las Vegas) 1998
[**   ] Lune de miel à Las Vegas (Honeymoon in Vegas) 1992
[  ?  ] The Virgin of Las Vegas 2009
...
./allocine.py las vegas parano
[**** ] Las Vegas parano (Fear and Loathing in Las Vegas) 1998
Genre: Comédie dramatique, Aventure
Synopsis: A travers l'épopée à la fois comique et horrible vers Las Vegas du journaliste Raoul Duke et de son énorme avocat, le Dr. Gonzo, évocation caustique et brillante de l'année 1971 aux Etats-Unis, pendant laquelle les espoirs des années soixante et le fameux rêve américain furent balayés pour laisser la place à un cynisme plus politiquement correct.

Or you can 'import allocine' and use the class Allocine :
>>> import allocine
>>> a = allocine.Allocine()
>>> vegas = a.search_movie('las vegas')
>>> len(vegas)
10
>>> a.pretty_print_movie(vegas[0])
[**** ] Las Vegas parano (Fear and Loathing in Las Vegas) 1998
>>> vegas
[
    {u'code': 18457,
     u'castMember': [{u'person': u'Terry Gilliam', u'activity': {u'code': 8002}}, ...],
     u'title': u'Las Vegas parano',
     u'poster': {u'href': u'http://images.allocine.fr/medias/04/21/07/042107_af.jpg'},
     u'originalTitle': u'Fear and Loathing in Las Vegas',
     u'statistics': {u'userRating': 4},
     u'productionYear': 1998,
     u'release': {u'releaseDate': u'1998-08-19'},
     u'link': [{u'href': u'http://www.allocine.fr/film/fichefilm_gen_cfilm=18457.html', u'rel': u'aco:more'}]
    },
...
]
"""

import urllib
import sys
import json


class Allocine:
    movie_search_url = 'http://api.allocine.fr/xml/search?'
    movie_detail_url = 'http://api.allocine.fr/xml/movie?'

    def pretty_print_movie(self, film):
        """
        Return a pretty printed movie, like :
        [**** ] Las Vegas parano (Fear and Loathing in Las Vegas) (1998)
        Takes a movie object from movie_detail or from search_movie.
        """
        out = []
        if 'statistics' in film:
            rating = int(film['statistics']['userRating'])
            out.append('[%s]' % (rating * '*' + (5 - rating) * ' '))
        else:
            out.append('[  ?  ]')
        if 'title' in film:
            out.append('%s (%s)' % (film['title'], film['originalTitle']))
        else:
            out.append(film['originalTitle'])
        out.append(str(film['productionYear']))
        if 'genre'in film:
            out.append('\nGenre: ' + ', '.join(genre['$'] for genre in film['genre']))
        if 'synopsis' in film:
            out.append("\nSynopsis: " + film['synopsis'])
        return ' '.join(out)

    def movie_detail(self, movie):
        """
        return the details of a movie from its code found from search_movie.
        """
        params = {'code': movie, 'json': 1, 'partner': 3}
        result_json = urllib.urlopen(self.movie_detail_url
                                     + urllib.urlencode(params)).read()
        return json.loads(result_json)['movie']

    def search_movie(self, search):
        """
        Search a movie, returns an array of movies.
        """
        params = {'q': search, 'json': 1, 'partner': 3}
        result_json = urllib.urlopen(self.movie_search_url
                                     + urllib.urlencode(params)).read()
        results = json.loads(result_json)['feed']
        return results['movie'] if 'movie' in results else []

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print sys.modules[__name__].__doc__
        sys.exit(1)
    search = ' '.join(sys.argv[1:])
    allocine = Allocine()
    results = allocine.search_movie(search)
    for result in results:
        if result['originalTitle'].lower() == search.lower() \
                or ('title' in result
                    and result['title'].lower() == search.lower()):
            print allocine.pretty_print_movie(allocine.movie_detail(result['code']))
            sys.exit(0)
    for film in results:
        print allocine.pretty_print_movie(film)
