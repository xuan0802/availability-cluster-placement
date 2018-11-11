# mapping title to data
FIG_TITLE_DATA_MAP = {
    'Average availability': 'aver_avail',
    'Total bandwidth usage (Mbps)': 'total_bw',
    'Acceptance ratio (%)': 'accept_ratio'
}
# mapping title and y limit
FIG_TITLE_YLIMIT_MAP = {
    'Average availability': (0.99, 1),
    'Total bandwidth usage (Mbps)': (100, 6000)
}

LABEL_COLOR_MAP = {
    "BWGR": "blue",
    "AVGR": "red",
    "TARE": "green",
    "COGR": "purple"
}

LABEL_MARKER_MAP = {
    "BWGR": "s",
    "AVGR": "^",
    "TARE": "D",
    "COGR": "o"
}

Av_min = 0.95
Av_soft = 0.95
