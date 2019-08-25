from argparse import ArgumentParser
from opentargets import OpenTargetsClient
import pandas as pd


class OTAR_result_parser():
    def __init__(self, OTAR_response, verbose = False):

        # Try to read the response as a dataframe:
        try:
            self.OT_result_df = OTAR_response.to_dataframe()
        except AttributeError:
            raise AttributeError("[Error] OTAR_result_parser expects 'opentargets.conn.IterableResult'")

    # Get the average association scores:
    def get_association_score_mean(self):
        return self.OT_result_df['association_score.overall'].mean()

    # Get the lowest association scores:
    def get_association_score_min(self):
        return self.OT_result_df['association_score.overall'].min()

    # Get the highest association score:
    def get_association_score_max(self):
        return self.OT_result_df['association_score.overall'].max()

    # Get the standard deviation of the association scores:
    def get_association_score_std(self):
        return self.OT_result_df['association_score.overall'].std()

    # Get a dataframe with target disease pairs with the corresponding association score:
    def get_target_disease_pairs(self):
        return self.OT_result_df[['target.id','disease.id','association_score.overall']]

    # Add other functionality:
    def __len__(self):
        return(len(self.OT_result_df))


def run_analysis(queryType, identifier, verbose = False):
    """ This function will run the actual analysis

    Args:
        queryType (str): based on what we are fetching data either disease or target
        identifier (str): disease ID or target ID depending on the query type.
        verbose (bool): if we want extra information printed to STDOUT
    Returns:
        Dictionary:
        {
            "queryTerm" : <str>
            "target-disease-pairs" : <pandas.dataframe>,
            "score_max" : <float>,
            "score_min" : <float>,
            "score_mean" : <float>,
            "score_std" : <float>
        }

        The analysis values might be None if there are no returned values.
    """

    # Initializing output variable:
    analysisOutput = {
        "queryTerm" : identifier,
        "target-disease-pairs" : None,
        "score_max" : None,
        "score_min" : None,
        "score_mean" : None,
        "score_std" : None
    }

    # Initializing OTAR query object:
    client = OpenTargetsClient()
    otar_results = client.filter_associations()

    # Retrieving queried data:
    x = otar_results.filter(**{queryType : identifier})

    # Submit result to parser:
    OT_parser = OTAR_result_parser(x, verbose=verbose)

    # If the result set is empty, we can't get stats:
    if not len(OT_parser):
        if verbose: print('[Warning] The result set is empty. Can\'t calculate stats.')
        return analysisOutput

    if verbose: print('[Info] Number of associations: {}'.format(len(OT_parser)))

    # Retrieving target-disease pairs:
    analysisOutput['target-disease-pairs'] = OT_parser.get_target_disease_pairs()

    # Retrieving stats of the association scores:
    analysisOutput['score_max'] = OT_parser.get_association_score_max()
    analysisOutput['score_min'] = OT_parser.get_association_score_min()
    analysisOutput['score_mean'] = OT_parser.get_association_score_mean()
    analysisOutput['score_std'] = OT_parser.get_association_score_std()

    return analysisOutput


# The command line wrapper for the result parser package:
def main():
    parser = ArgumentParser(description=("A small command line tool to demonstrate the capabilities of the Opentargets parser module. "
                                         "At this stage, it shows statistics of the association scores in a result set of a target "
                                         "or disease specific query."))

    parser.add_argument('-t', '--target', dest='target', help='Specify target ID. eg. ENSG00000197386.', required=False, type=str)
    parser.add_argument('-d', '--disease', dest='disease', help='Specify disease ID. eg. Orphanet_399', required = False,  type=str)
    parser.add_argument('-v', '--verbose', dest='verbose', help='Prints out extra information', required=False, action='store_true')

    args = parser.parse_args()
    verbose = args.verbose

    # At least one of the arguments is required:
    if not (args.target or args.disease):
        parser.error('Target or disease has to be specified with the -t or -d switches respectively.')

    # fill out anaysis output:
    analysisResult = {}
    if args.target:
        if verbose: print('[Info] The following target is queried from Opentargets: {}'.format(args.target))
        analysisResult['target'] = run_analysis('target', args.target, verbose)
    if args.disease:
        if verbose: print('[Info] The following disease is queried from Opentargets: {}'.format(args.disease))
        analysisResult['disease'] = run_analysis('disease', args.disease, verbose)

    # print target/disease pairs for target and disease oriented search:
    for queryType in ['target', 'disease']:
        if queryType not in analysisResult:
            continue
        elif isinstance(analysisResult[queryType]['target-disease-pairs'], pd.DataFrame):
            print('\n[Info] {} as {} ID returned the following associations:'.format(analysisResult[queryType]['queryTerm'], queryType))
            analysisResult[queryType]['target-disease-pairs'].apply(lambda row: print(
                'Assoc #{} - Target ID: {}, disease ID: {}, association score: {}'.format(row.name, row['target.id'],
                                                                      row['disease.id'],row['association_score.overall'])),
                 axis=1)
        else:
            print('\n[Warning] {} as {} ID returned no association.'.format(analysisResult[queryType]['queryTerm'], queryType))

    # Print association score stats for the target and disease oriented search:
    for queryType in ['target', 'disease']:
        if queryType not in analysisResult:
            continue
        elif isinstance(analysisResult[queryType]['target-disease-pairs'], pd.DataFrame):
            print('\n\n[Info] Association score stats for the {} based query for {}:'.format(queryType, analysisResult[queryType]['queryTerm']))
            print('\tThe maximum of the association_score.overall values: {}'.format(analysisResult[queryType]['score_max']))
            print('\tThe minimum of the association_score.overall values: {}'.format(analysisResult[queryType]['score_min']))
            print('\tThe average of the association_score.overall values: {}'.format(analysisResult[queryType]['score_mean']))
            print('\tThe standard error of the association_score.overall values: {}'.format(analysisResult[queryType]['score_std']))
        else:
            print('\n\n[Warning] {} as {} ID returned no association.'.format(analysisResult[queryType]['queryTerm'], queryType))


if __name__ == '__main__':
    main()
