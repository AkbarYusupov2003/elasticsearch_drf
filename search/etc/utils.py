import json
import sys
import os
import subprocess
import shlex
from pathlib import Path
from django.conf import settings

bento_prefix = settings.BENTO_PREFIX


def erase_content(content_path):
    content_path = Path(content_path)
    rmdir(settings.MEDIA_ROOT / content_path / "audio")
    rmdir(settings.MEDIA_ROOT / content_path / "subs")
    rmdir(settings.MEDIA_ROOT / content_path / "video")
    if Path(settings.MEDIA_ROOT / content_path / 'stream.mpd').exists():
        Path(settings.MEDIA_ROOT / content_path / 'stream.mpd').unlink()


def rmdir(directory):
    directory = Path(directory)
    if directory.exists():
        for item in directory.iterdir():
            if item.is_dir():
                rmdir(item)
            else:
                item.unlink()
        directory.rmdir()


def makeOutDir(filepath, is_file=False):
    """create unique output dir based on file name and current timestamp"""

    if is_file:
        base = os.path.dirname(filepath)
    else:
        base = filepath

    if not os.path.exists(base):
        os.makedirs(base)
    elif os.path.exists(base):
        # remove previous contents if reusing out dir
        files = os.listdir(base)
        for f in files:
            try:  # (try, except) needed because if base variable contains other dirs, exception rises
                os.unlink(os.path.join(base, f))
            except Exception as e:
                print(e)
    return base


def doCmd(cmd):  # execute a shell command and return/print its output
    args = shlex.split(cmd)  # tokenize args
    output = None
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)  # pipe stderr into stdout
    except Exception as e:
        raise e
    sys.stdout.flush()
    return output


def split_media(file_path, out_path, is_video=True):
    """
    Split media file into chunks
    :param file_path:
    :param out_path:
    :return:
    """
    doCmd(
        f"{bento_prefix}mp4split --pattern-parameters N {'--video' if is_video else '--audio'} --init-segment {os.path.join(out_path, 'init.mp4')} --media-segment {os.path.join(out_path, 'seg-%llu.m4s')} {file_path}")


def make_audio_mpd(out_path, init_path, fragmented_path, ):
    """
    Make audio mpd
    :param out_path:
    :param init_path:
    :param fragmented_path:
    :return:
    """
    doCmd(
        f"{bento_prefix}mp4dash --use-segment-timeline -o {out_path} --mpd-name=audio.mpd -f --no-media --init-segment={init_path} {fragmented_path} ")


def get_codec_string(video_path):
    """
    Get Codec Info
    :param video_path:
    :return:
    """
    v = str(video_path).replace('"', "\\\"")

    # doCmd(f"{bento_prefix}mp4info {video_path}")
    output = json.loads(doCmd(f"{bento_prefix}mp4info --format json \"{v}\"").decode('utf-8').replace('\n', ''))
    codecs_string = output["tracks"][0]["sample_descriptions"][0]["codecs_string"]
    return codecs_string


def get_video_info(video_path):
    """
    Get Video Info
    :param video_path:
    :return:
    """
    v = str(video_path).replace('"', "\\\"")

    output = json.loads(
        subprocess.check_output(f"{bento_prefix}mp4info --format json \"{v}\"", shell=True).decode('utf-8').replace(
            '\n', ''))
    return output


def fragment_video(video_path, video_out_path):
    """
    Fragment video into chunks
    :param video_path:
    :param video_out_path:
    :return:
    """
    v = str(video_path).replace('"', "\\\"")

    doCmd(f"{bento_prefix}mp4fragment \"{v}\" {video_out_path}")


def make_stream_mpd(video_path_list, out_path_dir):
    """
    Fragment video into chunks
    :param video_path_list:
    :param out_path_dir:
    :return:
    """
    # doCmd(f"{bento_prefix}mp4dash {video_path_list} -o {out_path_dir}")
    doCmd(f"{bento_prefix}mp4dash --use-segment-timeline {video_path_list} -o {out_path_dir}")


def resize_video(video_path, video_out_path, width, height):
    # doCmd(f"ffmpeg -i {video_path} -vf scale={width}:{height} -preset slow -crf 18 {video_out_path}")
    v = str(video_path).replace('"', "\\\"")

    # doCmd(f"ffmpeg -i \"{v}\" -vf scale={width}:{height} -c:v libx264 -preset slower -x264opts keyint=48:min-keyint=48:no-scenecut -strict -2 -r 24 {video_out_path}")  # for MPD
    # doCmd(f"ffmpeg -i \"{v}\" -vf scale={width}:{height} -preset ultrafast -crf 18 {video_out_path}")
    doCmd(f"ffmpeg -i \"{v}\" -vf scale={width}:{height} -preset slow -crf 18 {video_out_path}")


def resize_adv_video(video_path, video_out_path, width, height):
    doCmd(f"ffmpeg -i {video_path} -vf scale={width}:{height} -preset slow -crf 18 {video_out_path}")


def make_screenshot_from_video(video_path, screenshot_path, time_set):
    Path(Path(screenshot_path).parent).mkdir(parents=True, exist_ok=True)
    v = str(video_path).replace('"', "\\\"")
    # subprocess.call(f"yes | ffmpeg -ss 00:00:10 -i \"{v}\" -frames:v 1 -q:v 2 {screenshot_path}", shell=True)
    subprocess.call(f"yes | ffmpeg -ss {time_set} -i \"{v}\" -frames:v 1 -q:v 2 {screenshot_path}", shell=True)


# def extract_audio(video_file_path, audio_out_path):
#     v = str(video_file_path).replace('"', "\\\"")
#     doCmd(f"ffmpeg -i {v} -c copy -vn {audio_out_path} ")


# def extract_video(video_file_path, video_out_path):
#     v = str(video_file_path).replace('"', "\\\"")
#     doCmd(f"ffmpeg -i {v} -c copy -an {video_out_path}")


def make_hls(video_file_path, out_path, is_audio=False):
    """ Make HLS
    :param video_file_path путь до видео
    :param out_path путь до директории выхода без слэша
    :param is_audio будет конвертировать в видео или аудио
    """
    v = str(video_file_path).replace('"', "\\\"")
    segment_duration = 6
    doCmd(
        f"{bento_prefix}mp42hls --segment-filename-template {out_path}/segment-%d.ts --index-filename {out_path}/stream.m3u8 --segment-duration {segment_duration} --{'video' if is_audio else 'audio'}-track-id 0 {v}")


def make_adv_hls(video_file_path, out_path):
    v = str(video_file_path).replace('"', "\\\"")
    doCmd(
        f"{bento_prefix}mp42hls --segment-filename-template {out_path}/segment-%d.ts --index-filename {out_path}/stream.m3u8 {v}")


def make_audio_hls(audio_file_path, out_path):
    a = str(audio_file_path).replace('"', "\\\"")
    segment_duration = 6
    # doCmd(f"{bento_prefix}mp42hls --segment-filename-template {out_path}/segment-%d.ts --index-filename {out_path}/stream.m3u8 --segment-duration {segment_duration} --video-track-id 0 {a}")
    makeOutDir(out_path)
    doCmd(
        f"{bento_prefix}mp42hls --segment-filename-template {out_path}/segment-%d.ts --index-filename {out_path}/stream.m3u8 --segment-duration {segment_duration} --video-track-id 0 \"{a}\"")


if __name__ == '__main__':
    # fragment_video('/home/alan/Python\ Projects/sevimliplay_dj/media/sintel/video/10000kbit.mp4', '/home/alan/Python\ Projects/sevimliplay_dj/media/test.mp4')
    # split_media('/home/alan/Python\ Projects/sevimliplay_dj/media/110kbit-fragment.mp4',
    #             '/home/alan/Python\ Projects/sevimliplay_dj/media/test')
    split_media('/home/alan/Python\ Projects/sevimliplay_dj/media/test.mp4',
                '/home/alan/Python\ Projects/sevimliplay_dj/media/frag-qual-split')
    # resize_video('/home/alan/Python\ Projects/sevimliplay_dj/media/110kbit-fragment.mp4',
    #             '/home/alan/Python\ Projects/sevimliplay_dj/media/test/test.mp4', width=1920, height=1080)
