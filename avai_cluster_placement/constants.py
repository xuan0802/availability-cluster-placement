# mapping title to data
FIG_TITLE_DATA_MAP = {
    'Average availability': 'aver_avail',
    'Total bandwidth usage (Mbps)': 'total_bw',
    'Acceptance ratio (%)': 'accept_ratio'
}
# mapping title and y limit
FIG_TITLE_YLIMIT_MAP = {
    'Average availability': (0.994, 1),
    'Total bandwidth usage (Mbps)': (100, 8000)
}

LABEL_COLOR_MAP = {
    "BWGR": "blue",
    "AVGR": "red",
    "TARE": "green",
    "COGR": "purple"
}

LABEL_MARKER_MAP = {
    "BWGR": "o",
    "AVGR": "o",
    "TARE": "o",
    "COGR": "o"
}

Av_min = 0.95
Av_soft = 0.95
