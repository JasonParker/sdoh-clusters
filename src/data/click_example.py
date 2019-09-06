# -*- coding: utf-8 -*-
import click
import logging

logger = logging.getLogger(__name__)


@click.command()
@click.argument('your_name', default='Erica')
@click.argument('favorite_pasta', default='bow tie')
@click.option('--logging_level', '-l', default='DEBUG',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']))
def main(your_name, favorite_pasta, logging_level):
    """ Basic example of click command line tool"""
    logging.basicConfig(level=logging_level, filename='example.log')

    introduction = '\nHi, my name is {} and my favorite pasta is {}\n'.format(
        your_name, favorite_pasta)

    print(introduction)
    logger.info(introduction)

    if favorite_pasta == 'bow tie':
        logger.warning('\nUser may not have entered a favorite pasta!\n')

    msg = '\nSome really detailed message that only someone who writes lots of code could love\n'
    logger.debug(msg)
    

if __name__ == '__main__':
    main()
