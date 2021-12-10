
InvokeDefaultThreads = 20
InvokeMaxThreads = 20
TerminateTaskDefaultThreads = 20
TerminateTaskMaxThreads = 20
StreamMax = 200

RedisMaxConnection = 20
RedisConnectionTimeout = 3
RedisTimeout = 3

JobKey = "Job::{job_id}"
TaskKey = "Task::{task_id}"
EventQueue = "EventQueue::{task_id}"
PushLiveJobsSet = "PushLiveJobs"

JobOfRealTime = 'real_time'
JobOfPreset = 'preset'

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

VideoToRtmp = 'PullVodPushLive'
RtmpToRtmp = 'PullLivePushLive'