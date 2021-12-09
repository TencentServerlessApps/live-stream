
RedisMaxConnection = 5
RedisConnectionTimeout = 3
RedisTimeout = 3

JobKey = "Job::{job_id}"
TaskKey = "Task::{task_id}"
EventQueue = "EventQueue::{task_id}"

TaskInitSuccess = 'init_success'
TaskInitFailed = 'init_failed'
TaskRunning = 'running'
TaskPaused = 'paused'
TaskFailed = 'failed'
TaskFinish = 'finish'

PausedSig = 'pause'
ResumeSig = 'resume'
TerminateSig = 'term'
RefreshSig = 'update'
FFmpegNormalTerminateSig = 'ffmpeg_normal_term'
FFmpegAbnormalTerminateSig = 'ffmpeg_abnormal_term'
WorkerTerminateSig = 'worker_term'

StreamBrokenSleepInterval = 100
StreamIdleTimeOut = 30 * 1000 * 1000
StreamError = {'Server error: No such stream', 'Closing connection',
               'NetStream.Play.StreamNotFound', 'HTTP error', 'Conversion failed'}
FFmpegRtmpToRtmp = "/var/user/ffmpeg -fflags nobuffer -rw_timeout {stream_idle_timeout} -i {source_url} " \
                   "-c copy -threads 4 -f flv " \
                   "{target_url}"
FFmpegVodToRtmp = "/var/user/ffmpeg -re -reconnect 1 -rw_timeout 30000000 -reconnect_at_eof 1 -reconnect_streamed 1 " \
                  "-reconnect_delay_max 2 {offset_config} -i {source_url} " \
                  "-c copy -f flv -flvflags no_duration_filesize " \
                  "{target_url}"

FFmpegVodsToRtmp = "/var/user/ffmpeg -v verbose -f concat -safe 0 -protocol_whitelist file,http,tcp,https,tls " \
                   "-re -i {file_path} -c:a aac -c:v h264 -f flv -flvflags no_duration_filesize" \
                   "{target_url}"
FFmpegJobRetry = 3
FFmpegErrorExitCode = 1
FFmpegNormalExitCode = 0
VideoRealtime = r'time=(?P<t>\S+)'

WatchDogSleepTime = 3
StreamHandlerIdleSleep = 3



