import requests
import pprint
from collections import Counter
from datetime import datetime, timedelta
import csv

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlM"
                     "TNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfc"
                     "mVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
}


class Film:

    def __init__(self, numb):
        self.lst = []
        self.get_fetch_data(numb)
        self.collection = []

    # 1
    def get_fetch_data(self, numb):
        for i in range(1, numb + 1):
            url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by' \
                  f'=popularity.desc&page={i}'
            getter = requests.get(url=url, headers=headers)
            self.lst.extend(getter.json()['results'])

    # 2
    def get_lst(self):
        return self.lst

    # 3
    def get_index_3_to_19(self):
        return self.lst[3:19:4]

    # 4
    def get_popularity(self):
        return max(self.lst, key=lambda h: h['popularity'])['title']

    # 5
    def get_names_titles_keywords(self, keywords):
        return [movie['title'] for movie in self.lst if any(keyword in movie['overview'] for keyword in keywords)]

    # 6
    def get_unique_collection(self):
        return set(genre for movie in self.lst for genre in (movie.get('genre_ids', [])))

    # 8
    def get_most_popular_genres(self, num_genres):
        return dict(Counter(genre for movie in self.lst for genre in movie['genre_ids']).most_common(num_genres))

    # 10
    def get_data_and_change_copy(self):
        return self.lst, list(map(self.back_film, self.lst))

    @staticmethod
    def back_film(film):
        film['genre_ids'][0] = 22
        return film

    # 7
    def delete_all_movies(self, num_of_delete):
        return list(filter(lambda movie: num_of_delete not in movie['genre_ids'], self.lst))

    # 11
    def get_collection_of_structures(self):
        for movie in self.lst:
            mark = {
                'Title': movie['title'],
                'Popularity': round(movie['popularity'], 1),
                'Score': int(movie['vote_average']),
                'Last day in cinema': (
                            datetime.strptime(movie['release_date'], '%Y-%m-%d') + timedelta(weeks=8, days=4)).strftime(
                    '%Y-%m-%d')
            }
            self.collection.append(mark)
        self.collection.sort(key=lambda film: (film['Score'], film['Popularity']))
        return self.collection

    # 12
    def write_csv_file(self):

        fields = ['Title', 'Popularity', 'Score', 'Last day in cinema']

        with open('D:/file.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fields)
            writer.writeheader()
            for film in self.collection:
                writer.writerow(film)

    # 9
    def get_titles_grouped(self):
        movie = []
        for i, film in enumerate(self.lst):
            for film_1 in self.lst[i:]:
                if set(film['genre_ids']).intersection(film_1['genre_ids']):
                    movie.append((film['title'], film_1['title']))
        return movie


test = Film(3)
user_keywords = ['action']
# 1
pprint.pprint(test.get_lst())
# 3
pprint.pprint(test.get_index_3_to_19())
# 4
pprint.pprint(test.get_popularity())
# 5
pprint.pprint(test.get_names_titles_keywords(user_keywords))
# 6
pprint.pprint(test.get_unique_collection())
# 7
pprint.pprint(test.delete_all_movies(35))
# 8
pprint.pprint(test.get_most_popular_genres(4))
# 9
pprint.pprint(test.get_titles_grouped())
# 10
pprint.pprint(test.get_data_and_change_copy())
# 11
pprint.pprint(test.get_collection_of_structures())
# 12
test.write_csv_file()
