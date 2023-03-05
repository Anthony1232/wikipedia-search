import requests
from bs4 import BeautifulSoup as bs
import os

# to run, requires:
# python3
# command prompt: pip install BeautifulSoup
# command prompt: pip install requests

everything = '-a'
exitstate = '-e'
savefile = '-s'

print(f'this program will search through wiki given any keyword and return the most relevant website. Type any word and it will search automatically.\nOnce a website has been found the following can be done:\ntype -a to display content of site\ntype any words to search for keywords within site\ntype -s to save site to a text file at {os.getcwd()}\ntype -e to exit site and search for another one\n')


def findlink(urll):
     url = urll
     site = requests.get(url)
     soup = bs(site.text, 'html.parser')
     paragraphs = soup.find_all('p')
     return soup, paragraphs


def searchsite(soup, search, paragraphs):
     while True:
    
          search2 = input('website command:\n').lower()

          if search2 == exitstate:
               return

          elif search2 == savefile:
               saveas = input('\nsave as:\n') + '.txt'
               with open(saveas, 'w') as file:
                    for par in paragraphs:
                         counter = 1
                         for char in par.text:
                              counter += 1
                              if counter % 180 == 0:
                                   file.write('\n')
                              try:
                                   file.write(char)
                              except:
                                   file.write('--unk_char--')
                                   counter += len('--unk_char--')
                         file.write('\n')
                    file.write('\n\n\nLinks:\n\n')

                    links = []
                    for link in soup.find_all('a'):
                         links.append(link.text + ':   ' + str(link.get('href')) + '\n')
                    links.sort()
                    for i in links:
                         try:
                              file.write(i)
                         except:
                              pass
                         

          elif search2 == everything:
               correct = [i.text  for i in paragraphs]
               for i in correct:
                    print(i, '\n\n')

                    
          else:
               correct = [i.text for i in paragraphs if search2 in i.text.lower()]


               for i in correct:
                    i = i.replace(search2, f'--{search2.upper()}--')
                    print(i)
                    print('\n-----------------              ------------------\n\n')

               

def search():
          search = input('search for a website:\n')
          
          url = 'https://en.wikipedia.org/wiki/' + search
          site = requests.get(url)
          soup = bs(site.text, 'html.parser')
          paragraphs = soup.find_all('p')

          try:
               if 'Other reasons this message may be displayed:' in paragraphs[1].text:
                    wrong = True
               else:
                    wrong = False
          except:
               if 'Other reasons this message may be displayed:' in paragraphs[0].text:
                    wrong = True
               else:
                    wrong = False
          if wrong:
               print('\nno website with this name. searching for similar websites...\n')
               out = soup.find_all('a')
               working = False
               for i in out:
                    if 'search for ' in i.text and ' in Wikipedia' in i.text:
                         actual = i.get('href')
                         working = True
               if not working:
                    print('unable to find site, please try again')
                    return
                         
               soup, paragraphs = findlink(actual)

               lists = soup.find('ul', class_='mw-search-results')
               try:
                    link = lists.find('a').get('href')
               except:
                    print('no website found..')
                    return
               
               soup, paragraphs = findlink('https://en.wikipedia.org' + link)

          reference = soup.find('div', id='mw-content-text')
          try:
               if 'most commonly refers to:' in reference.find('p', class_ = '').text:
                    link = reference.find('ul').find('a').get('href')
                    print(f'{search} most commonly refers to:\n')
                    print(reference.find('ul').text + '\n\n')
                    print(f'{search} may also refer to:\n')
                    print(reference.find_all('ul')[1].text + '\n\n\n')
                    print('entering top reference..')
                    soup, paragraphs = findlink('https://en.wikipedia.org' + link)
          except:
               pass
          
          try:
               if 'may refer to:' in reference.find('p', class_='').text:
                    link = reference.find('ul').find('a').get('href')
                    print(reference.find('p').text)
                    print(reference.find('ul').text + '\n\n')
                    print('entering top reference..')
                    soup, paragraphs = findlink('https://en.wikipedia.org' + link)
          except:
               pass
                    
          if 'User talk:' in soup.title.text:
               print(soup.title.text)
               print('error, page not found')
               return
               
          
          if '404' in soup.text[0:100] and 'error' in soup.text[0:100] and 'not found' in soup.text[0:100]:
               print('error 404')
               return


          print('\ngot website:  ' + soup.title.text + '\n')


          searchsite(soup, search, paragraphs)
     

while True:
     search()
