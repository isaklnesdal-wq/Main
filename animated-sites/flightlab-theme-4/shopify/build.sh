#!/bin/sh
# Bygger templates/index.liquid av den frittstående index.html.
#
#   index.html   hele forsiden, uendret, pakket i {% raw %} så Shopify ikke
#                prøver å tolke JS-en som Liquid
#   head.liquid  Liquid som leser temainnstillingene og setter window.FL_IMG.
#                Settes inn rett før </head> — altså INNE i dokumentet, slik
#                at <!DOCTYPE> fortsatt står først (ellers havner siden i
#                quirks mode og layouten ryker).
#
# Kjør fra denne mappen:  sh build.sh
set -e
cd "$(dirname "$0")"

SRC=../index.html
test "$(grep -c '</head>' "$SRC")" -eq 1 || { echo "FEIL: forventet nøyaktig én </head> i $SRC"; exit 1; }

SPLIT=$(grep -n '</head>' "$SRC" | cut -d: -f1)

{
  printf '{%% layout none %%}{%% raw %%}\n'
  head -n "$((SPLIT - 1))" "$SRC"
  printf '{%% endraw %%}\n'
  cat head.liquid
  printf '{%% raw %%}\n'
  tail -n "+$SPLIT" "$SRC"
  printf '\n{%% endraw %%}'
} > index.liquid

echo "index.liquid bygget ($(wc -c < index.liquid) bytes, </head> på linje $SPLIT)"
