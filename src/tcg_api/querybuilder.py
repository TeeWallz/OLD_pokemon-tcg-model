import math

from dacite import from_dict
from tqdm import tqdm

from tcg_api.restclient import RestClient
from tcg_api.config import __endpoint__


class QueryBuilder():
    def __init__(self, type, transform=None):
        self.params = {}
        self.type = type
        self.transform = transform

    def all(self, db, callback):
        """Get all resources, automatically paging through data

        Returns:
            list of object: List of resource objects
        """
        list = []
        fetch_all = True
        url = "{}/{}".format(__endpoint__, self.type)


        if 'page' in self.params:
            fetch_all = False
        else:
            self.params['page'] = 1

        # Peek to get total pages
        response = RestClient.get(url, self.params)
        total_pages = math.ceil(response['totalCount'] / response['pageSize'])
        pbar = tqdm(total=total_pages)

        # In-case count above fails, just keep pulling
        while True:
            response = RestClient.get(url, self.params)['data']
            if len(response) > 0:
                # list.extend([item for item in response])
                callback(db, response, self.type)

                if fetch_all:
                    self.params['page'] += 1
                else:
                    break
            else:
                break
            pbar.update(1)

        return list
