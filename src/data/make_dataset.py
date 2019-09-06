# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd


@click.command()
@click.argument('input_filepath', 
                default='data/raw/chr_measures_CSV_2018.csv',
                type=click.Path(exists=True))
@click.argument('interim_filepath', 
                default='data/interim/chr_interim_2018.csv',
                type=click.Path())
@click.argument('processed_filepath', 
                default='data/processed/chr_final_2018.csv',
                type=click.Path())
@click.option('-i', '--index', 
              default='county-name',
              type=click.Choice(['fips-code', 'county-name']))
# . TODO: Add columns to keep as a CLI option?
def main(input_filepath, interim_filepath, processed_filepath, index):
    """ Process raw data
    
        Run data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../interim).
        
        Run from top level directory (project root)
        
        Data download: 
        http://www.countyhealthrankings.org/sites/default/files/chr_measures_CSV_2018.csv
        Data documentation
        https://www.countyhealthrankings.org/sites/default/files/CHR2018_CSV_SAS_documentation.pdf
    """
    logger = logging.getLogger(__name__)
    
    logger.info('Reading raw data from {}'.format(input_filepath))
    sdoh_data = pd.read_csv(input_filepath, 
                            dtype={'year': object, '5-Digit FIPS Code': object})
    
    measure_id_map = {
            'Length of Life Premature death': (1),
            'Quality of Life Poor or fair health': (2),
            'Poor physical health days': (36),
            'Poor mental health days': (42),
            'Low birthweight': (37),
            'Tobacco Use Adult smoking': (9),
            'Adult obesity': (11),
            'Food environment index': (133),
            'Physical inactivity': (70),
            'Access to exercise opportunities':(132),'Excessive drinking': (49),
            'Alcohol-impaired driving deaths': (134),
            'Sexual Activity Sexually transmitted infections': (45) ,
            'Teen births': (14) ,
            'Access to Care Uninsured': (85) ,
            'Primary care physicians': (4) ,
            'Dentists': (88) ,
            'Mental health providers': (62) ,
            'Quality of Care Preventable hospital stays': (5) ,
            'Diabetes monitoring': (7) ,
            'Mammography screening': (50) ,
            'Education High school graduation': (21) ,
            'Some college': (69),
            'Employment Unemployment': (23) ,
            'Income Children in poverty': (24),
            'Income inequality': (44),
            'Children in single-parent households': (82) ,
            'Social associations': (140) ,
            'Violent crime': (43) ,
            'Injury deaths':(135) ,
            'Air pollution – particulate matter 1': (125) ,
            'Drinking water violations':(124) ,
            'Severe housing problems': (136) ,
            'Driving alone to work': (67) ,
            'Long commute – driving alone': (137) ,
            'Premature age-adjusted mortality': (127),
            'Infant mortality': (129) ,
            'Child mortality': (128) ,
            'Frequent physical distress': (144) ,
            'Frequent mental distress': (145) ,
            'Diabetes prevalence': (60) ,
            'HIV prevalence': (61) ,
            'Food insecurity': (139) ,
            'Limited access to healthy foods': (83),
            'Motor vehicle crash deaths': (39) ,
            'Drug overdose deaths': (138) ,
            'Drug overdose deaths modeled': (146) ,
            'Insufficient sleep': (143) ,
            'Uninsured adults': (3),
            'Uninsured children': (122),
            'Health care costs': (86) ,
            'Other primary care providers': (131) ,
            'Disconnected youth': (149) ,
            'Median household income': (63) ,
            'Children eligible for free or reduced price lunch': (65) ,
            'Homicides': (15) ,
            'Firearm fatalities': (148) ,
            'Residential segregation—black/white': (141) ,
            'Residential segregation—non-white/white': (142) ,
            'Population': (51) ,
            'below 18 years of age': (52) ,
            '65 and older': (53) ,
            'Non-Hispanic African American': (54),
            'American Indian and Alaskan Native': (55) ,
            'Asian': (81) ,
            'Native Hawaiian/Other Pacific Islander': (80) ,
            'Hispanic': (56),
            'Non-Hispanic white': (126) ,
            'not proficient in English': (59),
            'Females': (57) ,
            'Rural': (58)}
    
    # Rename columns
    id_measure_map = {v: k for (k, v) in measure_id_map.items()}

    def rename_col(x):
        try:
            measure, number, category = x.strip().split('_')
            name = id_measure_map[int(number)]
            return name + '_' + category
        except (ValueError, KeyError):
            # Not a column with double underscores OR not a number that has a column name
            logging.debug('Skipped column {}'.format(x))
            return x

    logger.info('Renaming Columns')
    sdoh_data.columns = sdoh_data.columns.map(rename_col)
    
    # Make sure there the dataset is only one year and it's 2018
    assert(sdoh_data['year'].value_counts().index.values == ['2018'])
    
    if index == 'fips-code':
        sdoh_data.index = sdoh_data['5-Digit FIPS Code']
    elif index == 'county-name':
        county_name = sdoh_data['county'].fillna('').apply(
            lambda x: x.replace(' County', '')
        )
        county_index = county_name + ',' + sdoh_data['state']
        sdoh_data.index = county_index
    else:
        logging.warning('Not resetting index')

    sdoh_data = sdoh_data.drop(
            ['FIPS State Code', 'FIPS County Code', 'year', '5-Digit FIPS Code'], axis=1
    )
    
    sdoh_data.index.name = 'index'
    
    logger.info('Writing interim dataset to {}'.format(interim_filepath))
    sdoh_data.to_csv(interim_filepath)
    
    # Could update script to pass this as an argument (comma separated string, filepath)
    columns_to_keep = ['Median household income_value',
                       'Social associations_value',
                       'Access to exercise opportunities_value',
                       'Limited access to healthy foods_value',
                       'Long commute – driving alone_value',
                       'Rural_value',
                       'not proficient in English_value']
    
    # Drop na values, including FIPS na, which indicates higher level state, county, etc
    msg = 'Writing final dataset to {}'.format(processed_filepath)
    logger.info(msg)
    sdoh_data = sdoh_data[columns_to_keep].reset_index().dropna().set_index('index')
    sdoh_data.to_csv(processed_filepath)
    

if __name__ == '__main__':
    # Add timestamp to logging output
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
