from requests import get

class APKDownloader:
    def __init__(self, download: str, results; str):
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
        pass
        #TODO

    def googleplay_download(self, package: str):
        if not self.credentials_path:
            raise SystemExit('[-] No GooglePlay key found')
        #TODO