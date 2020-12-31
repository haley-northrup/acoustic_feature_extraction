Compute segment-level Rhythm features mean, std over call or day 

adapted from: /nfs/turbo/McInnisLab/gideonjn/extractRhythm.m 

get_rhythm_featrues.sh: script to run get_rhythm_features.py 
    configuration settings are in this file 
    calls get_rhythm_features.py and agg_rhythm_features.py 

get_rhythm_features.py: computes Rhythm features  
    given a set of segments and metadata, compute Rhythms features for each segment 
    compute mean, std over segments in call or day

    outputs: segments/<segment_id>.csv, calls/<call_id>.csv or days/<subject_id>_<date>.csv 
    level = call or day
        call: statistics over segments in a call 
        day: statistics over segments in a day
    call_type = personal, assessment, or all 


agg_rhythm_features.py: aggregates individual call or day feature files into a single .csv file
