import os
from tcg_api import load_from_api

#
# import download_tcgapi.extraction_tools as extraction_tools
# import tcg_data_enrichment.generate_card_variations as enrichment_variations
#
# conn_string = 'sqlite:////home/tom/pokemon.db'
#

pg_user = os.environ.get('pg_user')
pg_password = os.environ.get('pg_password')
conn_string = f'postgresql://{pg_user}:{pg_password}@docker.tomekwaller.com:5432/pokemon'
#
# extraction_tools.drop_all_and_extract(conn_string, "/tmp/pokemon_staging/")
# enrichment_variations.load_card_variations(conn_string)

load_from_api.load(conn_string)