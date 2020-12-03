Compute segment-level OpenSmile features mean, std over call or day 

adapted from: /nfs/turbo/chai-health/aromana/gemaps_features  

run_gemaps_features.sh: script to run get_opensmile_features.py (with GeMAPs config file) 
    configuration settings are in this file 
    calls get_opensmile_features.py and agg_opensmile_features.py 

get_opensmile_features.py: computes OpenSmile features  
    given a set of segments and metadata, compute OpenSmile features for each segment 
    compute mean, std over segments in call or day

    outputs: segments/<segment_id>.csv, calls/<call_id>.csv or days/<subject_id>_<date>.csv 
    level = call or day
        call: statistics over segments in a call 
        day: statistics over segments in a day
    call_type = personal, assessment, or all 


agg_opensmile_features.py: aggregates individual call or day feature files into a single .csv file
