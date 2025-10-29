# 2025 PbPb
# CMSSW_15_1_X
# ZeroBias[0-??]

from CRABClient.UserUtilities import config
from CRABClient.UserUtilities import getUsername
username = getUsername()

###############################################################################
# INPUT/OUTPUT SETTINGS

pd = '0'
jobTag = 'PbPb_HIZeroBias' + pd
cmsswConfig = 'forest_CMSSWConfig_Run3_151X_2025PbPb_DATA.py'

isOnDAS = False
# If isOnDAS == True, use these inputs:
input = '/HIZeroBias' + pd + '/PbPbRun2025-PromptReco-v1/MINIAOD'
inputDatabase = 'global'
# Otherwise, use a filelist as input:
inputFilelist = 'filelist_HIZeroBias' + pd + '.txt'

output = '/store/group/phys_heavyions/' + username + '/Run3_2025PbPb_ExpressForests/'
outputServer = 'T2_CH_CERN'

###############################################################################

config = config()

config.General.requestName = jobTag
config.General.workArea = 'CrabWorkArea'
config.General.transferOutputs = True

config.JobType.psetName = cmsswConfig
config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 5000
config.JobType.pyCfgParams = ['noprint']
config.JobType.allowUndistributedCMSSW = True

if isOnDAS :
    config.Data.inputDataset = input
    config.Data.inputDBS = inputDatabase
    #config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions25pO/pO_golden.json'
    config.Data.splitting = 'EventAwareLumiBased'
    config.Data.unitsPerJob = 10000
    config.Data.totalUnits = -1
else :
    config.Data.outputPrimaryDataset = jobTag
    config.Data.userInputFiles = open(inputFilelist).readlines()
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 1
    config.Data.totalUnits = -1

config.Data.outLFNDirBase = output
config.Data.publication = False
config.Data.allowNonValidInputDataset = True

config.Site.storageSite = outputServer
