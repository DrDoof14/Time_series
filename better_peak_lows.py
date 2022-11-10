"""
1) identify borderline lows like:
- 09 14 200:220
- 09 15 270
- 09 16 230
possible solution: find_peaks with higher threshold,
we'll manage the fact that it's a borderline low after
during later analysis

2) multiple lows that should be detected as one
- 09 17 before 200 it should be one low
possible solutions:
    - custom rule
    - smoothing
    - use find_peaks function better
    - resampling with 10-15 min interval

3) identify borderline peaks

4) multiple peaks that should be detected as one
- 09 17 25 

5) peaks that should not be detected
- 09 21 150
"""

# TASK
""" TASK:
1) creating a foundation for visualizing different approaches:

    NOTE: by approaches i mean the various ways we are going to 
    solve the problems above, so a list of approaches could be something like:
    - custom_rule_1
    - custom_rule_2
    - smoothing_1
    etc...

    we want to visualize:
        - original glucose values
        - for each approach:
            - plot the relevant peak and low value with a unique symbol
    so at the end of this i can compare multiple approaches at the same time 
    NOTE: in case of smoothing, maybe just plot the
    peaks and lows over the original values, without overcrowding the plot 
    with the smoothed line

    Optional: datetime selection
    

2) brainstorm different ways in which we could attack every issue 
    an example of this are the possible solution lists above at point 1) and 2)

    NOTE: call me, text me, etc. 

3) estimate and choose the preferred way and implement that (take your time)

4) copy and paste the implementation in the streamlit page to get visual feedback
5) repeat 3) and 4) if needed or repeat 2) 3) and 4) if needed 

"""

"""
intro material
https://www.loom.com/share/e33b3c56ac2b4959ad5250950bf5090f
https://www.loom.com/share/e432c9d582d840c19c77101417009491
https://www.loom.com/share/bbe2ef0ad03c4180907819157cfdad37
https://www.loom.com/share/86db51d3d19f474087bda8b2f3f9f1b1
https://www.loom.com/share/a72a54676e0841cfa1d7ada001633cbd
https://www.loom.com/share/174396ffaf664a368613d333e592e630
"""