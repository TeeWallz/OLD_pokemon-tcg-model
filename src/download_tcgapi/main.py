from src.download_tcgapi import extraction_tools

# sets = extraction_tools.read_sets()
extraction_tools.clear_database()
extraction_tools.readDataIntoSql()
