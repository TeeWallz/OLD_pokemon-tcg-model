import os

version = "old_website"

# pg_user = os.environ.get('pg_user')
# pg_password = os.environ.get('pg_password')
pg_user = 'postgres'
pg_password = 'EurGSFYsmNQFW6x4s3S4uFmR8Nr9QZbQ'
conn_string = f'postgresql://{pg_user}:{pg_password}@docker.tomekwaller.com:5432/pokemon-site-dev'

if version == 'new':
    from tcg_api import load_from_api

    # load_from_api.load(conn_string)
elif version == 'medium':
    import download_tcgapi.extraction_tools as extraction_tools
    import tcg_data_enrichment.generate_card_variations as enrichment_variations
    extraction_tools.drop_all_and_extract(conn_string, "/tmp/pokemon_staging/")
#     enrichment_variations.load_card_variations(conn_string)
    extraction_tools.readDataIntoSql()

