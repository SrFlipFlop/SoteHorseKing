from requests import get
from requests.utils import default_headers

class APKDownloader:
    def __init__(self, download: str, results: str):
        self.credentials_path = None
        self.download_path = download
        self.results_path = results

    def regular_download(self, url: str):
        if not url.endswith('.apk'):
            raise SystemExit(f'[!] Error downloading APK ({url}) - Not ends with apk extension')

        res = get(url, verify=False, stream=True)
        if res.status_code != 200:
            raise SystemExit(f'[!] Error downloading APK ({url}) - Status code {res.status_code}')

        correct = False
        for header in ['vnd.android.package-archive', 'java-archive', 'apk', 'zip']:
            if header in res.headers['Content-Type']:
                correct = True
                break
        if not correct:
            raise SystemExit(f'[!] Error downloading APK ({url}) - Download does not have the correct Content-Type')

        with open(self.download_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        return self.download_path
        
    def apkpure_download(self, package: str):
        headers = default_headers()
        headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',})
        res = get(f'https://d.apkpure.com/b/APK/{package}?version=latest', headers=headers, stream=True)
        
        correct = False
        for header in ['vnd.android.package-archive', 'java-archive', 'apk', 'zip']:
            if header in res.headers['Content-Type']:
                correct = True
                break
        if not correct:
            raise SystemExit(f'[!] Error downloading APK ({package}) - Download does not have the correct Content-Type')

        with open(self.download_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        return self.download_path

    def googleplay_download(self, package: str):
        if not self.credentials_path:
            raise SystemExit('[-] No GooglePlay key found')
        #TODO: https://github.com/ClaudiuGeorgiu/PlaystoreDownloader