import argparse
import os
import cv2


def start_record(video_url, output_path, last_im_file):
    stream = cv2.VideoCapture(video_url)

    width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = stream.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))
    last_frame = None
    print("Start video recording...", 'stream:', video_url, 'output:', output_path)
    try:
        while (True):
            ret, frame = stream.read()
            last_frame = frame.copy()
            if ret==True:
                out.write(frame)
            else:
                break
    except KeyboardInterrupt:
        print("Stop video recording...")
    finally:
        print("\nVideo recording stopped")
        if last_frame:
            cv2.imwrite(last_im_file, last_frame)

        stream.release()
        out.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads video from the video server')
    parser.add_argument("--video_url", dest='video_url', required=True, type=str, help='URL of the video')
    parser.add_argument("--output_file", dest='output_file', required=True, type=str, help='Output file')
    parser.add_argument("--last_im_file", dest='last_im_file', required=True, type=str, help='Last image file (save after process interruption)')

    args = parser.parse_args()
    start_record(args.video_url, args.output_file, args.last_im_file)
