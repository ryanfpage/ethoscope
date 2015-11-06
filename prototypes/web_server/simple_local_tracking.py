
from ethoscope.core.monitor import Monitor
from ethoscope.trackers.adaptive_bg_tracker import AdaptiveBGModel
from ethoscope.utils.io import SQLiteResultWriter
from ethoscope.hardware.input.cameras import MovieVirtualCamera
from ethoscope.drawers.drawers import DefaultDrawer

# You can also load other types of ROI builder. This one is for 20 tubes (two columns of ten rows)
from ethoscope.roi_builders.target_roi_builder import SleepMonitorWithTargetROIBuilder




#INPUT_VIDEO = "test_video.mp4"
INPUT_VIDEO = "/home/quentin/comput/ethoscope-git/src/ethoscope/tests/intergation_server_tests/test_video2.mp4"
OUTPUT_VIDEO = "/tmp/my_output.avi"
OUTPUT_DB = "/tmp/results.db"


# We use a video input file as if it was a "camera"
cam = MovieVirtualCamera(INPUT_VIDEO)

# here, we generate ROIs automatically from the targets in the images
roi_builder = SleepMonitorWithTargetROIBuilder()
rois = roi_builder.build(cam)
# Then, we go back to the first frame of the video
cam.restart()

# we use a drawer to show inferred position for each animal, display frames and save them as a video
drawer = DefaultDrawer(OUTPUT_VIDEO, draw_frames = True)
# We build our monitor
monitor = Monitor(cam, AdaptiveBGModel, rois)

# Now everything ius ready, we run the monitor with a result writer and a drawer
with SQLiteResultWriter(OUTPUT_DB, rois) as rw:
    monitor.run(rw,drawer)

