import av


def trim_pyav(input_path, output_path, start_time, end_time):
    input_container = av.open(str(input_path))
    output_container = av.open(str(output_path), mode="w")

    # Setup streams
    in_streams = [
        stream
        for stream in input_container.streams
        if stream.type in ("video", "audio")
    ]
    out_streams = {
        s: output_container.add_stream(codec_name="libx264") for s in in_streams
    }

    # Seek to nearest keyframe before start
    input_container.seek(int(start_time * av.time_base), any_frame=False)

    for packet in input_container.demux(in_streams):
        if packet.pts is None:
            continue

        time = float(packet.pts * packet.time_base)

        if time < start_time:
            continue
        if time > end_time:
            break

        packet.stream = out_streams[packet.stream]
        output_container.mux(packet)

    output_container.close()
    input_container.close()


if __name__ == "__main__":
    input_path = "/home/skye/Videos/Im.Nobody.S01E21.1080p.x264-[T4TSA.cc].mkv"
    output_path = "/home/skye/Videos/trimed.mkv"
    trim_pyav(input_path, output_path, 166, 350)
