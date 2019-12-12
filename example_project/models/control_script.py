import os, re
import site
import pandas as pd

from io import StringIO

import tellurium as te
from pycotools3 import model, tasks, viz

import seaborn
seaborn.set_context(context='talk')

# Add path to sources root to Python's PATH variable
site.addsitedir(os.path.dirname(os.path.dirname(os.path.abspath(''))))
# note: Pycharm already doesn't this for you. But doesn't hurt to add it here anyway

copasiBinPath = "/Applications/copasi"

if not re.search(copasiBinPath, os.environ["PATH"]):
    os.environ["PATH"] += os.pathsep + copasiBinPath

# Go and get the model string by importing it from your models_strings module
from example_project.models.model_strings import model_string, model_string_ex

# imports all the global variables (notice that we can print out the WORKING_DIRECTORY variable)
from example_project import *


# Any functions or classes you write will go here

if __name__ == '__main__':

    # Any code that uses the functions or classes your have created above,
    #  will go here. We will be using flags defined in our __init__.py
    #  to modify the behaviour of this script. Since the Flags are boolean,
    #  we just us a simple if statement for each of them

    #fname="/Users/peter/Documents/GitHub/ExampleProject/example_project/models/BIOMD0000000560_url.xml"

    working_directory = os.path.abspath('')  # create a base directory to work from
    copasi_filename = os.path.join(working_directory, 'myToyModel.cps')

    copasi_ex_filename = os.path.join(working_directory, 'myExampleModel.cps')

    #te.setDefaultPlottingEngine('matplotlib')
    #r = te.loadSBMLModel(fname)
    #print(r.getCurrentAntimony())

    #print(te.sbmlToAntimony(fname))

    #myTeMod=te.loada(model_string)
    #myPctMod=model.loada(model_string,copasi_filename)
    #myPctMod.open()

    #myTeMod.simulate(0, 100, 100)
    #myTeMod.plot()

    #pctSimData = tasks.TimeCourse(myPctMod, end=100, step_size=1, intervals=100)
    #viz.PlotTimeCourse(pctSimData, savefig=True)

    #myTeSS = myTeMod.getSteadyStateValues()
    #print(myTeSS)
    #for sid, value in zip(myTeMod.steadyStateSelections, myTeMod.getSteadyStateValues()):
    #    print(sid, "=", value)


    myData="""
Time,P
0,0.1
15,0.1
30,0.1
45,0.1
60,1
70,1
80,1
90,1
    """


    calDataFName=os.path.join(working_directory, 'toyModelCalData.csv')
    f = StringIO(myData)
    myData = pd.read_csv(f)
    print(myData)
    myData.to_csv(calDataFName)
    if False:
        pctPlSimData = myPctMod.simulate(0, 100, 1)
        plDataFName = os.path.join(working_directory, 'toyModelPlData.csv')
        pctPlSimData.to_csv(plDataFName)

    if False:
        # profile likelyhoods can't handel 0 value paramiters because it divides by them
        with tasks.ParameterEstimation.Context(myPctMod, plDataFName, context='pl', parameters='gm') as context:
            #context.set('randomize_start_values', True)
            context.set('separator', ',')
            context.set('method', 'hooke_jeeves')
            context.set('pl_lower_bound', 1000)
            context.set('pl_upper_bound', 1000)
            #context.set('population_size', 50)
            #context.set('number_of_generations', 300)
            context.set('run_mode', True)  ##defaults to False
            context.set('pe_number', 3)  ## number of repeat items in scan task
            #context.set('copy_number', 2)  ## number of times to copy model
            #context.set('problem', 'Problem1')
            #context.set('fit', 3)
            #context.set('prefix', 'k')
        config = context.get_config()

        pe = tasks.ParameterEstimation(config)

        #myPctMod.open()
        data = viz.Parse(pe)
        print(data)

    myExMod = model.loada(model_string_ex, copasi_ex_filename)

    def my_add_cols(inFName,outFName,sState,i1State,i2State):
        myData = pd.read_csv(os.path.join(os.path.dirname(working_directory), 'data', inFName))
        myData.insert(len(myData.columns), 'S_indep', sState)
        myData.insert(len(myData.columns), 'I1_indep', i1State)
        myData.insert(len(myData.columns), 'I2_indep', i2State)
        myData.rename(columns={"pN": "Np", "pG": "Gp", "pD": "Dp", "pK": "Kp"}, inplace=True)
        myData.to_csv(os.path.join(working_directory, outFName))


    my_add_cols('S.csv','S_ex_data.csv',1,0,0)
    my_add_cols('SI1.csv', 'I1_ex_data.csv', 1, 1, 0)
    my_add_cols('SI2.csv', 'I2_ex_data.csv', 1, 0, 1)
    my_add_cols('SI.csv', 'I_ex_data.csv', 1, 1, 1)

    exDataFNames=['S_ex_data.csv','I1_ex_data.csv','I2_ex_data.csv','I_ex_data.csv']
    exDataFNames=[os.path.join(working_directory, FName) for FName in exDataFNames]

    copy_number=3

    with tasks.ParameterEstimation.Context(myExMod, exDataFNames, context='s', parameters='g') as context:
        context.set('randomize_start_values', True)
        context.set('separator', ',')
        context.set('method', 'hooke_jeeves')
        # context.set('population_size', 50)
        # context.set('number_of_generations', 300)
        context.set('run_mode', 'parallel')  ##defaults to False
        context.set('pe_number', 1)  ## number of repeat items in scan task
        context.set('copy_number', copy_number)  ## number of times to copy model
        context.set('problem', 'Example')
        context.set('fit', 1)
        context.set('prefix', '_')
    config = context.get_config()

    pe = tasks.ParameterEstimation(config)

    viz.WaterfallPlot(pe)

    data = viz.Parse(pe)
    data['myExampleModel'].to_csv('my_ex_pe.csv')

    if PRINT_WORKING_DIRECTORY:
        # prints /home/ncw135/Documents/ExampleProject/example_project
        print(WORKING_DIRECTORY)







