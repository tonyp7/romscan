""" Provides core functions to work with rom dat files"""
import os
import zlib
from xml.dom import minidom

def crc32(filename, chunksize=65536):
    """Compute the CRC-32 checksum of the contents of the given filename"""
    with open(filename, "rb") as f:
        checksum = 0
        while (chunk := f.read(chunksize)) :
            checksum = zlib.crc32(chunk, checksum)
        return hex(checksum)[2:]


def extract_rom_info(node):
    """ Extract rom info from a rom node in a data file """
    return {'filename':node.attributes['name'].value,
                'game':node.parentNode.attributes['name'].value, 
                'description':node.parentNode.getElementsByTagName('description')[0].firstChild.data
                }



def scan_folder(path: str, dat_file: str, rename: bool=False):
    """ Scan the given folder using the specified dat file(s)."""

    #load DAT files
    dat = minidom.parse(dat_file)

    # Build a dict where the key is the CRC32
    games = {}
    xml_games = dat.getElementsByTagName('rom')
    #dat.getElementsByTagName('rom')[0].attributes['name'].value
    for g in xml_games:
        if g.hasAttribute('crc') and not (g.attributes['crc'].value in games):
            games[ g.attributes['crc'].value ] = extract_rom_info(g)

    #list files in the path
    files = next(os.walk(path), (None, None, []))[2]  # [] if no file

    for f in files:
        fullpath = os.path.join(path, f)
        chksum = crc32(fullpath)
        if chksum in games: #found a rom match
            rom = games[ chksum ]
            if rename and f != rom['filename']:
                new_name = os.path.join(path, rom['filename'])
                os.rename( fullpath, new_name)
                print( f"Found {rom['game']}, renamed to {rom['filename']}")
            else:
                print( f"Found {rom['game']}")




    return files



