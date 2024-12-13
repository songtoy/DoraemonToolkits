import os
import numpy as np
import tgt
from tqdm import tqdm

class Preprocessor:
    def __init__(self, config):
        '''
        config: configuration object
            sampling_rate: audio sampling rate
            hop_length: stft hop length
        '''
        self.config = config
        self.in_dir = config["raw_path"]
        self.out_dir = config["preprocessed_path"]
        self.frame_rate = config["frame_rate"]

        self.prefix = config["prefix"] if "prefix" in config else ""


    def get_word_intevals(self, textgrid_file):
        textgrid = tgt.io.read_textgrid(textgrid_file, include_empty_intervals=True)
        tier = textgrid.get_tier_by_name("words")
        if tier is None:
            return None
        duration = 0
        for interval in tier.intervals:
            duration += interval.duration()
        return duration
        

    def get_alignment_phone_legacy(self, tier):
        sil_phones = ["sil", "sp", "spn", ""]

        phones = []
        durations = []
        start_time = 0
        end_time = 0
        end_idx = 0
        for t in tier._objects:
            s, e, p = t.start_time, t.end_time, t.text

            # Trim leading silences
            if phones == []:
            #    if p in sil_phones:
            #        continue
            #    else:
                start_time = s

            if p not in sil_phones:
                # For ordinary phones
                phones.append(p)
                end_time = e
                end_idx = len(phones)
            else:
                # For silent phones
                phones.append('sil')

            durations.append(
                int(
                    np.round(e * self.frame_rate)
                    - np.round(s * self.frame_rate)
                )
            )

        ## Trim tailing silences
        #phones = phones[:end_idx]
        #durations = durations[:end_idx]

        return phones, durations, start_time, end_time
    


        
if __name__ == "__main__":
    textgrid = tgt.io.read_textgrid('/path/to/TextGrid', include_empty_intervals=True)
    tier = textgrid.get_tier_by_name("words")
    print(tier)
    duration = 0
    for interval in tier.intervals:
        duration += interval.duration()
        print(interval)