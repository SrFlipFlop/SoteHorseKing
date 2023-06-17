from utils.common.ssh import SecureShell

from json import load
from requests import get
from hashlib import sha256
from requests.utils import default_headers

class APKDownloader:
    def __init__(self, download: str, results: str, credentials=None):
        self.credentials_path = credentials
        self.download_path = download
        self.results_path = results
        self.apk_content_type = ['vnd.android.package-archive', 'java-archive', 'apk', 'zip']

    def regular_download(self, url: str) -> str:
        if not url.endswith('.apk'):
            raise SystemExit(f'[!] Error downloading APK ({url}) - Not ends with apk extension')

        res = get(url, verify=False, stream=True)
        if res.status_code != 200:
            raise SystemExit(f'[!] Error downloading APK ({url}) - Status code {res.status_code}')

        if not self._check_apk(res.headers['Content-Type']):
            raise SystemExit(f'[!] Error downloading APK ({url}) - Download does not have the correct Content-Type')

        self._store_apk(res)
        return self.download_path
        
    def apkpure_download(self, package: str) -> str:
        headers = default_headers()
        headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',})
        res = get(f'https://d.apkpure.com/b/APK/{package}?version=latest', headers=headers, stream=True)
        
        if not self._check_apk(res.headers['Content-Type']):
            raise SystemExit(f'[!] Error downloading APK ({package}) - Download does not have the correct Content-Type')

        self._store_apk(res)
        return self.download_path

    def googleplay_download(self, package: str):
        if not self.credentials_path:
            raise SystemExit('[-] No GooglePlay credentials')

        with open(self.credentials_path, 'r') as f:
            credentials = load(f)
            raw = f.read()

        valid = False
        for creds in credentials:
            user = creds.get('USERNAME')
            passwd = creds.get('PASSWORD')
            android = creds.get('ANDROID_ID')
            valid = (not user or not passwd or not android)

        if not valid:    
            raise SystemExit(f'[-] No GooglePlay valid credentials {credentials}')

        hash = sha256(raw.encode('utf-8')).hexdigest()
        self.ssh = SecureShell('android-tools', 'root', '/opt/airflow/config/id_rsa')
        self.ssh.execute_wait_commands([
            f'echo \'{raw}\' > /tmp/{hash}.json',
            f'cd /opt/PlaystoreDownloader && pipenv run python3 -m playstoredownloader.cli -c /tmp/{hash}.json -o {self.download_path} "{package}"',
            f'rm /tmp/{hash}.json'
        ])
        return self.download_path

    def _check_apk(self, content_type: str) -> bool:
        correct = False
        for header in self.apk_content_type:
            if header in content_type:
                correct = True
                break
        return correct
    
    def _store_apk(self, response: object):
        with open(self.download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()