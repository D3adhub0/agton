set -euo pipefail
projects=(ton jetton wallet dedust)
for p in "${projects[@]}"; do
  rm -rf "$p/dist" 
  rm -rf "$p/build"
  rm -rf $p/*.egg-info
  find . -type d -name "__pycache__" -exec rm -rf {} +
done
