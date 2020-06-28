def solution(versions):
    exploded_versions = []
    for version in versions:
        exploded_versions.append(padded(version.split('.')))
    exploded_versions = sorted(exploded_versions, cmp=compareTo)
    compressed_versions = compress(exploded_versions)
    return compressed_versions

def padded(version):
    while len(version) < 3:
        version.append('')
    return version

def compress(exploded_versions):
    compressed = []
    for version in exploded_versions:
        compressed.append('.'.join(version).strip('.'))
    return compressed

def compareTo(v1, v2):
    #return 1 if v1 > v2
    for i in range(3):
        if v1[i] == '':
            return -1
        if v2[i] == '':
            return 1
        if int(v1[i]) > int(v2[i]):
            return 1
        if int(v2[i]) > int(v1[i]):
            return -1
    return 1

