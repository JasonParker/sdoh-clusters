import pickle
import logging
from pathlib import Path
import pandas as pd


class AnalyticsManager(object):
    """Load model, read in new data, make predictions and write results
    
    Parameters
    ----------
    model_filepath: str
        path of the pickled sklearn.cluster.k_means_.KMeans model
        
    input_filepath: str
        location of the new data to be classified
    """
    
    def __init__(self, model_filepath, input_filepath=None):
        self.model_filepath = model_filepath
        
        if input_filepath:
            self.input_filepath = input_filepath
        else:
            project_dir = Path(__file__).resolve().parents[2]
            self.input_filepath = project_dir / 'data' / 'raw' / 'new_samples.csv'
            
        self.predictions = None
        
        with open(self.model_filepath, 'rb') as infile:
            self.model = pickle.load(infile)
            
        logging.info('Pickled model successfuly loaded from {}'.format(self.model_filepath))
        
        # If wanting to connect to SQL to load new members, 
        # write & call DatabaseProvider class here:
        # self.database_provider = src.data.databaseprovider.DatabaseProvider()

    def _clean(self):
        """ETL - done in command line script, but in production would be here"""
        columns = self.model['input_format']
        self.data = self.data[columns].dropna()

    def _predict_clusters(self):
        # do transform
        number_new_samples = self.data.shape[0]
        
        logging.info('Computing clusters for {} samples'.format(number_new_samples))
        
        scaled_df = self.model['scaler'].transform(self.data)
        predictions = self.model['kmeans'].predict(scaled_df)
        
        # Map cluster numbers to names
        label_map = self.model['label_map']
        predictions = [label_map[cluster_number] for cluster_number in predictions]
        
        self.predictions = predictions
        
    def process(self):
        """Load and clean data, predict, and return predicted clusters
        
        Would typically use custom database_provider here:
        self.database_provider.load_data()...etc
        
        Instead we will just read from a test dataframe in this example
        """
        self.data =  pd.read_csv(self.input_filepath)  # is in init in clustermanager
        self._clean()
        self._predict_clusters()
        
        return self.predictions

    def write_results(self):
        """Use databaseprovider to write results to staging table or applicable location"""
        raise NotImplementedError
#         if self.predictions:
#             self.database_provider.write_results(self.predictions)
#         else:
#             raise Exception('No predictions. Run AnalyticsManager().process() before writing predictions')
           
        
# Test with main
# For production - could write another command line script using click and run regularly
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # filename='example.log'
    
    project_dir = Path(__file__).resolve().parents[2]
    model_filepath = project_dir / 'models' / 'final_clustering.pkl'
    
    manager = AnalyticsManager(model_filepath)
    manager.process()
    
    print(manager.predictions)
    # manager.write_results()
