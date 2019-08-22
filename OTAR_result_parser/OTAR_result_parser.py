from argparse import ArgumentParser
from opentargets import OpenTargetsClient


class OTAR_result_parser():
    def __init__(self, OTAR_response, verbose = False):

        # Try to read the response as a dataframe:
        try:
            self.OT_result_df = OTAR_response.to_dataframe()
        except AttributeError:
            raise AttributeError("[Error] OTAR_result_parser expects 'opentargets.conn.IterableResult'")

        # Get the number of associations:
        if verbose:
            self.__get_stats()

    # If the verbose flag is set, a
    def __get_stats(self):
        print('[Info] Number of association in the response: {}'.format(len( self.OT_result_df)))

    # Get the average association scores:
    def get_association_score_mean(self):
        return self.OT_result_df['association_score.overall'].mean()

    # Get the lowest association scores:
    def get_association_score_min(self):
        return self.OT_result_df['association_score.overall'].min()

    # Get the highest association scores:
    def get_association_score_max(self):
        return self.OT_result_df['association_score.overall'].max()

    # Get the standard deviation of the association scores:
    def get_association_score_std(self):
        return self.OT_result_df['association_score.overall'].std()

    # Add other functionality:
    def __len__(self):
        return(len(self.OT_result_df))

# The command line wrapper for the result parser package:
def __main__():
    parser = ArgumentParser(description="A small tool to retrieve association information from Opentargets based on a provided target or disease.")

    parser.add_argument('-t', '--target', dest='target', help='Target name eg. ENSG00000197386.', required=False, type=str)
    parser.add_argument('-d', '--disease', dest='disease', help='Name of schema eg. association. eg. Orphanet_399', required = False,  type=str)
    parser.add_argument('-v', '--verbose', dest='verbose', help='Prints out extra information', required=False, action='store_true')

    args = parser.parse_args()
    verbose = args.verbose

    # At least one of the arguments is required:
    if not (args.target or args.disease):
        parser.error('Target or disease has to be specified with the -t or -d switches respectively.')

    # The two arguments are mutually exclusive:
    if args.target and args.disease:
        parser.error('Target or disease has to be specified with the -t or -d switches respectively.')

    # If the input looks good, let's submit the query:
    client = OpenTargetsClient()
    otar_results = client.filter_associations()

    if args.target:
        if verbose: print('[Info] The following target is queried from Opentarget: {}'.format(args.target))
        x = otar_results.filter(target=args.target)
    elif args.disease:
        if verbose: print('[Info] The following disease is queried from Opentarget: {}'.format(args.disease))
        x = otar_results.filter(disease=args.disease)

    # Parse the result:
    OT_parser = OTAR_result_parser(x, verbose=verbose)

    # If the result set is empty, we can't get stats:
    if not len(OT_parser):
        print('[Error] The result set is empyt. Can\'t calculate stats. Exiting.')
        quit()

    # Generate the output:
    print('[Info] The maximum of the association_score.overall values: {}'.format(OT_parser.get_association_score_max()))
    print('[Info] The minimum of the association_score.overall values: {}'.format(OT_parser.get_association_score_min()))
    print('[Info] The average of the association_score.overall values: {}'.format(OT_parser.get_association_score_mean()))
    print('[Info] The standard error of the association_score.overall values: {}'.format(OT_parser.get_association_score_std()))


if __name__ == '__main__':
    __main__()
