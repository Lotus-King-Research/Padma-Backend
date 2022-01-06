# Environment

The below is recommended for development:

```
# get the package
gh repo clone Lotus-King-Research/Padma-Backend

# install the package (being in the root of the package)
pip install .

# run (for development)
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
