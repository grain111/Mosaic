import urllib.request
from tqdm import tqdm

l = []

def conv_url(url, q, p):
    url = url.replace('%%%query%%%', q)
    url = url.replace('%%%page%%%', p)
    return url


url = 'https://pixabay.com/api/?key=4683416-8754135a461a502021a00143e&q=%%%query%%%&image_type=photo&per_page=200&page=%%%page%%%'

query = ['cat', 'dog', 'mouse', 'horse', 'panda', 'duckling', 'hedghog', 'kitten', 'lamb', 'owl', 'bunny', 'piglet', 'penguins', 'baby+hipo', 'fox', 'rainbow', 'seal', 'dolphin', 'deer', 'crocodile', 'pet', 'chick', 'bird', 'rat', 'puppy', 'retriever', 'buldog']
query2 = []
page = ['1', '2']
for q in query:
    print('Fetching {}'.format(q))
    for p in page:
        d = eval(urllib.request.urlopen(conv_url(url, q, p)).read().decode('utf-8'))
        for photo in d['hits']:
            l.append(photo['webformatURL'])

print('Download started')
num = 0
for i in tqdm(range(len(l))):
    num += 1
    f = open('{}.jpg'.format(num),'wb')
    f.write(urllib.request.urlopen(l[i]).read())
    f.close()
