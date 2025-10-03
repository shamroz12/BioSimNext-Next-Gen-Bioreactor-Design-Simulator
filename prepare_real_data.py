
# Headless script to fetch and preprocess real datasets.
import argparse
from pathlib import Path
from biosimnext.data import RealDataLoader

parser = argparse.ArgumentParser()
parser.add_argument('--data-dir', default='examples/sample_data/real', help='output data directory')
parser.add_argument('--datasets', nargs='+', default=['dryad_microalgae','abpdu_fcic_drive'])
args = parser.parse_args()

loader = RealDataLoader(Path(args.data_dir))
for k in args.datasets:
    print('Fetching', k)
    try:
        df = loader.fetch_and_preprocess(k)
        out = Path(args.data_dir) / f"{k}.csv"
        # If df is a pandas DataFrame, save; else skip
        try:
            df.to_csv(out, index=False)
            print('Wrote', out)
        except Exception as e:
            print('Downloaded data for', k, 'but failed to save as CSV:', e)
    except Exception as e:
        print('Failed to fetch', k, 'error:', e)
print('Done.')
