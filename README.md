# MuteTime

MuteTime is a forensic timeline cleaner that reduces the noise of time by filtering out irrelevant paths and artifacts from FLS or mactime bodyfiles. It helps investigators focus on **meaningful events** by trimming digital clutter and highlighting what's truly important in filesystem timelines.



`python3 mute.py --help`



## Optional

In `mute.py` you can add `warning_list["selected"].append("sys32")` at line 33. It is possible to change `sys32` by any key of `warning-timeline.json`
