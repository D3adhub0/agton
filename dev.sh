# fresh venv
python3 -m venv .venv && source .venv/bin/activate

# editable installs of all dists for dev:
pip install -e ./ton -e ./jetton -e ./wallet -e ./dedust