# BioSimNext—Next-Gen Bioreactor Design Simulator (Full Expanded Repo)

BioSimNext is a modern, interactive bioreactor simulator combining mechanistic modeling,
AI-based optimization, and real-time sensor data visualization. This archive contains a full
expanded scaffold with real-data integration hooks (scripts to fetch public datasets),
backend FastAPI service, frontend React + Tailwind skeleton, examples, notebooks, Docker
configs, and CI workflow templates.

NOTE: Due to licensing and size, raw external datasets are NOT included. Use
`examples/scripts/prepare_real_data.py` to download and preprocess public datasets.


## Real datasets integrated

- Dryad microalgae photobioreactor dataset (public): DOI 10.5061/dryad.p9m57n7. The loader downloads multiple CSV runs directly from Dryad.
- ABPDU FCIC archive: linked from ABPDU resources (Google Drive). The loader attempts to download via gdown using the public file id.
- Mendeley Verrucodesmus dataset: currently under embargo; the loader will not auto-download it. If you have access, download manually and place files into `examples/sample_data/real/mendeley/`.
