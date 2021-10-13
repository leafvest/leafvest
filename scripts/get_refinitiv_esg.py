"""Get ESG scores for each US Stock"""

import csv
import aiohttp
import asyncio

from pprint import pprint
from datetime import date
from typing import Any, Dict, Generator, List

JSON = Any
Session = Any

REFINITIV_ESG = 'https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode='

ABC = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

REFINITIV_ESG_FIELDNAMES = [
    'symbol', 'date', 'esg_score',
    'environment', 'environment_emissions', 'environment_resource_use', 'environment_innovation',
    'social', 'social_human_rights', 'social_product_responsibility', 'social_workforce', 'social_community',
    'governance', 'governance_management', 'governance_shareholders', 'governance_csr_strategy'
]


def usa_tickers() -> Generator[str, None, None]:
    """Generates all USA company tickers"""
    with open('data/company.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Country'] == 'United States':
                yield row['Symbol']


async def get_json(url: str, session: Session) -> JSON:
    """Get json-like dictionary from given `url`"""
    async with session.get(url) as resp:
        resp = await resp.json()
        return resp


async def get_refinitiv_esg_score(ticker: str, session: Session) -> JSON:
    """Get ESG scores for the given ticker from Refinitiv"""
    
    print('TRY ' + ticker)

    esg_row_data = await get_json(f'{REFINITIV_ESG}{ticker}', session)

    if not esg_row_data:
        for letter in ABC:
            print('TRY ' + ticker + '.' + letter)
            esg_row_data = await get_json(f'{REFINITIV_ESG}{ticker}.{letter}', session)
            if esg_row_data:
                break
            
    if not esg_row_data:
        print('MISSED ' + ticker)
        return None

    print('GOT ' + ticker)
    
    esg_data = {
        'symbol':                   ticker,
        'date':                     date.today(),
        'esg_score':                esg_row_data['esgScore']['TR.TRESG']['score'],
        'environment':              esg_row_data['esgScore']['TR.EnvironmentPillar']['score'], 
        'environment_emissions':    esg_row_data['esgScore']['TR.TRESGEmissions']['score'], 
        'environment_resource_use': esg_row_data['esgScore']['TR.TRESGResourceUse']['score'], 
        'environment_innovation':   esg_row_data['esgScore']['TR.TRESGInnovation']['score'],
        'social':                   esg_row_data['esgScore']['TR.SocialPillar']['score'],
        'social_human_rights':      esg_row_data['esgScore']['TR.TRESGHumanRights']['score'], 
        'social_product_responsibility': esg_row_data['esgScore']['TR.TRESGProductResponsibility']['score'], 
        'social_workforce':         esg_row_data['esgScore']['TR.TRESGWorkforce']['score'], 
        'social_community':         esg_row_data['esgScore']['TR.TRESGCommunity']['score'],
        'governance':               esg_row_data['esgScore']['TR.GovernancePillar']['score'],
        'governance_management':    esg_row_data['esgScore']['TR.TRESGManagement']['score'], 
        'governance_shareholders':  esg_row_data['esgScore']['TR.TRESGShareholders']['score'], 
        'governance_csr_strategy':  esg_row_data['esgScore']['TR.TRESGCSRStrategy']['score']
    }
    
    return esg_data


async def main() -> None:
    """Print ESG scores for each US Stock"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ticker in usa_tickers():
            tasks.append(get_refinitiv_esg_score(ticker, session))
        esg_scores: List[Dict[str, Any]] = await asyncio.gather(*tasks)

    with open('data/company_refinitiv_esg.csv', mode='w') as file:
        writer = csv.DictWriter(file, delimiter=',', restval='',
                                extrasaction='ignore', 
                                fieldnames=REFINITIV_ESG_FIELDNAMES)
        writer.writeheader()
        
        for esg_score in esg_scores:
            if esg_score:
                writer.writerow(esg_score)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        print('Finished')
