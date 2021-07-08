"""A video player class."""

from .video_library import VideoLibrary
from random import randint
import re


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.is_playing = False
        self.currently_playing = None
        self.is_paused = None

        self.playlist_dict = {}
        self.flagged_dict = {}

        for vid in self._video_library.get_all_videos():
            self.flagged_dict[vid.video_id] = None


    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = self._video_library.get_all_videos()
        raw_list = []

        for vid in videos:

            tags = ""

            for tag in vid.tags:
                tags = tags + tag + " "
            tags = tags[:-1]

            raw_list += [f"{vid.title} ({vid.video_id}) [{tags}]"]


        ordered_list = sorted(raw_list)


        for x in ordered_list:
            id = re.findall(r"\(([A-Za-z0-9_]+)\)", x)[0]

            if self.flagged_dict[id] != None:
                print(f"{x} - FLAGGED (reason: {self.flagged_dict[id]})")

            else:
                print(x)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if all(values != None for values in self.flagged_dict.values()):
            print(f"No videos available")
            return

        video = self._video_library.get_video(video_id)

        if video == None:
            print("Cannot play video: Video does not exist")

        elif self.flagged_dict[video_id] != None:
            print(f"Cannot play video: Video is currently flagged (reason: {self.flagged_dict[video_id]})")
            return

        elif self.is_playing == True or self.is_paused == True:
            print(f"Stopping video: {self.currently_playing.title}")
            self.is_playing = False

            print(f"Playing video: {video.title}")
            self.is_playing = True
            self.is_paused = False

        else:
            print(f"Playing video: {video.title}")
            self.is_playing = True
            self.currently_playing = video
            self.is_paused = False

    def stop_video(self):
        """Stops the current video."""
        if self.is_playing == False and self.is_paused != True:
            print("Cannot stop video: No video is currently playing")

        elif self.is_playing == False and self.is_paused != True:
            print(f"Stopping video: {self.currently_playing.title} ")
            self.is_playing = False
            self.is_paused = False

        else:
            print(f"Stopping video: {self.currently_playing.title} ")
            self.is_playing = False

    def play_random_video(self):
        """Plays a random video from the video library."""

        videos = self._video_library.get_all_videos()
        x = randint(0,len(videos)-1)
        id_list = []

        for vid in videos:
            id_list.append(vid._video_id)

        self.play_video(id_list[x])


    def pause_video(self):
        if self.is_paused == True:
            print(f"Video already paused: {self.currently_playing.title}")

        elif self.currently_playing == None:
            print("Cannot pause video: No video is currently playing")

        else:
            self.is_paused = True
            self.is_playing = False

            print(f"Pausing video: {self.currently_playing.title}")


    def continue_video(self):
        """Resumes playing the current video."""

        if self.is_paused == True:
            print(f"Continuing video: {self.currently_playing.title}")
            self.is_paused = False

        elif self.is_playing == True:
            print("Cannot continue video: Video is not paused")

        elif self.currently_playing == None:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        tags = []

        try:
            for tag in self.currently_playing.tags:
                tags.append(tag)

            tag_format = str(" ".join(tags))

            if self.is_playing == True and self.is_paused == False:
                print(f"Currently playing: {self.currently_playing.title} ({self.currently_playing._video_id}) [{tag_format}]")


            elif self.is_paused == True and self.is_playing == False:
                print(f"Currently playing: {self.currently_playing.title} ({self.currently_playing._video_id}) [{tag_format}] - PAUSED")

        except:
            print("No video is currently playing")



    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = playlist_name.lower()

        if playlist in self.playlist_dict:
            print("Cannot create playlist: A playlist with the same name already "
            "exists")

        else:
            self.playlist_dict[playlist_name] = []
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        name = playlist_name.lower()
        playlist_name_lower_dict = {k.lower(): v for (k, v) in self.playlist_dict.items()}

        try:
            if self.flagged_dict[video_id] != None:
                print(
                    f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {self.flagged_dict[video_id]})")
                return

            elif video_id in playlist_name_lower_dict[name]:
               print(f"Cannot add video to {playlist_name}: Video already added")

            elif name in playlist_name_lower_dict.keys():
                    playlist_name_lower_dict[name].append(video_id)
                    print(f"Added video to {playlist_name}: {video.title}")



        except:
            if name in playlist_name_lower_dict.keys():
                print(f"Cannot add video to {playlist_name}: Video does not exist")

            else:
                print(f"Cannot add video to {playlist_name}: Playlist does not exist")





    def show_all_playlists(self):
        """Display all playlists."""

        playlists = self.playlist_dict.keys()

        if len(playlists) == 0:
            print("No playlists exist yet")

        else:
            print("Showing all playlists:")

            for playlist in sorted(playlists):
                print(playlist)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            name = playlist_name.lower()
            playlist_name_lower_dict = {k.lower(): v for (k, v) in self.playlist_dict.items()}
            playlist_name_lower_dict[name]

            print(f"Showing playlist: {playlist_name}")

            if len(playlist_name_lower_dict[name]) == 0 :
                print("No videos here yet")

            else:
                id_list = playlist_name_lower_dict[name]
                for id in id_list:
                    vid_info = self._video_library.get_video(id)

                    tags = []

                    for tag in vid_info.tags:
                        tags.append(tag)

                    tag_format = str(" ".join(tags))

                    if self.flagged_dict[id] != None:
                        print(f"{vid_info.title} ({vid_info._video_id}) [{tag_format}] - FLAGGED (reason: {self.flagged_dict[id]})")
                        return

                    print(f"{vid_info.title} ({vid_info._video_id}) [{tag_format}]")

        except:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")



    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        name = playlist_name.lower()
        playlist_name_lower_dict = {k.lower(): v for (k, v) in self.playlist_dict.items()}

        try:
            if not video_id in playlist_name_lower_dict[name] and self._video_library.get_video(video_id)!= None:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

            elif self._video_library.get_video(video_id) == None:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")

            elif name in playlist_name_lower_dict.keys():
                info = self._video_library.get_video(video_id)

                playlist_name_lower_dict[name].remove(video_id)
                print(f"Removed video from {playlist_name}: {info.title}")

        except:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        name = playlist_name.lower()
        playlist_name_lower_dict = {k.lower(): v for (k, v) in self.playlist_dict.items()}

        try:
            playlist_name_lower_dict[name]
            if name in playlist_name_lower_dict.keys():
                playlist_name_lower_dict[name].clear()
                print(f"Successfully removed all videos from {playlist_name}")

        except:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")



    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        name = playlist_name.lower()
        playlist_name_lower_dict = {k.lower(): v for (k, v) in self.playlist_dict.items()}

        try:
            del self.playlist_dict[playlist_name]
            print(f"Deleted playlist: {playlist_name}")
        except:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")



    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        searched = []
        num = 1


        for vid in videos:
            if search_term.lower() in vid.title.lower() and self.flagged_dict[vid.video_id] == None    :
                searched.append(vid)


        if len(searched) == 0:
            print(f"No search results for {search_term}")
            return

        else:
            print(f"Here are the results for {search_term}:")

            for vid in searched:
                tags = []

                for tag in vid.tags:
                    tags.append(tag)

                tag_format = str(" ".join(tags))

                print(f"{num}) {vid.title} ({vid.video_id}) [{tag_format}]")
                num +=1

            print("Would you like to play any of the above? If yes, "
        "specify the number of the video.")

            print(
           "If your answer is not a valid number, we will assume "
           "it's a no.")

        answer = input()

        if answer.isnumeric():
            if int(answer) <= len(searched):
                self.play_video(searched[int(answer)-1].video_id)

        else:
            pass

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self._video_library.get_all_videos()
        searched = []
        num = 1

        for vid in videos:
            if video_tag in vid.tags and self.flagged_dict[vid.video_id] == None:
                searched.append(vid)

        if len(searched) == 0:
            print(f"No search results for {video_tag}")
            return

        else:
            print(f"Here are the results for {video_tag}:")

            for vid in searched:
                tags = []

                for tag in vid.tags:
                    tags.append(tag)

                tag_format = str(" ".join(tags))

                print(f"{num}) {vid.title} ({vid.video_id}) [{tag_format}]")
                num += 1

            print("Would you like to play any of the above? If yes, "
                  "specify the number of the video.")

            print(
                "If your answer is not a valid number, we will assume "
                "it's a no.")

        answer = input()

        if answer.isnumeric():
            if int(answer) <= len(searched):
                self.play_video(searched[int(answer) - 1].video_id)

        else:
            pass



    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        if flag_reason == "":
            flag_reason = "Not supplied"
            self.flagged_dict[video_id] = flag_reason
            print(f"Successfully flagged video: {self._video_library.get_video(video_id).title} (reason: {flag_reason})")


        elif video_id not in self.flagged_dict.keys():
            print("Cannot flag video: Video does not exist")

        elif self.flagged_dict[video_id] == flag_reason:
            print("Cannot flag video: Video is already flagged")

        elif self.currently_playing == self._video_library.get_video(video_id) or (self.is_paused == True and self.currently_playing == self._video_library.get_video(video_id)):
            self.flagged_dict[video_id] = flag_reason
            self.stop_video()
            self.currently_playing = None
            print(f"Successfully flagged video: {self._video_library.get_video(video_id).title} (reason: {flag_reason})")


        else:
            self.flagged_dict[video_id] = flag_reason
            print(f"Successfully flagged video: {self._video_library.get_video(video_id).title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        if video_id not in self.flagged_dict.keys():
            print("Cannot remove flag from video: Video does not exist")
            return

        elif self.flagged_dict[video_id] != None:
            self.flagged_dict[video_id] = None
            print(f"Successfully removed flag from video: {self._video_library.get_video(video_id).title}")

        elif self.flagged_dict[video_id] == None:
            print("Cannot remove flag from video: Video is not flagged")

        elif video_id not in self.flagged_dict.keys():
            print("Cannot flag video: Video does not exist")