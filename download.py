import sys, argparse, requests, json, os
from os.path import basename

def getContent (url, type):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0'}
    if type == 'json':
        return requests.get(url, headers=headers).json()
    elif type == 'raw':
        return requests.get(url, headers=headers).content
    elif type == 'zip':
        return requests.get(url, headers=headers, stream=True)

# python3 download.py -o listcategories
def listcategories ():
    url = 'https://www.hackerrank.com/rest/contests/master'
    categories = getContent(url, 'json')['model']['categories']
    [print(category['slug']) for category in categories]

# python3 download.py -o listsubcategories -c java
def listsubcategories (category):
    url = 'https://www.hackerrank.com/rest/contests/master'
    categories = getContent(url, 'json')['model']['categories']
    for c in categories:
        if c['slug'] == category:
            [print(children['slug']) for children in c['children']]
            break

# python3 download.py -o listproblems -c algorithms -s implementation
def listproblems (categoryname, subcategoryname):
    url = 'https://www.hackerrank.com/rest/contests/master/tracks/' + categoryname + '/challenges?offset=0&limit=1000&filters[subdomains][]=' + subcategoryname + '&track_login=true'
    response = getContent(url, 'json')
    [print(elem['slug']) for elem in response['models']]

def getProblemDetails (problemname):
    problemurl = 'https://www.hackerrank.com/rest/contests/master/challenges/' + problemname + '/'
    problemdetails = getContent(problemurl, 'json')
    return problemdetails

# python3 download.py -o downloadproblem -p angry-professor
def downloadproblem (problemname):
    # problem details (like, domain and sub-domain name of the problem)
    problemdetails = getProblemDetails(problemname)
    dir = problemdetails['model']['track']['track_name'] + '/' + problemdetails['model']['track']['name']
    if not os.path.exists(dir):
        os.makedirs(dir)

    # problem statement pdf
    problemstatementurl = 'https://www.hackerrank.com/rest/contests/master/challenges/' + problemname + '/download_pdf?language=English'
    pdfcontent = getContent(problemstatementurl, 'raw')
    with open('/Users/sbaranidharan/Documents/hackerrank/' + dir + '/' + problemname + '.pdf', 'wb') as f:
        f.write(pdfcontent)
    print(problemname + '.pdf is saved under /Users/sbaranidharan/Documents/hackerrank/' + dir)

    # test cases zip
    testcasesurl = 'https://www.hackerrank.com/rest/contests/master/challenges/' + problemname + '/download_testcases'
    zipcontent = getContent(testcasesurl, 'zip')
    with open('/Users/sbaranidharan/Documents/hackerrank/' + dir + '/' + problemname + '-testcases.zip', 'wb') as f:
        for chunk in zipcontent.iter_content(chunk_size=128):
            f.write(chunk)
    print(problemname + '-testcases.zip is saved under /Users/sbaranidharan/Documents/hackerrank/' + dir)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--category',       '-c', help='Categories slug name like algorithms, data-structures, mathematics etc.,')
    parser.add_argument('--subcategory',    '-s', help='Sub-Categories slug name like warmup, implementation etc.,')
    parser.add_argument('--problem',        '-p', help='Problem slug name like solve-me-first, a-very-big-sum etc.,')
    parser.add_argument('--operation',      '-o', help='List of operations like listcategories, listsubcategories, listproblems and downloadproblem')

    args=parser.parse_args()
    #url = 'https://www.hackerrank.com/rest/contests/master'
    #print (getContent(url)['model']['categories'][1]['children'][0]['name'])
    if args.operation.lower()    == 'listcategories':
        listcategories()
    elif args.operation.lower()  == 'listsubcategories':
        listsubcategories(args.category)
    elif args.operation.lower()  == 'listproblems':
        listproblems(args.category, args.subcategory)
    elif args.operation.lower()  == 'downloadproblem':
        downloadproblem(args.problem)
