# Getting started using the Fire Risk Computation Library

The purpose of this lab is to do a very basic experiment with the frcm library which will serve as a starting point for the project work on developing the FireGuard software product.

Setup a new Python project with an associated virtual environment and install the most recent version of the frcm library: https://pypi.org/project/dynamic-frcm/

If you setup the project using poetry you may use poetry to add the library. Alternativ, you may create a simple Python project and install the library using pip.

Follow the steps described on https://pypi.org/project/dynamic-frcm/ in order to create a basic Python script that uses the frcm library to compute fire risks for a given location. This include getting the credentials required to retrieve weather data from the Norwegian Meteorological Institute.

You should also download the source files (tar.gz file) and have a look at the data model implementation used by the library. Knowledge of the data model will be needed in order to integrate the frcm library into your FireGuard software product.