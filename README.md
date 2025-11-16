# 2025 CMS PbPb Run - Foresting
**Last updated: 29 October 2025**

* **Overview of Config Files**
* **1A) Setup for Low-PU pp**
* **1B) Setup for PbPb**
* **2) Processing Forests**
* **3) Quick Reference**
  * CMSSW 
  * CRAB
  * Updating "forest_CMSSW_15_X_X"
  * Updating ZDC emap
  * VOMS Certificate Setup

--------------------------------------------------------------------------------

## Overview of Config Files

### Low-PU pp Configs (use with CMSSW_15_0_X)
* **CMSSW**
  * `forest_CMSSWConfig_Run3_150X_2025LowPUpp_DATA.py`
* **CRAB**
  * `forest_CRABConfig_150X_2025LowPUpp_DATA_SpecialHLTPhysics.py`
  * `forest_CRABConfig_150X_2025LowPUpp_DATA_SpecialZeroBias.py`

### PbPb Configs (use with CMSSW_15_1_X)
* **CMSSW**
  * `forest_CMSSWConfig_Run3_151X_2025PbPb_DATA.py`: Intended for general PbPb
    data (i.e. not UPC).
  * `forest_CMSSWConfig_Run3_151X_2025PbPb_DATA_CaloTower.py`: Same as general
    PbPb data config but adds `L1CaloTowerTree`. Should only be used with
    private reco miniAOD that includes L1CaloTower info.
  * `forest_CMSSWConfig_Run3_151X_2025PbPb_DATA_UPC.py`: Specifically for
    PbPb UPC data. Uses Dfinder (see **Setup for PbPb**). Also includes
    ZDC and FSC trees.
* **CRAB**
  * `forest_CRABConfig_151X_2025PbPb_DATA_ZeroBias.py`: CRAB template for
    general PbPb data. Preset for ZeroBias PDs, modify for other PbPb data.
  * `forest_CRABConfig_151X_2025PbPb_DATA_UPC_HIForward.py`: CRAB template for
    UPC data from HIForward PDs. Modify for other UPC data.

> [!TIP]
> To test CMSSW configs, modify `INPUT_TEST_FILE` in the config and run with:
> ```bash
> cmsRun <forest_CMSSWConfig_XXX.py>
> ```
> 
> To use CRAB for foresting, you will need to work from lxplus.
> ```bash
> ssh <your_cern_id>@lxplus.cern.ch
> ```

--------------------------------------------------------------------------------

## 1A) Setup for Low-PU pp

> [!WARNING] 
> Low-PU pp uses **CMSSW_15_0_X**, *not CMSSW_15_1_X* as in PbPb!

### 1.1) Install CMSSW
```bash
cmsrel CMSSW_15_0_15_patch4
cd CMSSW_15_0_15_patch4/src
cmsenv
```


### 1.2) Add CMS Heavy Ion foresting tools
```bash
git cms-merge-topic CmsHI:forest_CMSSW_15_0_X
scram build -j4
```


### 1.3) Clone this repository and add your remote repo
**On github.com**, fork this repository to make your own version. This will be used
to document your forest configs.

Next, clone your forked version of this repo:
```bash
git clone git@github.com:<your_git_username>/HIForestSetupPbPbRun2025.git
cd HIForestSetupPbPbRun2025/
```

Finally, add the original repo as an "upstream" repo:
```bash
git remote add upstream git@github.com:jdlang/HIForestSetupPbPbRun2025.git
git fetch upstream
git pull upstream main
```



--------------------------------------------------------------------------------

## 1B) Setup for PbPb

### 1.1) Install CMSSW
```bash
cmsrel CMSSW_15_1_0_patch3
cd CMSSW_15_1_0_patch3/src
cmsenv
```


### 1.2) Add CMS Heavy Ion foresting tools
```bash
git cms-merge-topic CmsHI:forest_CMSSW_15_1_X
scram build -j4
```

> [!IMPORTANT]
> To use Dfinder, add the repo below and recompile:
> ```bash
> git clone -b Dfinder_14XX_miniAOD git@github.com:boundino/Bfinder.git --depth 1
> sed -i "s|forest_miniAOD_run3_UPC_23rereco_DATA|forest_miniAOD_run3_UPC_23rereco_DATA_wDfinder|" Bfinder/test/DnBfinder_to_Forest.sh
> source Bfinder/test/DnBfinder_to_Forest.shx
> scram build -j4
> ```

> [!TIP] 
> You can add CMSHI as a remote git reference in case of updates:
> ```bash
> git remote add cmshi git@github.com:CmsHI/cmssw.git
> ```


### 1.3) Clone this repository and add your remote repo
**On github.com**, fork this repository to make your own version. This will be used
to document your forest configs.

Next, clone your forked version of this repo:
```bash
git clone git@github.com:<your_git_username>/HIForestSetupPbPbRun2025.git
cd HIForestSetupPbPbRun2025/
```

Finally, add the original repo as an "upstream" repo:
```bash
git remote add upstream git@github.com:jdlang/HiForestSetupPbPbRun2025.git
git fetch upstream
git pull upstream main
```



--------------------------------------------------------------------------------

## 2) Processing Forests

### 2.1) Check CMSSWConfig Era and Global Tag
Confirm that your CMSSWConfig Era and Global Tag match the reco settings. These
are the lines shown below (for example):
```python
import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_pp_on_PbPb_2025_cff import Run3_pp_on_PbPb_2025
process = cms.Process('HiForest', Run3_pp_on_PbPb_2025)

HIFOREST_VERSION = "151X"
GLOBAL_TAG = "151X_dataRun3_Prompt_v1"
```

> [!TIP]
> If you are foresting from PromptReco and have a CMS DAS path, click the
> "Configs" link below the dataset entry on DAS
> ([example](https://cmsweb.cern.ch/das/request?instance=prod/global&input=config+dataset%3D%2FHIForward0%2FHIRun2025A-PromptReco-v1%2FMINIAOD)),
> and then click "show" to see the era and global tag used for reco.

### 2.2) Edit CRABConfig settings
Make a **copy** of the CRABConfig file with an appropriate name:
```bash
cp forest_CRABConfig_Run3_PbPb_DATA_TEMPLATE.py forest_CRABConfig_Run3_PbPb_DATA_<your_label>.py
```

If you want to process over a local file or a list of files, use
`forest_CRABConfig_Run3_PbPb_DATA_filelist_TEMPLATE.py` as your template 
instead. Save your file(s) to a `.txt` file using a command like:
```bash
ls /path/to/files/*.root > filelist_<your_label>.txt
# If the miniaod files are on /eos, you MUST remove "/eos/cms" from
# the start of the paths:
sed -i "s|/eos/cms||" filelist_<your_label>.txt
```

Modify the input and output paths in the config (example shown below):
```Python
# INPUT/OUTPUT SETTINGS

pd = '0'
jobTag = 'LowPUpp_SpecialZeroBias' + pd
cmsswConfig = 'forest_CMSSWConfig_Run3_150X_2025LowPUpp_DATA.py'

isOnDAS = False
# If isOnDAS == True, use these inputs:
input = '/SpecialZeroBias' + pd + '/ppRun2025-PromptReco-v1/MINIAOD'
inputDatabase = 'global'
# Otherwise, use a filelist as input:
inputFilelist = 'filelist_SpecialZeroBias' + pd + '.txt'

output = '/store/group/phys_heavyions/' + username + '/Run3_2025ExpressForests/'
outputServer = 'T2_CH_CERN'
```
Explanation of variables:
- `pd` is the PD number of the dataset being forested.
- `jobTag` is a personal label for differentiating samples.
- `cmsswConfig` is the CMSSW config file these CRAB jobs should use.
- `isOnDAS` is a toggle to use either a DAS path or a list of file paths.
- Input on DAS:
    - `input` is the miniAOD path on [CMS DAS](https://cmsweb.cern.ch/das/).
    - `inputDatabase` is the DAS "dbs instance" that contains the files
      (typically `'global'` or `'phys03'`).
- Input from file list:
    - `inputFilelist` list of local file paths on `/eos`.
- `output` is the path on the output server. Forested files are saved here.
- `outputServer` is the CMS T2 server where data will be stored.

### 2.3) Initialize VOMS proxy
```bash
voms-proxy-init -rfc -voms cms
```
> [!TIP] 
> Add an alias for this to `~/.bash_profile` to make VOMS easier:
> ```bash
> alias proxy='voms-proxy-init -rfc -voms cms; cp/tmp/x509up_u'$(id -u)' ~/'
> ```
> This will let you initialize VOMS just by running the command: `proxy`

### 2.4) Submit CRAB jobs (may need to be from `src`)
```bash
cd ..
# Copy CMSSW configs to "src"
cp HiForestSetupOORun2025/forest_CMSSWConfig* ..
# Run CRAB configs from "src"
crab submit -c HiForestSetupOORun2025/forest_CRABConfig_Run3_OO_DATA_<your_label>.py
```

### 2.5) Track status of CRAB jobs
You can view the status of a job with:
```bash
crab status -d CrabWorkArea/crab_<your job tag>/
```
> [!TIP]
> Always check job status ~2-3 minutes after submitting to make sure the job
> has been accepted! If you see the status `SUBMITREFUSED` you will need to fix
> the config(s) and delete the job folder from `CrabWorkArea/` before
> submitting it again.

When you (inevitably) have failed jobs, you can resubmit them with:
```bash
crab resubmit -d CrabWorkArea/crab_<your job tag>/
```
Optionally you can also change the requested memory or runtime for jobs when
you resubmit:
```bash
crab resubmit --maxmemory 2500 --maxruntime 300 -d CrabWorkArea/crab_<your job tag>/
```
> [!WARNING]
> Requesting more than the maximum allowed memory or runtime will result in
> your job being refused and **you will be unable to __resubmit__ any failed jobs
> for that CRAB submission!** 
> * `maxmemory` **must not exceed 3000 (MB)** for the initial submission,
>   and must not exceed 5000 (MB) for resubmissions!
> * `maxruntime` **must not exceed 900** (minutes)!

If you need to stop a job before it finishes, use:
```bash
crab kill -d CrabWorkArea/crab_<your job tag>/
```



--------------------------------------------------------------------------------

# 3) Quick Reference

## CMSSW
```bash
# Run CMSSWConfig LOCALLY:
cmsRun forest_CMSSWConfig_XXXX.py
```


## CRAB
```bash
# Submit job:
crab submit -c <CRAB_config_file.py>

# Check job status:
crab status -d <path/to/crab_status_directory/>

# Kill a job (WARNING: this is irreversible!):
crab kill -d <path/to/crab_status_directory/>

# Resubmit failed jobs:
crab resubmit -d <path/to/crab_status_directory/>
# Resubmit with max memory and max runtime
crab resubmit --maxmemory 3000 --maxruntime 450 -d <path/to/crab_status_directory/>
```


## Updating "forest_CMSSW_15_X_X"
This process should work for any branch of the `cmshi/cmssw.git` repo.
The example below uses forest_CMSSW_15_1_X:
```bash
cd CMSSW_15_1_0/src/HeavyIonsAnalysis/
git config pull.rebase true
git remote add git@github.com:cmshi/cmssw.git
git fetch cmshi forest_CMSSW_15_1_X
git pull cmshi forest_CMSSW_15_1_X

# Return to src folder and recompile:
cd ..
cmsenv
scram b -j4
```


## VOMS Certificate Setup

### Obtaining Certificates

https://ca.cern.ch/ca/user/Request.aspx?template=ee2user

Use the “New Grid User Certificate” tab to get a new CERN grid. You should set a password for this, and will need to remember it.

### Linux/Unix Installation

https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookStartingGrid#BasicGrid

To **setup the certificate** in your remote workspace, you should:
1. Export the certificate from your browser to a file in p12 format. You can 
give any name to your p12 file (in the example below the name is `mycert.p12`).

2. Place the p12 certificate file in the `.globus` directory of your home area. 
If the `.globus` directory doesn't exist, create it.
```bash
cd ~
mkdir .globus
cd ~/.globus
mv /path/to/mycert.p12 .
```

3. Execute the following shell commands:
```bash
rm -f usercert.pem
rm -f userkey.pem
openssl pkcs12 -in mycert.p12 -clcerts -nokeys -out usercert.pem
openssl pkcs12 -in mycert.p12 -nocerts -out userkey.pem
chmod 400 userkey.pem
chmod 400 usercert.pem
```
> [!WARNING]
> **If you are new to VOMS, you will need to sign the Acceptable Usage Policy 
> (AUP)** before you are able to access files, tools, and servers secured by
> certificate access. Just follow instructions here to sign the CMS AUP:
> https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideLcgAccess#AUP
