import os
import sys
import json
import time
import calendar as cal
from pathlib import Path
import requests as rq
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def _page(n, page_size=100):
    q = n // page_size
    if  n % page_size != 0:
        q += 1
    return q

def _fetch_repo(params, folder):
    token = os.getenv('GITHUB_TOKEN')
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }
    while True:
        resp = rq.get('https://api.github.com/search/repositories', headers=headers, params=params)
        if resp.status_code == rq.codes.ok:
            break
        print(f'fetch error: {resp.json()["message"]}')
        time.sleep(61)
    return resp.json()['items']

def fetch_repo(query, sort_method, count, folder=Path('data')):
    pages = _page(count)
    folder.mkdir(exist_ok=True)
    futures = []
    print('start', query)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for page in range(1, pages+1):
            params = {
                'q': query,
                'sort': sort_method,
                'per_page': 100,
                'page': page
            }
            futures.append(executor.submit(_fetch_repo, params, folder))
        repos = [ i for l in concurrent.futures.as_completed(futures) for i in l.result() ]
    print('finish', query)
    filename = query.replace('/', '_')
    with open(folder / f'{filename}.json', 'w') as fp:
        json.dump(repos, fp, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) < 3:
        exit(1)
    year = int(sys.argv[1])
    month = int(sys.argv[2])

    folder = Path('data') / str(year) / f'{month:02d}'
    days = cal.monthrange(year, month)[1]
    for i in range(1, days+1):
        query = f'created:{year}-{month:02d}-{i:02d} size:>10'
        fetch_repo(query, 'updated', 1000, folder)

if __name__ == '__main__':
    main()

