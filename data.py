
import requests
import pandas as pd
from pathlib import Path
import io, time, subprocess, sys

class RealDataLoader:
    """RealDataLoader with working integrations for public datasets:
    - dryad_microalgae (public Dryad dataset DOI:10.5061/dryad.p9m57n7)
    - abpdu_fcic_drive (Google Drive file from ABPDU page; uses gdown)
    - mendeley_verrucodesmus (EMBARGOED: will raise and instruct user)
    """
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_and_preprocess(self, key: str):
        if key == 'dryad_microalgae':
            return self._fetch_dryad_microalgae()
        if key == 'abpdu_fcic_drive':
            return self._fetch_abpdu_drive()
        if key == 'mendeley_verrucodesmus':
            raise RuntimeError('Mendeley dataset is under embargo until its public release date. Please download manually if you have access.')
        raise ValueError(f'Unknown dataset key: {key}')

    def _download_url(self, url, max_retries=3, timeout=30):
        for attempt in range(max_retries):
            try:
                r = requests.get(url, timeout=timeout)
                r.raise_for_status()
                return r.content
            except Exception as e:
                print(f"download attempt {attempt+1} failed: {e}")
                time.sleep(2)
        raise RuntimeError(f"Failed to download {url}")

    def _fetch_dryad_microalgae(self):
        # Dryad dataset DOI:10.5061/dryad.p9m57n7
        # Files listed on Dryad; we download a few representative CSV runs.
        base_files = [
            ('Run140514.csv','https://datadryad.org/stash/downloads/file_stream/159577?file=Run140514.csv'),
            ('Run140619.csv','https://datadryad.org/stash/downloads/file_stream/159578?file=Run140619.csv'),
            ('Run140708.csv','https://datadryad.org/stash/downloads/file_stream/159579?file=Run140708.csv'),
            ('Run140722.csv','https://datadryad.org/stash/downloads/file_stream/159580?file=Run140722.csv'),
            ('Run140814.csv','https://datadryad.org/stash/downloads/file_stream/159581?file=Run140814.csv'),
            ('Run140902.csv','https://datadryad.org/stash/downloads/file_stream/159582?file=Run140902.csv'),
            ('Run150624.csv','https://datadryad.org/stash/downloads/file_stream/159583?file=Run150624.csv'),
            ('Run150817.csv','https://datadryad.org/stash/downloads/file_stream/159584?file=Run150817.csv'),
            ('Run150909.csv','https://datadryad.org/stash/downloads/file_stream/159585?file=Run150909.csv'),
            ('sunrise2014.csv','https://datadryad.org/stash/downloads/file_stream/159586?file=sunrise2014.csv'),
        ]

        dfs = []
        for name, url in base_files:
            try:
                content = self._download_url(url)
                df = pd.read_csv(io.BytesIO(content))
                # add source column, basic timestamp handling if present
                if 'time' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['time'], errors='coerce')
                # Many Dryad files use their own column names — keep them and store under a subdir
                out = self.data_dir / 'dryad' / name
                out.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(out, index=False)
                dfs.append(df)
            except Exception as e:
                print('Failed to download', name, e)
        # For convenience, return the first dataframe parsed (caller can inspect files)
        if dfs:
            return dfs[0]
        raise RuntimeError('Failed to fetch any Dryad files.')

    def _fetch_abpdu_drive(self):
        # ABPDU page links to a Google Drive file (public view). We attempt to download via gdown if available.
        # File id (from ABPDU page): 1RIcJgbCbgpI_l3BLhA0vihqQze97N32S
        file_id = '1RIcJgbCbgpI_l3BLhA0vihqQze97N32S'
        out_path = self.data_dir / 'abpdu_fcic_drive.zip'
        # Use gdown if installed, else instruct user how to install it
        try:
            import gdown
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, str(out_path), quiet=False)
        except Exception as e:
            # try calling gdown via subprocess
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gdown'])
                import gdown
                url = f'https://drive.google.com/uc?id={file_id}'
                gdown.download(url, str(out_path), quiet=False)
            except Exception as e2:
                raise RuntimeError('gdown is required to fetch the ABPDU Google Drive dataset. Please install gdown (`pip install gdown`) and re-run. Original error: ' + str(e2))

        # If downloaded, attempt to extract and read first CSV
        try:
            import zipfile
            with zipfile.ZipFile(out_path, 'r') as z:
                z.extractall(self.data_dir / 'abpdu')
            # find first csv in extracted folder
            extracted = list((self.data_dir / 'abpdu').rglob('*.csv'))
            if not extracted:
                raise RuntimeError('No CSVs found in extracted ABPDU archive.')
            df = pd.read_csv(extracted[0], parse_dates=True, infer_datetime_format=True)
            return df
        except Exception as e:
            raise RuntimeError('Failed to extract or parse ABPDU archive: ' + str(e))

