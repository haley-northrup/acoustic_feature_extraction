Compute emotion statistics from segment-level emotion predictions over a call or day 

adapted from: /nfs/turbo/chai-health/aromana/emotion_features 

run_emotion_stats.sh: script to run get_emotion_stats.py as a job, configuration settings are in this file 

get_emotion_stats.py: computes emotion statistics  
    given an emotion_preds file with 6 segment-level features (activation, valence (high, med, low)), 
    and a level (call or day), this script aggregates features to the call- or day-level. 
    the 27 stats taken over each segment-level feature are from John's When to Intervene paper.

    outputs: <level>_<call_type>_<stats_set>.csv 
    level = call or day
        call: statistics over segments in call 
        day: we take the statistics over all segments concatenated together so the features from longer calls are weighted more heavily 
    call_type = personal, assessment, or all 
    stats_set = full or abbreviated (abv)
        abv: abbreviated version of the above file. rather than the long list of 27 stats taken over the segment-level features, this is a shorter list of 5 stats. first column is call_id. other columns are 5 * 6 features. 
        full: 27 stats from John's When to Intervene paper
