
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from biosimnext.data import RealDataLoader
from pathlib import Path

app = FastAPI(title='BioSimNext API')

DATA_DIR = Path('examples/sample_data/real')

@app.get('/datasets')
def list_datasets():
    loader = RealDataLoader(DATA_DIR)
    keys = ['abpdu_rhodo','geo_gse71562','mendeley_photobioreactor']
    return JSONResponse({'available': keys})

@app.post('/datasets/fetch/{key}')
def fetch_dataset(key: str):
    loader = RealDataLoader(DATA_DIR)
    try:
        df = loader.fetch_and_preprocess(key)
        out = DATA_DIR / f"{key}.csv"
        df.to_csv(out, index=False)
        return {'status':'ok','written': str(out)}
    except Exception as e:
        return {'status':'error','error': str(e)}
