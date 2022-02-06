import download_tcgapi.extraction_tools as extraction_tools
import tcg_data_enrichment.generate_card_variations as enrichment_variations

conn_string = 'sqlite:////tmp/pokemon.db'

# extraction_tools.drop_all_and_extract(conn_string, "/tmp/pokemon_staging/")
enrichment_variations.load_card_variations(conn_string)
