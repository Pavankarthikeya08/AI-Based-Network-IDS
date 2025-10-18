#!/usr/bin/env bash
set -e
echo "This script opens dataset pages — download manually if required."
echo "CIC-IDS2017: https://www.unb.ca/cic/datasets/ids-2017.html"
echo "NSL-KDD on Kaggle: https://www.kaggle.com/datasets/hassan06/nslkdd"
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "https://www.unb.ca/cic/datasets/ids-2017.html"
  xdg-open "https://www.kaggle.com/datasets/hassan06/nslkdd"
fi
