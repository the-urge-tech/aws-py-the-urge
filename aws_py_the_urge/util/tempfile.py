import re


def tempfile_crawlid_extractor(tempfile):
    # remove _v2.0 we dont want the .
    tempfile = re.sub(r"_v.\..", "", tempfile)
    # keep only the filename
    if "/" in tempfile:
        tempfile = tempfile.split("/")[-1]

    matches = re.search(r".*__(.*)--.*--(.*?)\..*", tempfile)
    # if no extension
    if "." not in tempfile:
        matches = re.search(r".*__(.*)--.*--(.*)", tempfile)

    return matches.group(1)
