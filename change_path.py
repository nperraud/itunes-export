""" This script change the path of all the playlist found recursively in a folder. 

Each line of a .m3u file is a path to a file. It will be replaced by the new path.
For example the path:
    ../../Users/nati/Music/Musique/Tangos/YvesPierre/Musique/Tango_Triés/Alfredo De Angelis/Alfredo De Angelis-Oscar Larroca (Tango) Vision (1953) 124.97 BPM.mp3
will be replaced by:
    ../Tangos/YvesPierre/Musique/Tango_Triés/Alfredo De Angelis/Alfredo De Angelis-Oscar Larroca (Tango) Vision (1953) 124.97 BPM.mp3

The path to be updated is stored in the variable 'old_path' and the new path in the variable 'new_path'.
In the example above, the old path is '../../Users/nati/Music/' and the new path is '../'.

The script will update all the .m3u files found recursively in the folder 'folder_path'.
The script will save the new playlist in the folder 'new_folder_path'.

The script prints the name and the path of the updated files. It also prints the number of lines updated.
"""

from pathlib import Path



def update_playlist(playlist_path, folder, old_path, new_path):
    """ Update the playlist at the path 'playlist_path' and save it in the folder 'new_folder_path'.
    """
    playlist_name = playlist_path.name
    new_playlist_path = folder.joinpath(playlist_name)
    print(playlist_name, new_playlist_path)
    with playlist_path.open() as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        new_line = line.replace(old_path, new_path)
        new_lines.append(new_line)
    with new_playlist_path.open("w") as f:
        f.writelines(new_lines)
    print("Lines updated:", len(lines))
    return len(lines)

def update_playlists(folder_path, new_folder_path, old_path, new_path):
    """ Update all the playlists found recursively in the folder 'folder_path'.

    This function creates the folder 'new_folder_path' if it does not exist.

    It also creates the subfolders of 'folder_path' in 'new_folder_path'.
    """

    if not new_folder_path.exists():
        new_folder_path.mkdir()

    total_lines = 0
    for playlist_path in folder_path.rglob("*.m3u"):
        folder = playlist_path.parent
        new_folder = new_folder_path.joinpath(folder.relative_to(folder_path))
        if not new_folder.exists():
            new_folder.mkdir(parents=True)
        total_lines += update_playlist(playlist_path, new_folder, old_path, new_path)
    return total_lines

def check_playlists(path_playlist, root_path):
    """ Check if the playlist at the path 'path_playlist' is valid.

    A playlist is valid if all the paths in the playlist lead to existing files.
    This function print the name of the invalid playlists and the name of the files that are not found.    
    
    Parameters
    ----------
    path_playlist : pathlib.Path
        Path to the playlist to check.
    root_path : pathlib.Path
        Path to the root folder of the playlist.
    
    """
    print("Checking playlist:", path_playlist.name)

    with path_playlist.open() as f:
        lines = f.readlines()
    for line in lines:
        path = root_path.joinpath(line.strip())
        if not path.exists():
            print(path_playlist.name, path)


if __name__ == "__main__":

    folder_path = Path("./out2")
    new_folder_path = Path("./out3")
    old_path = "../../Users/nati/Music/Musique/"
    new_path = "../../"

    total_lines = update_playlists(folder_path, new_folder_path, old_path, new_path)
    print("Total lines updated:", total_lines)

    folder_path = Path("./out3")
    new_folder_path = Path("./out4")

    old_path = "../../Users/nati/Music/iTunes/iTunes Media/Music/"
    new_path = "../../"

    total_lines = update_playlists(folder_path, new_folder_path, old_path, new_path)
    print("Total lines updated:", total_lines)

    root_path = Path("/Users/nati/Nextcloud/music/00 playlists/By author")

    for playlist_path in new_folder_path.rglob("*.m3u"):
        check_playlists(playlist_path, root_path)
        