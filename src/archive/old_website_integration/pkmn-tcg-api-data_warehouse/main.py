from data_sources.PokemonTcgApi import PokemonTcgApi
from models.ModelSchema import TcgData
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
     level=logging.INFO,
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d}\t%(levelname)s - \t%(message)s',
     datefmt='%H:%M:%S'
 )

pg_user = 'postgres'
pg_password = 'EurGSFYsmNQFW6x4s3S4uFmR8Nr9QZbQ'
conn_string = f'postgresql://{pg_user}:{pg_password}@docker.tomekwaller.com:5432/pokemon-site-dev'
pokemon_tcg_api = PokemonTcgApi()
tcgdata = TcgData(conn_string)
#tcgdata = TcgData('mysql://root:b0nb0n@192.168.0.91:3306/pokemon_tcg_api')
# tcgdata = TcgData('sqlite:////tmp/sqlite_database.db')


pokemon_tcg_api.replicate_data(tcgdata)
# pokemon_tcg_api.save_database_to_json(tcgdata, '/home/tom/git/home/pokemon-tcg-data-data-warehouse/src/data_sources/build')
# pokemon_tcg_api.compare_data_directories(
#     '/home/tom/git/home/pokemon-tcg-data-data-warehouse/src/data_sources/build',
#     '/home/tom/git/home/pokemon-tcg-data-data-warehouse/src/data_sources/data_source_cache/PokemonTcgApi/data/pokemon-tcg-data-master'
# )


# CHeck if generated ids match set + number
# uniqueness

kek = 1


