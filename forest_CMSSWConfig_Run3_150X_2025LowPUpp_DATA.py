### HiForest CMSSW Configuration
# Collisions: 2025 Low PU pp
# Input: miniAOD
# Type: data
# SW: CMSSW_15_0_15_patch4, forest_CMSSW_15_0_X

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_2025_cff import Run3_2025
process = cms.Process('HiForest', Run3_2025)

HIFOREST_VERSION = "150X"
GLOBAL_TAG = "150X_dataRun3_Express_v2"
INPUT_TEST_FILE = "/store/group/phys_heavyions/wangj/RECO2025PbPb/miniaod_SpecialHLTPhysics0_398647/ppreco2miniaod_RAW2DIGI_L1Reco_RECO_PAT.root"
INPUT_MAX_EVENTS    = 200
OUTPUT_FILE_NAME    = "HiForest_2025LowPUpp.root"

INCLUDE_CENTRALITY  = False
INCLUDE_FSC         = False
INCLUDE_HLT_OBJ     = True
INCLUDE_JETS        = True # ak jets
_jetPtMin           = 15
_jetAbsEtaMax       = 2.5
_jetLabels          = ["0"] # "0" for original mini-AOD jets, otherwise use R value, e.g. 3,4,8
INCLUDE_L1_OBJ      = True
INCLUDE_MUONS       = False
INCLUDE_PF_TREE     = False
_pfPtMin            = 0.1
_pfAbsEtaMax        = 6.0
INCLUDE_PPS         = False
INCLUDE_TRACKS      = True
_doTrackDedx        = False
_trackPtMin         = 0.3
_trackEtaMax        = 3.0
INCLUDE_ZDC         = False

DEBUG_EDM           = False

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD," + HIFOREST_VERSION + ", data")

# load Global Tag, geometry, etc.
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, GLOBAL_TAG, '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
         INPUT_TEST_FILE
    ),
)

# number of events to process, set to -1 to process all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(INPUT_MAX_EVENTS)
)

# root output
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(OUTPUT_FILE_NAME)
)

# edm output for debugging purposes
if DEBUG_EDM :
    process.output = cms.OutputModule(
       "PoolOutputModule",
       fileName = cms.untracked.string('HiForestEDM.root'),
       outputCommands = cms.untracked.vstring(
           'keep *',
       )
    )
    process.output_path = cms.EndPath(process.output)

###############################################################################

# Define centrality binning
if INCLUDE_CENTRALITY :
    process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
    process.centralityBin.Centrality = cms.InputTag("hiCentrality")
    process.centralityBin.centralityVariable = cms.string("HFtowers")

# event analysis
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')
process.load('L1Trigger.L1TNtuples.l1MetFilterRecoTree_cfi')
if INCLUDE_PF_TREE :
    process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
    process.particleFlowAnalyser.ptMin = cms.double(_pfPtMin)
    process.particleFlowAnalyser.absEtaMax = cms.double(_pfAbsEtaMax)
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.hiEvtAnalyzer.doHFfilters = cms.bool(False)
process.hiEvtAnalyzer.doCentrality = cms.bool(False)
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
if INCLUDE_HLT_OBJ :
    process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
    process.hltobject.triggerNames = cms.vstring()
if INCLUDE_L1_OBJ :
    process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

# electrons, photons, muons
process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
process.ggHiNtuplizer.doGenParticles = cms.bool(False)
process.ggHiNtuplizer.doMuons = cms.bool(False)
process.ggHiNtuplizer.useValMapIso = cms.bool(False) # True here causes seg fault
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

# tracks
if INCLUDE_TRACKS :
    process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
    process.ppTracks.trackPtMin = cms.untracked.double(_trackPtMin)
    process.ppTracks.trackEtaMax = cms.untracked.double(_trackEtaMax)
    if _doTrackDedx :
        process.ppTracks.dedxEstimators = cms.VInputTag([
          "dedxEstimator:dedxAllLikelihood",
          "dedxEstimator:dedxPixelLikelihood",
          "dedxEstimator:dedxStripLikelihood"
        ])

# muons
if INCLUDE_MUONS :
    process.load("HeavyIonsAnalysis.MuonAnalysis.unpackedMuons_cfi")
    process.unpackedMuons.muonSelectors = cms.vstring()
    process.load("HeavyIonsAnalysis.MuonAnalysis.muonAnalyzer_cfi")
    process.unpackedMuons.muonSelectors = cms.vstring()

# ZDC RecHit Producer && Analyzer
# to prevent crash related to HcalSeverityLevelComputerRcd record
process.load("RecoLocalCalo.HcalRecAlgos.hcalRecAlgoESProd_cfi")
if INCLUDE_ZDC :
    process.load('HeavyIonsAnalysis.ZDCAnalysis.ZDCAnalyzersPbPb_cff')
if INCLUDE_FSC :
    process.load('HeavyIonsAnalysis.ZDCAnalysis.FSCAnalyzers_cff')
if INCLUDE_PPS :
    process.load('HeavyIonsAnalysis.ZDCAnalysis.PPSAnalyzers_cff')

###############################################################################

# main forest sequence
process.forest = cms.Path(
    process.HiForestInfo +
    process.hltanalysis +
    process.l1MetFilterRecoTree +
    process.trackSequencePP +
    process.hiEvtAnalyzer
)

if INCLUDE_HLT_OBJ :
     process.forest += process.hltobject
if INCLUDE_L1_OBJ :
     process.forest += process.l1object
if INCLUDE_PF_TREE :
    process.forest += process.particleFlowAnalyser
if INCLUDE_CENTRALITY :
    process.forest += process.centralityBin
if INCLUDE_ZDC :
    process.forest += process.zdcSequencePbPb
if INCLUDE_FSC :
    process.forest += process.fscSequence
if INCLUDE_PPS :
    process.forest += process.ppsSequence
if INCLUDE_MUONS :
    process.forest += process.ggHiNtuplizer
    process.forest += process.unpackedMuons
    process.forest += process.muonAnalyzer

###############################################################################

# jet reco sequence
if INCLUDE_JETS :
    process.load('HeavyIonsAnalysis.JetAnalysis.ak4PFJetSequence_ppref_data_cff')

    # Select the types of jets filled
    matchJets = True        # Enables q/g and heavy flavor jet identification in MC

    # Choose which additional information is added to jet trees
    doHIJetID = True        # Fill jet ID and composition information branches
    doWTARecluster = False  # Add jet phi and eta for WTA axis
    doBtagging  =  False    # Note that setting to True increases computing time a lot

    # 0 means use original mini-AOD jets, otherwise use R value, e.g., 3,4,8
    # Add all the values you want to process to the list
    jetLabels = _jetLabels

    # add candidate tagging for all selected jet radii
    from HeavyIonsAnalysis.JetAnalysis.setupJets_ppRef_cff import candidateBtaggingMiniAOD

    for jetLabel in jetLabels:
        candidateBtaggingMiniAOD(
            process,
            isMC = False,
            jetPtMin = _jetPtMin,
#            jetCorrLevels = ['L2Relative', 'L3Absolute'],
            jetCorrLevels = ['L2Relative', 'L2L3Residual'],
            doBtagging = doBtagging,
            labelR = jetLabel
        )

        # setup jet analyzer
        setattr(process,"ak"+jetLabel+"PFJetAnalyzer",process.ak4PFJetAnalyzer.clone())
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").jetTag = "selectedUpdatedPatJetsAK"+jetLabel+"PFCHSBtag"
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").jetName = 'ak'+jetLabel+'PF'
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").matchJets = matchJets
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").matchTag = 'patJetsAK'+jetLabel+'PFUnsubJets'
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").doBtagging = doBtagging
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").doHiJetID = doHIJetID
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").doWTARecluster = doWTARecluster
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").jetPtMin = _jetPtMin
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").jetAbsEtaMax = cms.untracked.double(_jetAbsEtaMax)
        getattr(process,"ak"+jetLabel+"PFJetAnalyzer").rParam = 0.4 if jetLabel=='0' else float(jetLabel)*0.1
        if doBtagging:
            getattr(process,"ak"+jetLabel+"PFJetAnalyzer").pfJetProbabilityBJetTag = cms.untracked.string("pfJetProbabilityBJetTagsAK"+jetLabel+"PFCHSBtag")
            getattr(process,"ak"+jetLabel+"PFJetAnalyzer").pfUnifiedParticleTransformerAK4JetTags = cms.untracked.string("pfUnifiedParticleTransformerAK4JetTagsAK"+jetLabel+"PFCHSBtag")
        process.forest += getattr(process,"ak"+jetLabel+"PFJetAnalyzer")

#Winter25Prompt25_RunF_V2_DATA

###############################################################################

# Event Selection -> add the needed filters here
process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
#process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
process.load('HeavyIonsAnalysis.EventAnalysis.hffilterPF_cfi')
process.pAna = cms.EndPath(process.skimanalysis)

#process.HFAdcana = cms.EDAnalyzer("HFAdcToGeV",
#    digiLabel = cms.untracked.InputTag("hcalDigis"),
#    #digiLabel = cms.untracked.InputTag("simHcalUnsuppressedDigis","HFQIE10DigiCollection"),
#    minimized = cms.untracked.bool(True),
#    fillhf = cms.bool(False) # only turn this on when you have or know how to produce "towerMaker"
#)
#process.hfadc = cms.Path(process.HFAdcana)

process.MessageLogger.cerr.FwkReport.reportEvery = 100

