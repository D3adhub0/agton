set -euo pipefail
projects=(ton jetton wallet dedust)
for p in "${projects[@]}"; do
  rm -rf "$p/dist" 
  rm -rf "$p/build"
  rm -rf $p/*.egg-info
done
