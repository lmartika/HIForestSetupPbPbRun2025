### HiForest CMSSW Configuration
# Collisions: 2025 PbPb
# Input: miniAOD
# Type: data
# SW: CMSSW_15_1_0_patch3, forest_CMSSW_15_1_X

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_pp_on_PbPb_2025_cff import Run3_pp_on_PbPb_2025
process = cms.Process('HiForest', Run3_pp_on_PbPb_2025)

HIFOREST_VERSION = "151X"
GLOBAL_TAG = "151X_dataRun3_Prompt_v1"
INPUT_TEST_FILE = "/store/group/phys_heavyions/lamartik/RECO2025/test/recoPbPbrawPr2mini_RAW2DIGI_L1Reco_RECO_PAT.root"
INPUT_MAX_EVENTS    = 200
OUTPUT_FILE_NAME    = "HiForest_2025PbPbCalo.root"

INCLUDE_CENTRALITY  = False
INCLUDE_DFINDER     = False
_includeD0          = 1     # 1 if true, 0 if false
_includeLcpKpi      = 0     # 1 if true, 0 if false
_includeLcpKs       = 0     # 1 if true, 0 if false
_DtkPtMin           = 0.1
_DtkEtaMax          = 2.4
INCLUDE_EGAMMA      = True
INCLUDE_FSC         = True
INCLUDE_HLT_OBJ     = True
INCLUDE_JETS        = False # ak Jets
_jetPtMin           = 15
_jetAbsEtaMax       = 5
_jetLabels          = ["0"] # "0" uses reco jets, otherwise recluster with R value, e.g. 3,4,8
INCLUDE_CSJETS      = True # akCS Jets
_jetPtMinCS         = 15
_jetAbsEtaMaxCS     = 5
_jetLabelsCS        = ["4"] # R-values for collections of CS subtracted jets (only eta dependent background)
_jetLabelsFlowCS    = ["4"] # R-values for flow subtracted CS jets (eta and phi dependent background)
INCLUDE_L1_OBJ      = True
INCLUDE_MUONS       = True
INCLUDE_PF_TREE     = False
_pfPtMin            = 0.1
_pfAbsEtaMax        = 6.0
INCLUDE_PPS         = False # Only included in 2025 pO
INCLUDE_TRACKS      = True
_doTrackDedx        = True
_trackPtMin         = 0.3
_trackEtaMax        = 3.0
INCLUDE_ZDC         = True

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
process.load('L1Trigger.L1TNtuples.l1CaloTowerTree_cfi')
if INCLUDE_PF_TREE :
    process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
    process.particleFlowAnalyser.ptMin = cms.double(_pfPtMin)
    process.particleFlowAnalyser.absEtaMax = cms.double(_pfAbsEtaMax)
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.hiEvtAnalyzer.doHFfilters = cms.bool(False)
process.hiEvtAnalyzer.doCentrality = cms.bool(True) # True needed to get HF info
process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
if INCLUDE_HLT_OBJ :
    process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
    process.hltobject.triggerNames = cms.vstring()
if INCLUDE_L1_OBJ :
    process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')

# electrons, photons, muons
if INCLUDE_EGAMMA :
    process.load('HeavyIonsAnalysis.EGMAnalysis.ggHiNtuplizer_cfi')
    process.ggHiNtuplizer.doGenParticles = cms.bool(False)
    process.ggHiNtuplizer.doMuons = cms.bool(False)
    process.ggHiNtuplizer.useValMapIso = cms.bool(False) # True here causes seg fault
    process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

# tracks
if INCLUDE_TRACKS :
    process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
    process.PbPbTracks.trackPtMin = cms.untracked.double(_trackPtMin)
    process.PbPbTracks.trackEtaMax = cms.untracked.double(_trackEtaMax)
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
    process.l1CaloTowerTree +
    process.trackSequencePbPb +
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
if INCLUDE_EGAMMA :
    process.forest += process.ggHiNtuplizer
if INCLUDE_MUONS :
    process.forest += process.unpackedMuons
    process.forest += process.muonAnalyzer
if INCLUDE_ZDC or INCLUDE_FSC or INCLUDE_PPS :
    process.forest += process.zdcSequencePbPb
if INCLUDE_FSC :
    process.forest += process.fscSequence
if INCLUDE_PPS :
    process.forest += process.ppsSequence

###############################################################################

# jet reco sequence

# ak Jets (NOT CS jets)
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
            #jetCorrLevels = ['L2Relative', 'L3Absolute'],
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

# akCS Jets
if INCLUDE_CSJETS :
    process.load('HeavyIonsAnalysis.JetAnalysis.akCs4PFJetSequence_pponPbPb_data_cff')
    # Select the types of jets filled
    matchJets = False             # Enables q/g and heavy flavor jet identification in MC
    # Choose which additional information is added to jet trees
    doHIJetID = True             # Fill jet ID and composition information branches
    doWTARecluster = True        # Add jet phi and eta for WTA axis
    doBtagging  =  False         # Note that setting to True increases computing time a lot
    # Combine the two lists such that all selected jets can be easily looped over
    # Also add "Flow" tag for the flow jets to distinguish them from non-flow jets
    allJetLabels = _jetLabelsCS + [flowR + "Flow" for flowR in _jetLabelsFlowCS]
    # add candidate tagging
    from HeavyIonsAnalysis.JetAnalysis.setupJets_PbPb_cff import candidateBtaggingMiniAOD

    for jetLabel in allJetLabels:
        candidateBtaggingMiniAOD(
            process,
            isMC = False,
            jetPtMin = jetPtMin,
            jetCorrLevels = ['L2Relative', 'L2L3Residual'],
            doBtagging = doBtagging,
            labelR = jetLabel
        )
        # setup jet analyzer
        setattr(process,"akCs"+jetLabel+"PFJetAnalyzer",process.akCs4PFJetAnalyzer.clone())
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetTag = "selectedUpdatedPatJetsAK"+jetLabel+"PFBtag"
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetName = 'akCs'+jetLabel+'PF'
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").matchJets = matchJets
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").matchTag = 'patJetsAK'+jetLabel+'PFUnsubJets'
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").doBtagging = doBtagging
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").doHiJetID = doHIJetID
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").doWTARecluster = doWTARecluster
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetPtMin = _jetPtMinCS
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").jetAbsEtaMax = cms.untracked.double(_jetAbsEtaMaxCS)
        getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").rParam = 0.4 if jetLabel=="0" else float(jetLabel.replace("Flow",""))*0.1
        if doBtagging:
            getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").pfJetProbabilityBJetTag = cms.untracked.string("pfJetProbabilityBJetTagsAK"+jetLabel+"PFBtag")
            getattr(process,"akCs"+jetLabel+"PFJetAnalyzer").pfUnifiedParticleTransformerAK4JetTags = cms.untracked.string("pfUnifiedParticleTransformerAK4JetTagsAK"+jetLabel+"PFBtag")
        process.forest += getattr(process,"akCs"+jetLabel+"PFJetAnalyzer")

###############################################################################

# D finder
if INCLUDE_DFINDER :
    runOnMC       = False
    VtxLabel      = 'offlineSlimmedPrimaryVertices'
    TrkLabel      = 'packedPFCandidates'
    TrkChi2Label  = 'packedPFCandidateTrackChi2'
    GenLabel      = 'prunedGenParticles'
    from Bfinder.finderMaker.finderMaker_75X_cff import finderMaker_75X,setCutForAllChannelsDfinder
    finderMaker_75X(process, runOnMC, VtxLabel, TrkLabel, TrkChi2Label, GenLabel)
    process.Dfinder.tkPtCut = cms.double(_DtkPtMin) # before fit
    process.Dfinder.tkEtaCut = cms.double(_DtkEtaMax) # before fit
    process.Dfinder.Dchannel = cms.vint32(
        _includeD0, # K+pi- : D0bar
        _includeD0, # K-pi+ : D0
        0, # K-pi+pi+ : D+
        0, # K+pi-pi- : D-
        0, # K-pi-pi+pi+ : D0
        0, # K+pi+pi-pi- : D0bar
        0, # K+K-(Phi)pi+ : Ds+
        0, # K+K-(Phi)pi- : Ds-
        0, # D0(K-pi+)pi+ : D+*
        0, # D0bar(K+pi-)pi- : D-*
        0, # D0(K-pi-pi+pi+)pi+ : D+*
        0, # D0bar(K+pi+pi-pi-)pi- : D-*
        0, # D0bar(K+pi+)pi+ : B+
        0, # D0(K-pi+)pi- : B-
        _includeLcpKpi, # p+k-pi+: lambdaC+
        _includeLcpKpi, # p-k+pi-: lambdaCbar-
        _includeLcpKs,  # p+Ks(pi+pi-): lambdaC+
        _includeLcpKs   # p-Ks(pi+pi-): lambdaCbar-
    )
    setCutForAllChannelsDfinder(
        process,
        dPtCut = 0.,            # Accept if > dPtCut
        VtxChiProbCut = 0.05,   # Accept if > VtxChiProbCut
        svpvDistanceCut = 0.2,  # Accept if < svpvDistanceCut
        alphaCut = 4.           # Accept if < alphaCut (note: 0 < alpha < pi)
    )
    process.Dfinder.dPtCut = cms.vdouble( # Accept if > dPtCut
        0.1, 0.1,   # K+pi- : D0bar
        0.,  0.,    # K-pi+pi+ : D+
        0.,  0.,    # K-pi-pi+pi+ : D0
        0.,  0.,    # K+K-(Phi)pi+ : Ds+
        0.,  0.,    # D0(K-pi+)pi+ : D+*
        0.,  0.,    # D0(K-pi-pi+pi+)pi+ : D+*
        0.,  0.,    # D0bar(K+pi+)pi+ : B+
        0.9, 0.9,   # p+k-pi+: lambdaC+
        0.9, 0.9.,  # p+Ks(pi+pi-): lambdaC+
    )
    process.Dfinder.printInfo = cms.bool(False)
    process.Dfinder.dropUnusedTracks = cms.bool(True)
    process.dfinder = cms.Path(process.DfinderSequence)

###############################################################################

# Event Selection -> add the needed filters here
process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
process.load('HeavyIonsAnalysis.EventAnalysis.hffilterPF_cfi')
process.pAna = cms.EndPath(process.skimanalysis)

#process.HFAdcana = cms.EDAnalyzer("HFAdcToGeV",
#    digiLabel = cms.untracked.InputTag("hcalDigis"), # for Data
#    #digiLabel = cms.untracked.InputTag("simHcalUnsuppressedDigis","HFQIE10DigiCollection"), # for MC
#    minimized = cms.untracked.bool(True),
#    fillhf = cms.bool(False) # only turn this on when you have or know how to produce "towerMaker"
#)
#process.hfadc = cms.Path(process.HFAdcana)

process.MessageLogger.cerr.FwkReport.reportEvery = 100

